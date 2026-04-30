circle = r'''0123456789абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ '''

def encrypt(text, sid=70223717): # ----->
    encrypted_message_list = []
    shift = sid%11
    count = len(text)
    inverse = circle[::-1]
    i = 1
    for i in range(count):
        symbhol = (text[i % count])
        index = inverse.find(symbhol) - shift
        encrypted_message_list.append(inverse[index])
    encrypted_message_line = "".join(encrypted_message_list)
    return encrypted_message_line

def decrypt(text, sid=70223717): # <-----
    decrypted_message_list = []
    shift = sid%11
    count = len(text)
    i = 1
    for i in range(count):
        symbhol = (text[i % count])
        index = circle.find(symbhol) - shift
        decrypted_message_list.append(circle[index])
    decrypted_message_line = "".join(decrypted_message_list)
    return decrypted_message_line


if __name__ == "__main__":
    clean = ['encrypt_result.txt', 'decrypt_result.txt']
    for file in clean:
        open(file, 'w').close()

    with open('decrypt.txt', 'r', encoding='utf-8') as file:
        for line in file:
            line = line.replace("\n", "").replace("\r", "")
            encrypted_message_line = encrypt(line)
            with open('decrypt_result.txt', 'a', encoding='utf-8') as file:
                file.write(encrypted_message_line + '\n')
    with open('decrypt_result.txt', 'r', encoding='utf-8') as file:
        for line in file:
            line = line.replace("\n", "").replace("\r", "")
            print(line)

    print('-------------------------------------------')

    with open('encrypt.txt', 'r', encoding='utf-8') as file:
        for line in file:
            line = line.replace("\n", "").replace("\r", "")
            decrypted_message_line = decrypt(line)
            with open('encrypt_result.txt', 'a', encoding='utf-8') as file:
                file.write(decrypted_message_line + '\n')
    with open('decrypt_result.txt', 'r', encoding='utf-8') as file:
        for line in file:
            line = line.replace("\n", "").replace("\r", "")
            print(line)