# Transform From JavaScript to Python by ChatGPT-GPT4o
# 神必MD5加密算法, 写的看不懂一点
# 调用方式: UrpMD5.hex_md5(string, "0")
# 这个后边的应该是版本号, 目前辽宁大学2024年传的是 '0'
# By Core_65536
def md5_rotate_left(x, n):
    return (x << n) | (x >> (32 - n))


def md5_add_unsigned(a, b):
    lX8 = (a & 0x80000000)
    lY8 = (b & 0x80000000)
    lX4 = (a & 0x40000000)
    lY4 = (b & 0x40000000)
    lResult = (a & 0x3FFFFFFF) + (b & 0x3FFFFFFF)
    if lX4 & lY4:
        return lResult ^ 0x80000000 ^ lX8 ^ lY8
    if lX4 | lY4:
        if lResult & 0x40000000:
            return lResult ^ 0xC0000000 ^ lX8 ^ lY8
        else:
            return lResult ^ 0x40000000 ^ lX8 ^ lY8
    else:
        return lResult ^ lX8 ^ lY8


def md5_F(x, y, z):
    return (x & y) | ((~x) & z)


def md5_G(x, y, z):
    return (x & z) | (y & (~z))


def md5_H(x, y, z):
    return x ^ y ^ z


def md5_I(x, y, z):
    return y ^ (x | (~z))


def md5_FF(a, b, c, d, x, s, ac):
    a = md5_add_unsigned(a, md5_add_unsigned(md5_add_unsigned(md5_F(b, c, d), x), ac))
    return md5_add_unsigned(md5_rotate_left(a, s), b)


def md5_GG(a, b, c, d, x, s, ac):
    a = md5_add_unsigned(a, md5_add_unsigned(md5_add_unsigned(md5_G(b, c, d), x), ac))
    return md5_add_unsigned(md5_rotate_left(a, s), b)


def md5_HH(a, b, c, d, x, s, ac):
    a = md5_add_unsigned(a, md5_add_unsigned(md5_add_unsigned(md5_H(b, c, d), x), ac))
    return md5_add_unsigned(md5_rotate_left(a, s), b)


def md5_II(a, b, c, d, x, s, ac):
    a = md5_add_unsigned(a, md5_add_unsigned(md5_add_unsigned(md5_I(b, c, d), x), ac))
    return md5_add_unsigned(md5_rotate_left(a, s), b)


def md5_convert_to_word_array(string):
    lMessageLength = len(string)
    lNumberOfWords_temp1 = lMessageLength + 8
    lNumberOfWords_temp2 = (lNumberOfWords_temp1 - (lNumberOfWords_temp1 % 64)) // 64
    lNumberOfWords = (lNumberOfWords_temp2 + 1) * 16
    lWordArray = [0] * lNumberOfWords
    lBytePosition = 0
    lByteCount = 0
    while lByteCount < lMessageLength:
        lWordCount = (lByteCount - (lByteCount % 4)) // 4
        lBytePosition = (lByteCount % 4) * 8
        lWordArray[lWordCount] = lWordArray[lWordCount] | (ord(string[lByteCount]) << lBytePosition)
        lByteCount += 1
    lWordCount = (lByteCount - (lByteCount % 4)) // 4
    lBytePosition = (lByteCount % 4) * 8
    lWordArray[lWordCount] = lWordArray[lWordCount] | (0x80 << lBytePosition)
    lWordArray[lNumberOfWords - 2] = lMessageLength << 3
    lWordArray[lNumberOfWords - 1] = lMessageLength >> 29
    return lWordArray


def md5_word_to_hex(lValue):
    WordToHexValue = ""
    for lCount in range(4):
        lByte = (lValue >> (lCount * 8)) & 255
        WordToHexValue += "{:02x}".format(lByte)
    return WordToHexValue


def md5_utf8_encode(string):
    utftext = ""
    for char in string:
        c = ord(char)
        if c < 128:
            utftext += chr(c)
        elif 128 <= c < 2048:
            utftext += chr((c >> 6) | 192)
            utftext += chr((c & 63) | 128)
        else:
            utftext += chr((c >> 12) | 224)
            utftext += chr(((c >> 6) & 63) | 128)
            utftext += chr((c & 63) | 128)
    return utftext


