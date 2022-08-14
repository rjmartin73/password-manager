from tkinter import (Tk, Entry, Canvas, PhotoImage, ttk)
from tkinter import messagebox, END, LEFT
from password_gen import generate_password
import json
import platform
platform = platform.platform()
print(platform)


# CONSTANTS
WHITE = "#FBFCFC"
LABEL_FONT = ("Verdana", 11, "normal")
BUTTON_FONT = ("Verdana", 12, "normal")
PSWD_FILE = "passwords.json"


# -------------------------- PASSWORD GENERATOR -----------------------------#
def create_password():
    count = 1
    len = 12
    upper = 2
    digits = 2
    special = 2

    if password_entry.get() != "":
        password_entry.delete(0, END)

    new_password = generate_password(len, upper, digits, special, count)
    password_entry.insert(0, new_password)

    window.clipboard_clear()
    window.clipboard_append(new_password)
    window.update()


# Open file function
def open_file(filename: str, method: str) -> object:
    try:
        data_file = open(filename, method)
    except FileNotFoundError:
        data_file = open(filename, "w")
        data_file.close()
        data_file = open_file(filename, method)

    return data_file


# Get JSON data function
def get_json_data(json_file: object) -> dict:
    try:
        data = json.load(json_file)
    except json.JSONDecodeError:
        data = {}
    return data


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    read = "r"
    write = "w"
    append = "a"
    output = {
            website.casefold(): {
                "email": email.casefold(),
                "password": password
                }
            }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Missing Data",
                            message="Please fill out all entries.")
        return

    data_file = open_file(PSWD_FILE, read)

    data = get_json_data(data_file)
    data_file.close()

    data.update(output)
    data_file = open_file(PSWD_FILE, write)
    json.dump(data, data_file, indent=4)
    website_entry.delete(0, END)
    password_entry.delete(0, END)
    data_file.close()


# ------------------------------- SEARCH ----------------------------------- #
def search():

    website = website_entry.get().casefold()
    if len(website) == 0:
        return

    data_file = open_file(PSWD_FILE, "r")
    data = get_json_data(data_file)
    data_file.close()

    # for key, value in data.items():
    #     print("Website:", key)
    #     print("Data", value)

    if website in data:
        email = data[website]["email"]
        password = data[website]["password"]
        messagebox.showinfo(title=f"Results for {website}",
                            message=f"username: {email}\npassword: {password}")
        window.clipboard_clear()
        window.clipboard_append(password)
        window.update()

    else:
        messagebox.showinfo(title="Not Found", message=f"{website.title()} not found.")


# ------------------------------ UI SETUP ---------------------------------- #
# Window
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

# Canvas
canvas = Canvas(window, width=200, height=200,
                highlightthickness=0, relief="ridge")
canvas.grid(row=1, column=2, sticky="w")

# Background
bg_image = PhotoImage(file="logo.png")
bg = canvas.create_image(100, 100, image=bg_image)

# Labels
label_style = ttk.Style()
# label_style.configure("TLabel", background=WHITE, font=LABEL_FONT)
# print(label_style.layout("TLabel"))
# print(label_style.element_options("TLabel.label"))

website_label = ttk.Label(window, text="Website: ", style="TLabel")
email_label = ttk.Label(window, text="Email/Username: ", style="TLabel")
password_label = ttk.Label(window, text="Password: ", style="TLabel")

website_label.grid(row=2, column=1, sticky="e")
email_label.grid(row=3, column=1, sticky="e")
password_label.grid(row=4, column=1, sticky="e")

# Inputs
website_entry = Entry(window, width=21)
website_entry.focus()
email_entry = Entry(window, width=21)
email_entry.insert(0, "rjmartin73@outlook.com")
password_entry = Entry(window, width=21)

website_entry.grid(row=2, column=2, columnspan=2, sticky="w", pady=2)
email_entry.grid(row=3, column=2, columnspan=2, sticky="w", pady=2)
password_entry.grid(row=4, column=2, sticky="w", pady=2)

button_style = ttk.Style()
button_style.theme_use("aqua")
button_style.configure("TButton", foreground="black", background=WHITE,
                       relief="raised", font=BUTTON_FONT)
# print(str(button_style.theme_names()))
# Buttons
add_btn_image = PhotoImage(file="icons8-add-48 (1).png")
add_btn_image_sm = add_btn_image.subsample(3, 3)
add_button = ttk.Button(window, text="Add", width=40, image=add_btn_image_sm,
                        compound=LEFT, command=lambda: save_password())
gen_pswd_button = ttk.Button(window, text="Generate Password", command=lambda: create_password())
search_button = ttk.Button(window, text="Search", style="TButton",
                           command=lambda: search())


add_button.grid(row=5, column=2, columnspan=2, sticky="w")
gen_pswd_button.grid(row=4, column=3, sticky="w")
search_button.grid(row=2, column=3, sticky="w")

if __name__ == '__main__':
    window.mainloop()
