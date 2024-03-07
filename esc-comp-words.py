import string as stri

def compress_words(s):
    p = stri.punctuation
    result = []
    already_passed = []
    repetitions = {}
    def idk_how_to_name_this(og_str, md_str):
        if not md_str:
            return '{}'
        result = ""
        skip = 0
        for i in og_str:
            if skip:
                skip -= 1
                continue
            if i == md_str[0]:
                result += '{}'
                skip = len(md_str)-1
                continue
            result += i
        return result
    for i,c in enumerate(s.split(' ')):  # i - index; c - character
        stripped = c.strip(p)
        if stripped in already_passed:
            formatted = idk_how_to_name_this(c, stripped).format('\x00')
            result.append(formatted)
            #           idk if this is gonna work
            repetitions[i+formatted.find('\x00')] = already_passed.index(stripped)
            continue
        result.append(c)
        already_passed.append(stripped)
    return " ".join(result)
