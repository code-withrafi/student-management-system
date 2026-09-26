import time
import os
import csv
import pymysql
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk

STUDENT_FIELDS = [
    ('Id', 'id'),
    ('Name', 'name'),
    ('Phone', 'mobile'),
    ('Email', 'email'),
    ('Address', 'address'),
    ('Gender', 'gender'),
    ('D.O.B', 'dob'),
]
DB_SCHEMA = '''CREATE TABLE IF NOT EXISTS students(
    id INT NOT NULL PRIMARY KEY,
    name VARCHAR(30),
    mobile VARCHAR(15),
    email VARCHAR(30),
    address VARCHAR(100),
    gender VARCHAR(20),
    dob VARCHAR(20),
    date VARCHAR(50),
    time VARCHAR(50)
)'''

TITLE_FONT = ("Segoe UI", 20, "bold")
SUBHEADER_FONT = ("Segoe UI", 13, "bold")
HEADER_FONT = ("Segoe UI", 12, "bold")
BODY_FONT = ("Segoe UI", 10)
BUTTON_FONT = ("Segoe UI Semibold", 10, "bold")

COLOR_BG = "#fafdff"           
COLOR_PANEL_BG = "#e8f0f6"     
COLOR_HEADER_BG = "#173753"    
COLOR_HEADER_FG = "#fafdff"    
COLOR_ACCENT = "#3fc1c9"       
COLOR_ACCENT_DARK = "#145374"  
COLOR_TABLE_HEADER = "#145374"

# Button styling
COLOR_BTN_BG = "#C0C0C0"         
COLOR_BTN_BG_ACTIVE = "#3aafa9"  
COLOR_BTN_FG = "#000000"         
COLOR_BTN_DISABLED = "#708090"   

# --- Utility Functions ---
def create_form(window, fields, initial=None):
    entries = {}
    form_frame = Frame(window, bg=COLOR_PANEL_BG)
    form_frame.pack(fill=X)
    LABEL_WIDTH = 12
    ENTRY_WIDTH = 32
    for i, (label, key) in enumerate(fields):
        ttk.Label(
            form_frame, text=label, font=BODY_FONT, background=COLOR_PANEL_BG, anchor=W, width=LABEL_WIDTH
        ).grid(row=i, column=0, padx=(0, 5), pady=6, sticky="w")
        entry = ttk.Entry(form_frame, font=BODY_FONT, width=ENTRY_WIDTH)
        entry.grid(row=i, column=1, padx=(0, 15), pady=6, sticky="ew")
        if initial and key in initial:
            entry.insert(0, initial[key])
        entries[key] = entry
    form_frame.grid_columnconfigure(1, weight=1)
    return entries

def get_form_values(entries):
    return {k: v.get() for k, v in entries.items()}


def connect_database():
    def connect():
        global mycursor, con
        try:
            con = pymysql.connect(
                host=hostEntry.get(),
                user=usernameEntry.get(),
                password=passwordEntry.get()
            )
            mycursor = con.cursor()
            mycursor.execute('CREATE DATABASE IF NOT EXISTS studentmanagementsystem')
            mycursor.execute('USE studentmanagementsystem')
            mycursor.execute(DB_SCHEMA)
            con.commit()
            messagebox.showinfo('Success', 'Database Connected Successfully', parent=connectWindow)
            connectWindow.destroy()
            for btn in action_buttons:
                btn.config(state=NORMAL)
            show_student()
            set_status("Connected to database successfully.")
        except Exception as e:
            messagebox.showerror('Error', f'Invalid Details\n{str(e)}', parent=connectWindow)
            set_status("Database connection failed.")

    connectWindow = Toplevel()
    connectWindow.grab_set()
    connectWindow.geometry('420x260+750+250')
    connectWindow.title('Database Connection')
    connectWindow.resizable(False, False)
    connectWindow.configure(bg=COLOR_PANEL_BG)

    header_frame = Frame(connectWindow, bg=COLOR_HEADER_BG, height=50)
    header_frame.pack(fill=X)
    Label(header_frame, text="Database Connection", font=SUBHEADER_FONT,
          bg=COLOR_HEADER_BG, fg=COLOR_HEADER_FG).pack(pady=10)

    content_frame = Frame(connectWindow, bg=COLOR_PANEL_BG)
    content_frame.pack(pady=16, padx=20, fill=BOTH, expand=True)

    LABEL_WIDTH = 14
    ENTRY_WIDTH = 28

    fields = [
        ('Host Name', 'localhost'),
        ('User Name', 'root'),
        ('Password', ''),
    ]
    global hostEntry, usernameEntry, passwordEntry
    for i, (text, default) in enumerate(fields):
        ttk.Label(content_frame, text=text, font=BODY_FONT, background=COLOR_PANEL_BG,
                  anchor=W, width=LABEL_WIDTH).grid(row=i, column=0, padx=(0, 5), pady=8, sticky="w")
        entry = ttk.Entry(content_frame, font=BODY_FONT, width=ENTRY_WIDTH,
                          show='*' if text == 'Password' else '')
        entry.grid(row=i, column=1, padx=(0, 10), pady=8, sticky="ew")
        entry.insert(0, default)
        if text == 'Host Name':
            hostEntry = entry
        elif text == 'User Name':
            usernameEntry = entry
        else:
            passwordEntry = entry
    content_frame.grid_columnconfigure(1, weight=1)

    button_frame = Frame(connectWindow, bg=COLOR_PANEL_BG)
    button_frame.pack(pady=8)
    ttk.Button(button_frame, text='Connect', style='Accent.TButton', command=connect).pack(side=LEFT, padx=10)
    ttk.Button(button_frame, text='Cancel', style='Accent.TButton', command=connectWindow.destroy).pack(side=LEFT, padx=10)


