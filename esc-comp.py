def decompress(s, byte: bool = False):
    if s[:6] != 'ESCCMP':
        raise Exception("This file doesn't look like an ESC file.")
    result = ''
    rawheaders = s[1:].split('\002')[0].split('\034')
    headers = {}
    text = s[1:].split('\002')[1]
    for i in rawheaders:
        esc = i
        esc = esc[esc.find('[') + 1:esc.find(']')]
        esc = esc.split(';')
        if len(esc) <= 1:
            continue
        char, index, n = esc[:3]
        char, index, n = int(char), int(index), int(n)
        headers[index] = (chr(char), n)
    skip = 0
    for i, c in enumerate(text):
        if skip:
            skip -= 1
            continue
        if c == '\x00':
            esc = headers[i]
            char, n = esc
            result += char * n
            continue
        result += c
    return result


def compress(s):
    result = ''
    headers = []

    def remove_repeating(st):
        lists = list(st)
        removed = {}
        cur_char, start = '', -1
        for i, c in enumerate(lists):
            if i == 0 or cur_char != c:
                cur_char = c
                start = i
                continue
            lists[start] = None
            lists[i] = None
            if start in removed:
                removed[start][1] += 1
            else:
                removed[start] = [c, 2]
        return lists, removed

    generate_esc = lambda char, index, n: "\033[{};{};{}]".format(char, index, n)
    repeated = remove_repeating(s)
    if len(repeated[1]) < 1:
        return False
    not_none = True
    repeatedc = ''
    for c, i in enumerate(repeated[0]):
        if i is None:
            if not_none or repeatedc != s[c]:
                not_none = False
                char = repeated[1][c]
                repeatedc = char[0]
                if char[1] > len(generate_esc(ord(char[0]), c, char[1])):
                    headers.append([ord(char[0]), c, char[1]])
                    result += '\x1d'
                else:
                    result += char[0] * char[1]
            continue
        not_none = True
        result += i
    kkk = list(result)
    for i in range(len(headers)):
        if '\x1d' not in kkk:
            break
        headers[i][1] = kkk.index('\x00')
        kkk[kkk.index('\x1d')] = None
    newheaders = []
    for i in headers:
        newheaders.append(generate_esc(*i))
    headers = newheaders
    if len(headers) < 1:
        return False
    return "ESCCMP\001" + "\034".join(headers) + "\002" + result
