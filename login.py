from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

def login():
    if usernameEntry.get().strip() == '' or passwordEntry.get().strip() == '':
        messagebox.showerror('Error', 'Fields cannot be empty')
    elif usernameEntry.get() == 'Rafi' and passwordEntry.get() == '1234':
        messagebox.showinfo('Success', 'Welcome')
        window.destroy()
        import studentmanagement
    else:
        messagebox.showerror('Error', 'Please enter correct credentials')

def toggle_password():
    if passwordEntry.cget('show') == '':
        passwordEntry.config(show='*')
        show_hide_btn.config(image=hide_img)
    else:
        passwordEntry.config(show='')
        show_hide_btn.config(image=show_img)

window = Tk()
window.geometry('1000x700+0+0')
window.title('Student Management System - Login')
window.resizable(False, False)


BG_COLOR = "#202942"         
BG_COLOR_2 = "#495579"       

CARD_COLOR = "#23304e"       
CARD_TEXT_COLOR = "#F4F7FB"  
PRIMARY_COLOR = "#406AFF"    
BUTTON_COLOR = "#406AFF"     
BUTTON_HOVER = "#1E3799"     
BORDER_COLOR = "#425076"     
ENTRY_BG = "#2f3f63"         
TEXT_COLOR = "#F4F7FB"       


gradient_canvas = Canvas(window, width=1000, height=700, highlightthickness=0)
gradient_canvas.place(x=0, y=0, relwidth=1, relheight=1)

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb_color):
    return '#%02x%02x%02x' % rgb_color

def draw_gradient(canvas, color1, color2, width, height):
    rgb1 = hex_to_rgb(color1)
    rgb2 = hex_to_rgb(color2)
    steps = height
    for i in range(steps):
        ratio = i / steps
        r = int(rgb1[0] * (1 - ratio) + rgb2[0] * ratio)
        g = int(rgb1[1] * (1 - ratio) + rgb2[1] * ratio)
        b = int(rgb1[2] * (1 - ratio) + rgb2[2] * ratio)
        color = rgb_to_hex((r, g, b))
        canvas.create_line(0, i, width, i, fill=color)

draw_gradient(gradient_canvas, BG_COLOR, BG_COLOR_2, 1000, 700)


shadow = Frame(window, bg="#162036")
shadow.place(relx=0.5, rely=0.5, anchor=CENTER, width=406, height=546, x=8, y=8)

card = Frame(window, bg=CARD_COLOR, bd=0, highlightthickness=0)
card.place(relx=0.5, rely=0.5, anchor=CENTER, width=406, height=546)


circle_color = "#2c3b5a"
circle = Canvas(card, width=88, height=88, bg=CARD_COLOR, highlightthickness=0)
circle.create_oval(4, 4, 84, 84, fill=circle_color, outline="")
circle.place(x=159, y=34)
try:
    logo_img = Image.open("logo.png").resize((80,80), Image.Resampling.LANCZOS)
    logo_tk = ImageTk.PhotoImage(logo_img)
    circle.create_image(44, 44, image=logo_tk)
except Exception:
    pass


Label(
    card, text="Sign In", font=("Roboto", 20, "bold"),
    fg=PRIMARY_COLOR, bg=CARD_COLOR
).place(x=0, y=130, width=406)

Label(
    card, text="Student Management System", font=("Segoe UI", 11, 'bold'),
    fg="white", bg=CARD_COLOR
).place(x=0, y=168, width=406)


user_frame = Frame(card, bg=CARD_COLOR)
user_frame.place(x=44, y=210, width=318, height=52)
try:
    user_img = Image.open("user.png").resize((24,24), Image.Resampling.LANCZOS)
    user_tk = ImageTk.PhotoImage(user_img)
    Label(user_frame, image=user_tk, bg=CARD_COLOR).place(x=0, y=13)
    user_entry_x = 36  # leave space for icon
except Exception:
    Label(user_frame, text="👤", font=("Segoe UI", 14), bg=CARD_COLOR, fg=CARD_TEXT_COLOR).place(x=0, y=13)
    user_entry_x = 36

usernameEntry = Entry(
    user_frame,
    font=('Segoe UI', 15),
    bd=0,
    relief=FLAT,
    fg=TEXT_COLOR,
    bg=ENTRY_BG,
    highlightthickness=2,
    highlightbackground=BORDER_COLOR,
    highlightcolor=PRIMARY_COLOR,
    insertbackground=TEXT_COLOR
)
usernameEntry.place(x=user_entry_x, y=0, width=318-user_entry_x, height=52)
usernameEntry.insert(0, "")


pass_frame = Frame(card, bg=CARD_COLOR)
pass_frame.place(x=44, y=280, width=318, height=52)
try:
    pass_img = Image.open("password.png").resize((24,24), Image.Resampling.LANCZOS)
    pass_tk = ImageTk.PhotoImage(pass_img)
    Label(pass_frame, image=pass_tk, bg=CARD_COLOR).place(x=0, y=13)
    pass_entry_x = 36  
except Exception:
    Label(pass_frame, text="🔒", font=("Segoe UI", 14), bg=CARD_COLOR, fg=CARD_TEXT_COLOR).place(x=0, y=13)
    pass_entry_x = 36


eye_button_width = 36  
passwordEntry = Entry(
    pass_frame,
    font=('Segoe UI', 15),
    bd=0,
    relief=FLAT,
    fg=TEXT_COLOR,
    bg=ENTRY_BG,
    highlightthickness=2,
    highlightbackground=BORDER_COLOR,
    highlightcolor=PRIMARY_COLOR,
    show='*',
    insertbackground=TEXT_COLOR
)
passwordEntry.place(x=pass_entry_x, y=0, width=318-pass_entry_x, height=52)

try:
    show_img = ImageTk.PhotoImage(Image.open("show.png").resize((18,18), Image.Resampling.LANCZOS))
    hide_img = ImageTk.PhotoImage(Image.open("hide.png").resize((18,18), Image.Resampling.LANCZOS))
except Exception:
    show_img = hide_img = None

show_hide_btn = Button(
    pass_frame, image=hide_img, bg=ENTRY_BG, bd=0, command=toggle_password,
    cursor='hand2', activebackground=ENTRY_BG, relief=FLAT
)

show_hide_btn.place(x=318-eye_button_width, y=13, width=26, height=26)


def on_enter(e): login_btn['background'] = BUTTON_HOVER
def on_leave(e): login_btn['background'] = BUTTON_COLOR

login_btn = Button(
    card, text="Login", font=('Segoe UI', 16, 'bold'),
    fg='white', bg=BUTTON_COLOR, activebackground=BUTTON_HOVER,
    activeforeground='white', cursor='hand2', command=login, bd=0, relief=FLAT
)
login_btn.place(x=44, y=382, width=318, height=46)
login_btn.bind("<Enter>", on_enter)
login_btn.bind("<Leave>", on_leave)


Label(
    card, text="© 2025 Student Management System ",
    font=("Segoe UI", 9),
    bg=CARD_COLOR, fg="#7f8ca3"
).place(x=0, y=510, width=406)

window.mainloop()