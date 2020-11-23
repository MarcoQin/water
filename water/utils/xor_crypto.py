
def o(x):
    if isinstance(x, str):
        return ord(x)
    else:
        return x


def xor_strings1(s, t):
    """xor two strings together"""
    return "".join(chr(o(a) ^ o(b)) for a, b in zip(s, t))


def xor_strings(s, t):
    len_t = len(t)
    rt = []
    for i, a in enumerate(s):
        aa = o(a) ^ o(t[i % len_t])
        rt.append(bytes([aa]))
    return b''.join(rt)
        #  print('fuck', chr(aa), chr(aa).encode('ascii'),  aa)
    #  return ''.join(chr(o(a) ^ o(t[i % len_t])) for i, a in enumerate(s))
