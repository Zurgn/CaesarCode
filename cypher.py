# from string import punctuation
# print(punctuation)

circle = r'''0123456789абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ '''

def encrypt(text, sid=70223717): # ----->
    encrypted_message_list = []
    shift = sid%11
    count = len(text)
    for i in range(count):
        symbhol = (text[i % count])
        index = (circle.find(symbhol) + shift) % len(circle)
        encrypted_message_list.append(circle[index])
    encrypted_message_line = "".join(encrypted_message_list)
    return encrypted_message_line

def decrypt(text, sid=70223717): # <-----
    decrypted_message_list = []
    shift = sid%11
    count = len(text)
    for i in range(count):
        symbhol = (text[i % count])
        index = (circle.find(symbhol) - shift) % len(circle)
        decrypted_message_list.append(circle[index])
    decrypted_message_line = "".join(decrypted_message_list)
    return decrypted_message_line


if __name__ == "__main__":
    test_ids = [70223717, 12345678, 98765432]

    for file in ['encrypt_result.txt', 'decrypt_result.txt']:
        open(file, 'w').close()

    with open('encrypt.txt', 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
        
    for i in range(3):
        result = encrypt(lines[i], sid=test_ids[i])
        
        print(f"SID: {test_ids[i]} | Исходный: {lines[i]} | Результат: {result}")

        with open('encrypt_result.txt', 'a', encoding='utf-8') as file:
            file.write(result + '\n')

    print("\n")
    
    with open('decrypt.txt', 'r', encoding='utf-8') as f:
        lines_dec = [line.strip() for line in f.readlines() if line.strip()]

    for i in range(3):
        result = decrypt(lines_dec[i], sid=test_ids[i])

        print(f"SID: {test_ids[i]} | Шифр: {lines_dec[i]} | Результат: {result}")

        with open('decrypt_result.txt', 'a', encoding='utf-8') as file:
            file.write(result + '\n')