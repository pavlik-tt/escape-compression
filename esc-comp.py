def decompress(s, byte: bool = False):
    invalid = False
    if s[:6] != 'ESCCMP' or '\002' not in s or '\034' not in s:
        raise Exception("This file doesn't look like an ESC file.")
    rawheaders = s[1:].split('\002')[0].split('\034')
    headers = {}
    text = s[1:].split('\002')[1]
    if len(rawheaders) < 1 and '\x00' in text:
        raise Exception("There are no headers in the string.")
    result = ''
    for i in rawheaders:
        esc = i
        if ('[' not in esc) or (']' not in esc):
            invalid = True
            break
        if ';' not in esc:
            invalid = True
            break
        esc = esc[esc.find('[') + 1:esc.find(']')]
        esc = esc.split(';')
        if len(esc) <= 1:
            invalid = True
            continue
        try:
            char, index, n = esc[:3]
        except (TypeError, ValueError):
            invalid = True
            break
        try:
            char = int(char)
            index = int(index)
            n = int(n)
        except ValueError:
            invalid = True
            break
        try:
            headers[index] = (chr(char), n)
        except ValueError:
            invalid = True
            break
    if invalid:
        raise Exception("This file doesn't look like an ESC file.")
    skip = 0
    for i, c in enumerate(text):
        if skip:
            skip -= 1
            continue
        if c == '\x00':
            try:
                esc = headers[i]
            except KeyError:
                invalid = True
                break
            try:
                char, n = esc
            except (TypeError, ValueError):
                invalid = True
                break
            result += char * n
            continue
        result += c
    if invalid:
        raise Exception("This file doesn't look like an ESC file.")
    return result


def compress(s, mode="escape"):
    if mode not in ('py_format', 'escape'):
        raise ValueError('`mode` can be only \'escape\' or \'py_format\'')
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
    generate_pformat = lambda char, n: "{"+repr(chr(char))+"*"+str(n)+"}"
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
                if mode == 'escape':
                    if char[1] > len(generate_esc(ord(char[0]), c, char[1])):
                        headers.append([ord(char[0]), c, char[1]])
                        result += '\x1d'
                    else:
                        result += char[0] * char[1]
                elif mode == 'py_format':
                    if char[1] > len(generate_pformat(ord(char[0]), char[1])):
                        result += generate_pformat(ord(char[0]), char[1])
                    else:
                        result += char[0] * char[1]
                else:
                    raise ValueError('`mode` can be only \'escape\' or \'py_format\'')
            continue
        not_none = True
        result += i
    if mode == 'escape':
        kkk = list(result)
        for i in range(len(headers)):
            if '\x1d' not in kkk:
                break
            headers[i][1] = kkk.index('\x1d')
            kkk[kkk.index('\x1d')] = None
        newheaders = []
        for i in headers:
            newheaders.append(generate_esc(*i))
        headers = newheaders
        if len(headers) < 1:
            return False
        return "ESCCMP\001" + "\034".join(headers) + "\002" + result
    else:
        return 'f' + repr(result)
