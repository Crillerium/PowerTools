def cc_encoding(data):
    binary_str = ''.join(format(ord(c), '08b') for c in data)
    cc_str = ''
    for i in range(0, len(binary_str), 2):
        if binary_str[i:i+2] == '00':
            cc_str += '嘌'
        elif binary_str[i:i+2] == '01':
            cc_str += '呤'
        elif binary_str[i:i+2] == '10':
            cc_str += '嘧'
        elif binary_str[i:i+2] == '11':
            cc_str += '啶'

    return cc_str


def cc_decoding(cc_str):
    binary_str = ''
    for char in cc_str:
        if char == '嘌':
            binary_str += '00'
        elif char == '呤':
            binary_str += '01'
        elif char == '嘧':
            binary_str += '10'
        elif char == '啶':
            binary_str += '11'

    data = ''
    for i in range(0, len(binary_str), 8):
        byte = binary_str[i:i+8]
        data += chr(int(byte, 2))

    return data


def encrypt(data):
    cc_data = cc_encoding(data)
    return cc_data


def decrypt(cc_data):
    data = cc_decoding(cc_data)
    return data



data = "Crillerium is the most handsome boy in th world!"
encrypted_data = encrypt(data)
print("加密后的数据：", encrypted_data)

decrypted_data = decrypt(encrypted_data)
print("解密后的数据：", decrypted_data)