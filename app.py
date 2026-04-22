import tkinter
from tkinter import filedialog, messagebox
import cypher

def load_file():
    file_path = filedialog.askopenfilename(title="Выберите текстовый файл", filetypes=(("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")))
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text_area.configure(state=tkinter.NORMAL)
                text_area.delete("1.0", tkinter.END)
                for line in file:
                    line = line.replace("\n", "").replace("\r", "")
                    content = cypher.decrypt(line)
                    text_area.insert(tkinter.END, content + '\n')
                text_area.configure(state=tkinter.DISABLED)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось прочитать файл: {e}")

def set_scroll(sbar, first, last):
    first, last = float(first), float(last)
    if first <= 0.0 and last >= 1.0:
        sbar.place_forget()
    else:
        sbar.place(relx=1.0, y=0, anchor='ne', height=195, width=20)
    sbar.set(first, last)

window = tkinter.Tk()
window.title("Код Цезаря")
window.geometry('400x500')

# Рассчитываем количество строк в выводе исходя из условия задания
line_output = 70223717
while line_output >= 10:
    line_output = sum(int(digit) for digit in str(line_output))
print(line_output)

text_area = tkinter.Text(window, height=10+line_output, wrap=tkinter.NONE, state=tkinter.DISABLED)
text_area.pack()

scrollbar = tkinter.Scrollbar(window, command=text_area.yview)
scrollbar.place(relx=1.0, y=0, anchor='ne', height=195, width=20)
text_area.config(yscrollcommand=lambda f, l: set_scroll(scrollbar, f, l))

btn_load = tkinter.Button(window, text="Загрузить файл", command=load_file)
btn_load.pack(fill='x', padx=10, pady=5)

window.mainloop()