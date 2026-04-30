import tkinter
from tkinter import filedialog
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
    global PATH
    file_path = filedialog.askopenfilename(initialfile="encrypt.txt")
    if not file_path:
        return
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for i, line in enumerate(lines, start=1):
                clean_line = line.rstrip('\n\r')
                for char in clean_line:
                    if char not in cypher.circle: 
                        set_status(f"файл содержит недопустимые символы на строке № {i}", "red")
                        return 
            PATH = file_path
            text_area.configure(state=tkinter.NORMAL)
            text_area.delete("1.0", tkinter.END)
            for line in lines:
                clean_line = line.rstrip('\n\r')
                if clean_line:
                    decrypted = cypher.decrypt(clean_line)
                    text_area.insert(tkinter.END, decrypted + '\n')
            text_area.configure(state=tkinter.DISABLED)
            update_line_numbers(text_area, lines_text1)
    except Exception:
        set_status("не удалось открыть файл", "red")

def save_file():
    global PATH
    if not PATH:
        PATH = filedialog.asksaveasfilename(initialfile="encrypt_2.txt", defaultextension=".txt")
    if PATH:
        try:
            content = text_area.get("1.0", tkinter.END).splitlines()
            with open(PATH, "w", encoding="utf-8") as file:
                for line in content:
                    if line.strip():
                        encrypted_line = cypher.encrypt(line)
                        file.write(encrypted_line + '\n')
        except Exception:
            set_status("файл недоступен для записи", "red")


def set_scroll(sbar, first, last):
    lines_text1.yview_moveto(first)
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
        update_line_numbers(text_area, lines_text1)
        update_line_numbers(new_line, lines_text2)

def set_status(message, color="black"):
    status_label.config(text=message, fg=color)

def update_line_numbers(text_widget, number_widget):
    number_widget.yview_moveto(text_widget.yview()[0])
    number_widget.config(state="normal")
    number_widget.delete("1.0", "end")
    line_count = int(text_widget.index('end-1c').split('.')[0])
    lines_string = "\n".join(str(i) for i in range(1, line_count + 1))
    number_widget.insert("1.0", lines_string)
    number_widget.config(state="disabled")
    number_widget.yview_moveto(text_widget.yview()[0])

def sync_scroll(*args):
    text_area.yview(*args)
    lines_text1.yview(*args)


window = tkinter.Tk()
window.resizable(False, False)
window.title("Код Цезаря")
window.geometry('400x500')

status_label = tkinter.Label(window, text="Готов", bd=1, relief=tkinter.SUNKEN, anchor=tkinter.W)
status_label.pack(side=tkinter.BOTTOM, fill=tkinter.X)

text_area_container = tkinter.Frame(window)
text_area_container.pack()

lines_text1 = tkinter.Text(text_area_container, width=3, height=10+LINE_OUTPUT_TEXT, state=tkinter.DISABLED)
lines_text1.pack(side="left", fill="y")

text_area = tkinter.Text(text_area_container, height=10+LINE_OUTPUT_TEXT, wrap=tkinter.NONE, state=tkinter.DISABLED)
text_area.pack(side="left")
text_area.bind("<MouseWheel>", lambda e: lines_text1.yview_scroll(int(-1*(e.delta/120)), "units"))
text_area.config(yscrollcommand=lambda f, l: set_scroll(scrollbar, f, l))

scrollbar = tkinter.Scrollbar(text_area_container, command=text_area.yview)
scrollbar.pack(side="right", fill="y")
scrollbar.config(command=sync_scroll)

new_line_container = tkinter.Frame(window)
new_line_container.pack()

tkinter.Label(new_line_container, text="Новая строка:").pack()

lines_text2 = tkinter.Text(new_line_container, width=3, height=3+LINE_OUTPUT_NEWLINE, state=tkinter.DISABLED)
lines_text2.pack(side="left", fill="y")

new_line = tkinter.Text(new_line_container, height=3+LINE_OUTPUT_NEWLINE, width=60)
new_line.pack(side="left")
new_line.bind("<KeyRelease>", lambda e: update_line_numbers(new_line, lines_text2))

tkinter.Button(window, text="Добавить строку", width=BTN_WIDTH, command=add_line).pack(pady=BTN_PADY)
tkinter.Button(window, text="Загрузить файл", width=BTN_WIDTH, command=load_file).pack(pady=BTN_PADY)
tkinter.Button(window, text="Зашифровать и сохранить", width=BTN_WIDTH, command=save_file).pack(pady=BTN_PADY)

window.mainloop()