def show_student():
    try:
        mycursor.execute('SELECT * FROM students')
        studentTable.delete(*studentTable.get_children())
        for data in mycursor.fetchall():
            studentTable.insert('', END, values=data)
        set_status("Loaded student records.")
    except Exception as e:
        messagebox.showerror('Error', str(e))
        set_status("Failed to load students.")

def add_student():
    def add_data():
        values = get_form_values(entries)
        if any(v == '' for v in values.values()):
            messagebox.showerror('Error', 'All Fields are required', parent=add_window)
            return
        currentdate = time.strftime('%d/%m/%Y')
        currenttime = time.strftime('%H:%M:%S')
        try:
            mycursor.execute('INSERT INTO students VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                             (int(values['id']), values['name'], values['mobile'], values['email'],
                              values['address'], values['gender'], values['dob'], currentdate, currenttime))
            con.commit()
            messagebox.showinfo('Success', 'Data added successfully!', parent=add_window)
            add_window.destroy()
            show_student()
            set_status("Added new student.")
        except Exception as e:
            messagebox.showerror('Error', f'Id cannot be repeated or error occurred\n{str(e)}', parent=add_window)
            set_status("Failed to add student.")

    add_window = Toplevel(root)
    add_window.grab_set()
    add_window.resizable(False, False)
    add_window.title('Add Student')
    add_window.configure(bg=COLOR_PANEL_BG)

    header_frame = Frame(add_window, bg=COLOR_ACCENT, height=50)
    header_frame.pack(fill=X)
    Label(header_frame, text="Add New Student", font=SUBHEADER_FONT, bg=COLOR_ACCENT, fg=COLOR_HEADER_FG).pack(pady=12)

    content_frame = Frame(add_window, bg=COLOR_PANEL_BG)
    content_frame.pack(pady=10, padx=22, fill=BOTH, expand=True)
    entries = create_form(content_frame, STUDENT_FIELDS)

    button_frame = Frame(add_window, bg=COLOR_PANEL_BG)
    button_frame.pack(pady=10)
    ttk.Button(button_frame, text='Add Student', style='Accent.TButton', command=add_data).pack(side=LEFT, padx=10)
    ttk.Button(button_frame, text='Cancel', style='Accent.TButton', command=add_window.destroy).pack(side=LEFT, padx=10)

