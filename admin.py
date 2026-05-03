import tkinter
from tkinter import filedialog
from tkinter import ttk
import cypher
import csv
from datetime import datetime

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
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")], defaultextension=".csv")
    if not file_path: return
    if not file_path.endswith('.csv'):
        set_status("Ошибка: выберите файл формата .csv", "red")
        return
    for item in tree.get_children():
        tree.delete(item)
    try:
        with open(file_path, 'r', encoding='utf-8', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 4:
                    decrypted_text = cypher.decrypt(row[1])
                    tree.insert('', 'end', values=(row[0], decrypted_text, row[2], row[3]))
            PATH = file_path
            set_status(f"Файл {file_path} загружен", "green")
    except Exception as e:
        set_status(f"Ошибка при чтении файла: {e}", "red")


def save_file():
    global PATH    
    if not PATH:
        PATH = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], initialfile="messages.csv")    
    if not PATH:
        return
    try:
        data_to_save = []
        for item in tree.get_children():
            row_values = tree.item(item)['values']
            encrypted_text = cypher.encrypt(str(row_values[1]))
            data_to_save.append([row_values[0], encrypted_text, row_values[2], row_values[3]])
        with open(PATH, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data_to_save)
        set_status(f"Сохранено в: {PATH}", "green")
    except Exception as e:
        set_status(f"Ошибка сохранения: {e}", "red")


def add_line():
    text = input_entry.get() 
    if not text:
        set_status("Ошибка: введите текст сообщения", "red")
        return
    all_items = tree.get_children()
    if all_items:
        last_item = all_items[-1]
        last_id = int(tree.item(last_item)['values'][0])
        new_id = last_id + 1
    else:
        new_id = 1
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tree.insert('', 'end', values=(new_id, text, current_time, "admin"))    
    input_entry.delete(0, 'end') # Очищаем поле ввода
    set_status("Запись добавлена", "green")


def delete_row():
    selected_item = tree.selection()
    if selected_item:
        hover_panel.place_forget()
        tree.delete(selected_item)
    else:
        set_status("Ошибка: сначала выберите строку", "red")

def move_up():
    leaves = tree.get_children('')
    for item in tree.selection():
        idx = leaves.index(item)
        if idx > 0:
            tree.move(item, '', idx - 1)
            check_selection(None)

def move_down():
    leaves = tree.get_children('')
    for item in tree.selection():
        idx = leaves.index(item)
        if idx < len(leaves) - 1:
            tree.move(item, '', idx + 1)
            check_selection(None)

def set_status(message, color="black"):
    status_label.config(text=message, fg=color)

def check_selection(event):
    selected = tree.selection()
    if not selected:
        return
    
    item = selected[0]
    all_items = tree.get_children()
    idx = all_items.index(item)

    if idx == 0:
        btn_up.config(state="disabled")
    else:
        btn_up.config(state="normal")

    if idx == len(all_items) - 1:
        btn_down.config(state="disabled")
    else:
        btn_down.config(state="normal")


def on_mouse_move(event):
    item_id = tree.identify_row(event.y)
    if item_id:
        bbox = tree.bbox(item_id)
        if bbox:
            x, y, width, height = bbox
            hover_panel.place(x=2, y=table_frame.winfo_y() + y - 2)            
            tree.selection_set(item_id)
            check_selection(None)
    else:
        hover_panel.place_forget()

window = tkinter.Tk()
window.resizable(False, False)
window.title("Код Цезаря")
window.geometry('400x500')

status_label = tkinter.Label(window, text="Готов", bd=1, relief=tkinter.SUNKEN, anchor=tkinter.W)
status_label.pack(side=tkinter.BOTTOM, fill=tkinter.X)

table_frame = tkinter.Frame(window)
table_frame.pack(fill="both", expand=True, padx=5)

columns = ("id", "text", "time", "ip")
tree = ttk.Treeview(table_frame, columns=columns, show="headings")

tree.heading("id", text="ID")
tree.heading("text", text="Текст")
tree.heading("time", text="Время")
tree.heading("ip", text="Адрес")

tree.column("id", width=50, anchor="center")
tree.column("text", width=100)
tree.column("time", width=90, anchor="center")
tree.column("ip", width=80, anchor="center")

table_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=table_scroll.set)
tree.bind("<<TreeviewSelect>>", check_selection)
tree.bind("<Motion>", on_mouse_move)

table_frame.columnconfigure(0, minsize=50)
table_frame.columnconfigure(1, weight=1)
table_frame.columnconfigure(2, minsize=20)

tree.grid(row=0, column=1, sticky="nsew")
table_scroll.grid(row=0, column=2, sticky="ns")

hover_panel = tkinter.Frame(window, bg="lightgrey")
btn_up = tkinter.Button(hover_panel, text="▲", width=1, command=move_up)
btn_down = tkinter.Button(hover_panel, text="▼", width=1, command=move_down)
btn_del = tkinter.Button(hover_panel, text="✖", width=1, fg="red", command=delete_row)

btn_up.pack(side="left")
btn_down.pack(side="left")
btn_del.pack(side="left")

tkinter.Label(window, text="Введите сообщение:").pack(pady=(10, 0))
input_entry = tkinter.Entry(window, width=50)
input_entry.pack(pady=5)

tkinter.Button(window, text="Добавить строку", width=BTN_WIDTH, command=add_line).pack(pady=BTN_PADY)
tkinter.Button(window, text="Загрузить файл", width=BTN_WIDTH, command=load_file).pack(pady=BTN_PADY)
tkinter.Button(window, text="Зашифровать и сохранить", width=BTN_WIDTH, command=save_file).pack(pady=BTN_PADY)

window.mainloop()