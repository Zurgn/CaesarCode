# Набор символов используемый для кодирования
circle = r'''0123456789абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ '''

# Метод зашифровки
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
    with open('encrypt_result.txt', 'a', encoding='utf-8') as file:
        file.write(encrypted_message_line + '\n')

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
    with open('decrypt_result.txt', 'a', encoding='utf-8') as file:
        file.write(decrypted_message_line + '\n')


# Выполняем если код запущен напрямую
if __name__ == "__main__":
    # Удаляем всё из файлов с результатами
    clean = ['encrypt_result.txt', 'decrypt_result.txt']
    for file in clean:
        open(file, 'w').close()

    # Открываем вайл encrypt.txt, перебираем каждую линию удаляя перенос строки и применяем к ней метод encrypt
    with open('encrypt.txt', 'r', encoding='utf-8') as file:
        for line in file:
            line = line.replace("\n", "").replace("\r", "")
            encrypt(line)
    # Открываем файл encrypt_result.txt и выводим его содержимое
    with open('encrypt_result.txt', 'r', encoding='utf-8') as file:
        for line in file:
            line = line.replace("\n", "").replace("\r", "")
            print(line)

    print('-------------------------------------------')

    # Открываем вайл decrypt.txt, перебираем каждую линию удаляя перенос строки и применяем к ней метод decrypt
    with open('decrypt.txt', 'r', encoding='utf-8') as file:
        for line in file:
            line = line.replace("\n", "").replace("\r", "")
            decrypt(line)
    # Открываем файл decrypt_result.txt и выводим его содержимое
    with open('decrypt_result.txt', 'r', encoding='utf-8') as file:
        for line in file:
            line = line.replace("\n", "").replace("\r", "")
            print(line)