def update_student():
    def update_data():
        values = get_form_values(entries)
        currentdate = time.strftime('%d/%m/%Y')
        currenttime = time.strftime('%H:%M:%S')
        try:
            mycursor.execute(
                '''UPDATE students SET name=%s, mobile=%s, email=%s, address=%s, gender=%s, dob=%s, date=%s, time=%s WHERE id=%s''',
                (values['name'], values['mobile'], values['email'], values['address'],
                 values['gender'], values['dob'], currentdate, currenttime, values['id']))
            con.commit()
            messagebox.showinfo('Success', f'Id {values["id"]} is updated successfully!', parent=update_window)
            update_window.destroy()
            show_student()
            set_status("Updated student.")
        except Exception as e:
            messagebox.showerror('Error', f'Update failed\n{str(e)}', parent=update_window)
            set_status("Update failed.")

    indexing = studentTable.focus()
    if not indexing:
        messagebox.showerror('Error', 'Please select a student to update!')
        return
    listdata = studentTable.item(indexing)['values']
    if not listdata:
        return
    initial = dict(zip([k for _, k in STUDENT_FIELDS], listdata))
    update_window = Toplevel(root)
    update_window.grab_set()
    update_window.title('Update Student')
    update_window.resizable(False, False)
    update_window.configure(bg=COLOR_PANEL_BG)

    header_frame = Frame(update_window, bg=COLOR_ACCENT, height=50)
    header_frame.pack(fill=X)
    Label(header_frame, text="Update Student", font=SUBHEADER_FONT, bg=COLOR_ACCENT, fg=COLOR_HEADER_FG).pack(pady=12)

    content_frame = Frame(update_window, bg=COLOR_PANEL_BG)
    content_frame.pack(pady=10, padx=22, fill=BOTH, expand=True)
    entries = create_form(content_frame, STUDENT_FIELDS, initial)

    button_frame = Frame(update_window, bg=COLOR_PANEL_BG)
    button_frame.pack(pady=10)
    ttk.Button(button_frame, text='Update', style='Accent.TButton', command=update_data).pack(side=LEFT, padx=10)
    ttk.Button(button_frame, text='Cancel', style='Accent.TButton', command=update_window.destroy).pack(side=LEFT, padx=10)

def delete_student():
    try:
        indexing = studentTable.focus()
        if not indexing:
            messagebox.showerror('Error', 'Please select a student to delete!')
            return
        content_id = studentTable.item(indexing)['values'][0]
        if messagebox.askyesno('Confirm Delete', f'Are you sure you want to delete student ID {content_id}?'):
            mycursor.execute('DELETE FROM students WHERE id=%s', (content_id,))
            con.commit()
            messagebox.showinfo('Deleted', f'ID {content_id} is deleted successfully')
            show_student()
            set_status("Deleted student.")
            
    except Exception as e:
        messagebox.showerror('Error', str(e))
        set_status("Delete failed.")

def search_student():
    def search_data():
        vals = get_form_values(entries)
        query = '''SELECT * FROM students WHERE
                id=%s OR name=%s OR mobile=%s OR email=%s OR address=%s OR gender=%s OR dob=%s'''
        mycursor.execute(query, (
            vals['id'], vals['name'], vals['mobile'], vals['email'], vals['address'], vals['gender'], vals['dob']
        ))
        studentTable.delete(*studentTable.get_children())
        found = False
        for data in mycursor.fetchall():
            studentTable.insert('', END, values=data)
            found = True
        if found:
            set_status("Search completed.")
            search_window.destroy()
        else:
            set_status("No student found.")

    search_window = Toplevel(root)
    search_window.title('Search Student')
    search_window.grab_set()
    search_window.resizable(False, False)
    search_window.configure(bg=COLOR_PANEL_BG)

    header_frame = Frame(search_window, bg=COLOR_ACCENT, height=50)
    header_frame.pack(fill=X)
    Label(header_frame, text="Search Student", font=SUBHEADER_FONT, bg=COLOR_ACCENT, fg=COLOR_HEADER_FG).pack(pady=12)

    content_frame = Frame(search_window, bg=COLOR_PANEL_BG)
    content_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)
    entries = create_form(content_frame, STUDENT_FIELDS)

    button_frame = Frame(search_window, bg=COLOR_PANEL_BG)
    button_frame.pack(pady=10)
    ttk.Button(button_frame, text='Search', style='Accent.TButton', command=search_data).pack(side=LEFT, padx=10)
    ttk.Button(button_frame, text='Cancel', style='Accent.TButton', command=search_window.destroy).pack(side=LEFT, padx=10)
    ttk.Button(button_frame, text='Reset', style='Accent.TButton', command=show_student).pack(side=LEFT, padx=10)

