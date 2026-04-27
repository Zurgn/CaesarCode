import tkinter
from tkinter import filedialog, messagebox
import cypher

BTN_WIDTH = 40
BTN_PADY = 5
ID = 70223717
PATH = None

LINE_OUTPUT_NEWLINE = ID % 4
LINE_OUTPUT_TEXT = ID
while LINE_OUTPUT_TEXT >= 10:
    LINE_OUTPUT_TEXT = sum(int(digit) for digit in str(LINE_OUTPUT_TEXT))


def load_file():
    global PATH # Дурной тон, но мне можно
    file_path = filedialog.askopenfilename(title="Выберите текстовый файл", initialfile="encrypt.txt", filetypes=(("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")))
    if file_path:
        try:
            #починить лишние переносы строк
            PATH = file_path
            with open(file_path, 'r', encoding='utf-8') as file:
                text_area.configure(state=tkinter.NORMAL)
                text_area.delete("1.0", tkinter.END)
                for line in file:
                    line = line.replace("\n", "").replace("\r", "")
                    content = cypher.decrypt(line)
                    text_area.insert(tkinter.END, content + '\n')
                text_area.delete("end-2c", "end-1c")
                text_area.configure(state=tkinter.DISABLED)
        except Exception as e:
            set_status(f"Не удалось прочитать файл: {e}", "red")

def save_file():
    global PATH
    if not PATH:
        PATH = filedialog.asksaveasfilename(initialfile="text.txt", defaultextension=".txt")
    if PATH:
        content = text_area.get("1.0", tkinter.END).splitlines()
        with open(PATH, "w", encoding="utf-8") as file:
            for line in content:
                encrypted_line = cypher.encrypt(line)
                file.write(encrypted_line + '\n')
        print(f"Сохранено в {PATH}")

def set_scroll(sbar, first, last):
    first, last = float(first), float(last)
    if first <= 0.0 and last >= 1.0:
        sbar.place_forget()
    else:
        sbar.place(relx=1.0, y=0, anchor='ne', height=195, width=20)
    sbar.set(first, last)

def add_line():
    line = new_line.get("1.0", tkinter.END).strip()
    if line:
        text_area.configure(state=tkinter.NORMAL)
        text_area.insert(tkinter.END, f"\n{line}")
        new_line.delete("1.0", tkinter.END)
        text_area.configure(state=tkinter.DISABLED)

def set_status(message, color="black"):
    status_label.config(text=message, fg=color)


window = tkinter.Tk()
window.resizable(False, False)
window.title("Код Цезаря")
window.geometry('400x500')

status_label = tkinter.Label(window, text="Готов", bd=1, relief=tkinter.SUNKEN, anchor=tkinter.W)
status_label.pack(side=tkinter.BOTTOM, fill=tkinter.X)

text_area = tkinter.Text(window, height=10+LINE_OUTPUT_TEXT, wrap=tkinter.NONE, state=tkinter.DISABLED)
text_area.pack()

#----------------------------------
scrollbar = tkinter.Scrollbar(window, command=text_area.yview)
scrollbar.place(relx=1.0, y=0, anchor='ne', height=195, width=20)
text_area.config(yscrollcommand=lambda f, l: set_scroll(scrollbar, f, l))
#----------------------------------

tkinter.Label(window, text="Новая строка:").pack()
new_line = tkinter.Text(window, height=3+LINE_OUTPUT_NEWLINE, width=60)
new_line.pack()

tkinter.Button(window, text="Добавить строку", width=BTN_WIDTH, command=add_line).pack(pady=BTN_PADY)
tkinter.Button(window, text="Загрузить файл", width=BTN_WIDTH, command=load_file).pack(pady=BTN_PADY)
tkinter.Button(window, text="Зашифровать и сохранить", width=BTN_WIDTH, command=save_file).pack(pady=BTN_PADY)

window.mainloop()