def hex_md5(string, ver):
    S11, S12, S13, S14 = 7, 12, 17, 22
    S21, S22, S23, S24 = 5, 9, 14, 20
    S31, S32, S33, S34 = 4, 11, 16, 23
    S41, S42, S43, S44 = 6, 10, 15, 21

    string = md5_utf8_encode(string + ("" if ver == "1.8" else "{Urp602019}"))
    x = md5_convert_to_word_array(string)
    a, b, c, d = 0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476

    for k in range(0, len(x), 16):
        AA, BB, CC, DD = a, b, c, d
        a = md5_FF(a, b, c, d, x[k + 0], S11, 0xD76AA478)
        d = md5_FF(d, a, b, c, x[k + 1], S12, 0xE8C7B756)
        c = md5_FF(c, d, a, b, x[k + 2], S13, 0x242070DB)
        b = md5_FF(b, c, d, a, x[k + 3], S14, 0xC1BDCEEE)
        a = md5_FF(a, b, c, d, x[k + 4], S11, 0xF57C0FAF)
        d = md5_FF(d, a, b, c, x[k + 5], S12, 0x4787C62A)
        c = md5_FF(c, d, a, b, x[k + 6], S13, 0xA8304613)
        b = md5_FF(b, c, d, a, x[k + 7], S14, 0xFD469501)
        a = md5_FF(a, b, c, d, x[k + 8], S11, 0x698098D8)
        d = md5_FF(d, a, b, c, x[k + 9], S12, 0x8B44F7AF)
        c = md5_FF(c, d, a, b, x[k + 10], S13, 0xFFFF5BB1)
        b = md5_FF(b, c, d, a, x[k + 11], S14, 0x895CD7BE)
        a = md5_FF(a, b, c, d, x[k + 12], S11, 0x6B901122)
        d = md5_FF(d, a, b, c, x[k + 13], S12, 0xFD987193)
        c = md5_FF(c, d, a, b, x[k + 14], S13, 0xA679438E)
        b = md5_FF(b, c, d, a, x[k + 15], S14, 0x49B40821)
        a = md5_GG(a, b, c, d, x[k + 1], S21, 0xF61E2562)
        d = md5_GG(d, a, b, c, x[k + 6], S22, 0xC040B340)
        c = md5_GG(c, d, a, b, x[k + 11], S23, 0x265E5A51)
        b = md5_GG(b, c, d, a, x[k + 0], S24, 0xE9B6C7AA)
        a = md5_GG(a, b, c, d, x[k + 5], S21, 0xD62F105D)
        d = md5_GG(d, a, b, c, x[k + 10], S22, 0x2441453)
        c = md5_GG(c, d, a, b, x[k + 15], S23, 0xD8A1E681)
        b = md5_GG(b, c, d, a, x[k + 4], S24, 0xE7D3FBC8)
        a = md5_GG(a, b, c, d, x[k + 9], S21, 0x21E1CDE6)
        d = md5_GG(d, a, b, c, x[k + 14], S22, 0xC33707D6)
        c = md5_GG(c, d, a, b, x[k + 3], S23, 0xF4D50D87)
        b = md5_GG(b, c, d, a, x[k + 8], S24, 0x455A14ED)
        a = md5_GG(a, b, c, d, x[k + 13], S21, 0xA9E3E905)
        d = md5_GG(d, a, b, c, x[k + 2], S22, 0xFCEFA3F8)
        c = md5_GG(c, d, a, b, x[k + 7], S23, 0x676F02D9)
        b = md5_GG(b, c, d, a, x[k + 12], S24, 0x8D2A4C8A)
        a = md5_HH(a, b, c, d, x[k + 5], S31, 0xFFFA3942)
        d = md5_HH(d, a, b, c, x[k + 8], S32, 0x8771F681)
        c = md5_HH(c, d, a, b, x[k + 11], S33, 0x6D9D6122)
        b = md5_HH(b, c, d, a, x[k + 14], S34, 0xFDE5380C)
        a = md5_HH(a, b, c, d, x[k + 1], S31, 0xA4BEEA44)
        d = md5_HH(d, a, b, c, x[k + 4], S32, 0x4BDECFA9)
        c = md5_HH(c, d, a, b, x[k + 7], S33, 0xF6BB4B60)
        b = md5_HH(b, c, d, a, x[k + 10], S34, 0xBEBFBC70)
        a = md5_HH(a, b, c, d, x[k + 13], S31, 0x289B7EC6)
        d = md5_HH(d, a, b, c, x[k + 0], S32, 0xEAA127FA)
        c = md5_HH(c, d, a, b, x[k + 3], S33, 0xD4EF3085)
        b = md5_HH(b, c, d, a, x[k + 6], S34, 0x4881D05)
        a = md5_HH(a, b, c, d, x[k + 9], S31, 0xD9D4D039)
        d = md5_HH(d, a, b, c, x[k + 12], S32, 0xE6DB99E5)
        c = md5_HH(c, d, a, b, x[k + 15], S33, 0x1FA27CF8)
        b = md5_HH(b, c, d, a, x[k + 2], S34, 0xC4AC5665)
        a = md5_II(a, b, c, d, x[k + 0], S41, 0xF4292244)
        d = md5_II(d, a, b, c, x[k + 7], S42, 0x432AFF97)
        c = md5_II(c, d, a, b, x[k + 14], S43, 0xAB9423A7)
        b = md5_II(b, c, d, a, x[k + 5], S44, 0xFC93A039)
        a = md5_II(a, b, c, d, x[k + 12], S41, 0x655B59C3)
        d = md5_II(d, a, b, c, x[k + 3], S42, 0x8F0CCC92)
        c = md5_II(c, d, a, b, x[k + 10], S43, 0xFFEFF47D)
        b = md5_II(b, c, d, a, x[k + 1], S44, 0x85845DD1)
        a = md5_II(a, b, c, d, x[k + 8], S41, 0x6FA87E4F)
        d = md5_II(d, a, b, c, x[k + 15], S42, 0xFE2CE6E0)
        c = md5_II(c, d, a, b, x[k + 6], S43, 0xA3014314)
        b = md5_II(b, c, d, a, x[k + 13], S44, 0x4E0811A1)
        a = md5_II(a, b, c, d, x[k + 4], S41, 0xF7537E82)
        d = md5_II(d, a, b, c, x[k + 11], S42, 0xBD3AF235)
        c = md5_II(c, d, a, b, x[k + 2], S43, 0x2AD7D2BB)
        b = md5_II(b, c, d, a, x[k + 9], S44, 0xEB86D391)
        a = md5_add_unsigned(a, AA)
        b = md5_add_unsigned(b, BB)
        c = md5_add_unsigned(c, CC)
        d = md5_add_unsigned(d, DD)

    return (md5_word_to_hex(a) + md5_word_to_hex(b) + md5_word_to_hex(c) + md5_word_to_hex(d)).lower()