def export_data():
    try:
        if not studentTable.get_children():
            messagebox.showerror('Error', 'No data available to export!', parent=root)
            return
        file = filedialog.asksaveasfilename(
            defaultextension='.csv',
            filetypes=[('CSV files', '*.csv'), ('All files', '*.*')],
            parent=root,
            title="Save Student Data"
        )
        if file:
            with open(file, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                headers = [studentTable.heading(col)['text'] for col in studentTable['columns']]
                writer.writerow(headers)
                for row_id in studentTable.get_children():
                    writer.writerow(studentTable.item(row_id)['values'])
            messagebox.showinfo('Success', f'Data exported successfully to:\n{file}', parent=root)
            set_status(f"Exported data to {os.path.basename(file)}")
    except Exception as e:
        messagebox.showerror('Error', f'Export failed\n{str(e)}', parent=root)
        set_status("Export failed.")

def confirm_exit():
    if messagebox.askyesno("Confirm Exit", "Are you sure you want to exit?", parent=root):
        root.destroy()

def set_status(msg):
    status_var.set(f"  {msg}")

# --- Main Application ---
root = Tk()
root.geometry('1200x700+80+40')
root.resizable(False, False)
root.title('Student Management System')
root.configure(bg=COLOR_BG)

# --- Custom Styles ---
style = ttk.Style(root)
style.theme_use('clam')

style.configure('Accent.TButton', font=BUTTON_FONT, background=COLOR_BTN_BG, foreground=COLOR_BTN_FG)
style.map('Accent.TButton',
          foreground=[('disabled', COLOR_BTN_FG), ('!disabled', COLOR_BTN_FG)],
          background=[('disabled', COLOR_BTN_DISABLED), ('active', COLOR_BTN_BG_ACTIVE), ('pressed', COLOR_BTN_BG_ACTIVE), ('!disabled', COLOR_BTN_BG)])

for btn_style in ['Default.TButton', 'Cancel.TButton', 'Danger.TButton', 'Success.TButton', 'Export.TButton', 'Show.TButton']:
    style.configure(btn_style, font=BUTTON_FONT, background=COLOR_BTN_BG, foreground=COLOR_BTN_FG)
    style.map(btn_style,
        foreground=[('disabled', COLOR_BTN_FG), ('!disabled', COLOR_BTN_FG)],
        background=[('disabled', COLOR_BTN_DISABLED), ('active', COLOR_BTN_BG_ACTIVE), ('pressed', COLOR_BTN_BG_ACTIVE), ('!disabled', COLOR_BTN_BG)]
    )

style.configure('Header.TLabel', font=SUBHEADER_FONT, background=COLOR_HEADER_BG, foreground=COLOR_HEADER_FG)

# Treeview styles
style.configure('Treeview',
    background=COLOR_BG,
    foreground="#232931",
    rowheight=28,
    fieldbackground=COLOR_BG,
    font=BODY_FONT,
    borderwidth=0,
    relief=FLAT
)
style.configure('Treeview.Heading',
    font=HEADER_FONT,
    foreground=COLOR_HEADER_FG,
    background=COLOR_TABLE_HEADER,
    borderwidth=0,
    relief=FLAT
)
style.map('Treeview.Heading',
    foreground=[('active', COLOR_ACCENT), ('!active', COLOR_HEADER_FG)],
    background=[('active', COLOR_TABLE_HEADER), ('!active', COLOR_TABLE_HEADER)]
)
style.map('Treeview',
    background=[('selected', '#e3f6fc')],
    foreground=[('selected', "#232931")]
)

# --- Header bar ---
header = Frame(root, bg=COLOR_HEADER_BG, height=70)
header.pack(fill=X, side=TOP)

logo_frame = Frame(header, bg=COLOR_HEADER_BG)
logo_frame.pack(side=LEFT, padx=22)

try:
    logo_path = 'students.png'
    if os.path.exists(logo_path):
        img = Image.open(logo_path)
        img = img.resize((44, 44), Image.LANCZOS)
        logo_img = ImageTk.PhotoImage(img)
        logo_lbl = Label(logo_frame, image=logo_img, bg=COLOR_HEADER_BG)
        logo_lbl.image = logo_img
        logo_lbl.pack(side=LEFT, padx=5)
    else:
        logo_lbl = Label(logo_frame, text='🎓', bg=COLOR_HEADER_BG, font=('Segoe UI Emoji', 30))
        logo_lbl.pack(side=LEFT, padx=5)
except Exception:
    logo_lbl = Label(logo_frame, text='🎓', bg=COLOR_HEADER_BG, font=('Segoe UI Emoji', 30))
    logo_lbl.pack(side=LEFT, padx=5)

title_lbl = Label(logo_frame, text='Student Management System', bg=COLOR_HEADER_BG,
                  fg=COLOR_HEADER_FG, font=TITLE_FONT)
title_lbl.pack(side=LEFT, padx=18)

datetime_frame = Frame(header, bg=COLOR_HEADER_BG)
datetime_frame.pack(side=RIGHT, padx=28)

datetimeLabel = Label(datetime_frame, font=BODY_FONT, bg=COLOR_HEADER_BG, fg=COLOR_HEADER_FG)
datetimeLabel.pack(pady=5)

def clock():
    date = time.strftime('%d/%m/%Y')
    currenttime = time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'  Date: {date}  |  Time: {currenttime}')
    datetimeLabel.after(1000, clock)
clock()

connect_btn = ttk.Button(header, text='Connect Database', style='Accent.TButton', command=connect_database)
connect_btn.pack(side=RIGHT, padx=10, pady=10)

# --- Main Content ---
main_frame = Frame(root, bg=COLOR_BG)
main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

# --- Left Panel ---
leftFrame = Frame(main_frame, bg=COLOR_PANEL_BG, bd=0, relief=FLAT)
leftFrame.pack(side=LEFT, fill=Y, padx=(0, 10))

section_header = Frame(leftFrame, bg=COLOR_HEADER_BG)
section_header.pack(fill=X, pady=(0, 12))
Label(section_header, text="Actions", font=SUBHEADER_FONT, bg=COLOR_HEADER_BG, fg=COLOR_HEADER_FG).pack(pady=10)

action_buttons = [
    ttk.Button(leftFrame, text='Add Student', style='Accent.TButton', state=DISABLED, command=add_student),
    ttk.Button(leftFrame, text='Search Student', style='Accent.TButton', state=DISABLED, command=search_student),
    ttk.Button(leftFrame, text='Delete Student', style='Accent.TButton', state=DISABLED, command=delete_student),
    ttk.Button(leftFrame, text='Update Student', style='Accent.TButton', state=DISABLED, command=update_student),
    ttk.Button(leftFrame, text='Show Students', style='Accent.TButton', state=DISABLED, command=show_student),
    ttk.Button(leftFrame, text='Export Data', style='Accent.TButton', state=DISABLED, command=export_data),
]
for btn in action_buttons:
    btn.pack(fill=X, pady=7, ipady=6)

ttk.Button(leftFrame, text='Exit', style='Accent.TButton', command=confirm_exit) \
    .pack(fill=X, pady=(36, 0), ipady=6)

# --- Right Panel ---
rightFrame = Frame(main_frame, bg=COLOR_BG, bd=0)
rightFrame.pack(side=RIGHT, fill=BOTH, expand=True)

table_header = Frame(rightFrame, bg=COLOR_HEADER_BG)
table_header.pack(fill=X)
Label(table_header, text="Student Records", font=SUBHEADER_FONT, bg=COLOR_HEADER_BG, fg=COLOR_HEADER_FG).pack(pady=10)

table_container = Frame(rightFrame, bg=COLOR_BG)
table_container.pack(fill=BOTH, expand=True)

scrollBarX = Scrollbar(table_container, orient=HORIZONTAL)
scrollBarY = Scrollbar(table_container, orient=VERTICAL)

studentTable = ttk.Treeview(
    table_container,
    columns=('Id', 'Name', 'Mobile Number', 'Email', 'Address', 'Gender', 'Date Of Birth', 'Added Date', 'Added Time'),
    xscrollcommand=scrollBarX.set,
    yscrollcommand=scrollBarY.set,
    style="Treeview"
)

scrollBarX.config(command=studentTable.xview)
scrollBarY.config(command=studentTable.yview)
scrollBarX.pack(side=BOTTOM, fill=X)
scrollBarY.pack(side=RIGHT, fill=Y)
studentTable.pack(side=LEFT, fill=BOTH, expand=True)

for col, width in zip(studentTable['columns'], [60, 200, 100, 210, 190, 90, 140, 110, 110]):
    studentTable.heading(col, text=col)
    studentTable.column(col, width=width, anchor=CENTER)
studentTable.config(show='headings')

# --- Footer / Copyright ---
footer_frame = Frame(root, bg=COLOR_HEADER_BG, height=24)
footer_frame.pack(fill=X, side=BOTTOM)
Label(
    footer_frame,
    text="© 2025 Student Management System",
    bg=COLOR_HEADER_BG,
    fg=COLOR_HEADER_FG,
    font=("Segoe UI", 9, "italic"),
    anchor='center',
    justify='center'
).pack(fill=X, pady=2)

# --- Status bar ---
status_var = StringVar()
status_var.set("  Connect Database For Access")
status_bar = Frame(root, bg=COLOR_HEADER_BG, height=28)
status_bar.pack(fill=X, side=BOTTOM)
Label(status_bar, textvariable=status_var, bg=COLOR_HEADER_BG, fg=COLOR_HEADER_FG, font=BODY_FONT).pack(side=LEFT, padx=12)

root.mainloop()