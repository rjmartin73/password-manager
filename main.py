from tkinter import (Tk, Label, Entry, Button, Canvas, PhotoImage)
from tkinter import messagebox, END
from password_gen import generate_password
import json
import platform
platform = platform.platform()
print(platform)


# CONSTANTS
WHITE = "#FBFCFC"
LABEL_FONT = ("Verdana", 11, "normal")
BUTTON_FONT = ("Verdana", 9, "normal")
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
        data_file = open(filename, method)

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

    data_file = open_file(PSWD_FILE, "r")
    data = get_json_data(data_file)
    data_file.close()

    # for key, value in data.items():
    #     print("Website:", key)
    #     print("Data", value)

    if website in data:
        email = data[website]["email"]
        password = data[website]["password"]

        website_entry.delete(0, END)
        website_entry.insert(0, website.title())

        password_entry.delete(0, END)
        password_entry.insert(0, password)

        email_entry.delete(0, END)
        email_entry.insert(0, email)
    else:
        password_entry.delete(0, END)
        messagebox.showinfo(title="Not Found", message=f"{website.title()} not found.")

# ------------------------------ UI SETUP ---------------------------------- #
# Window
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20, background=WHITE)

# Canvas
canvas = Canvas(window, width=200, height=200, background=WHITE,
                highlightthickness=0, relief="ridge")
canvas.grid(row=1, column=2, sticky="w")

# Background
bg_image = PhotoImage(file="logo.png")
bg = canvas.create_image(100, 100, image=bg_image)

# Labels
website_label = Label(window, text="Website: ", background=WHITE,
                      font=LABEL_FONT)
email_label = Label(window, text="Email/Username: ", background=WHITE,
                    font=LABEL_FONT)
password_label = Label(window, text="Password: ", background=WHITE,
                       font=LABEL_FONT)

website_label.grid(row=2, column=1, sticky="e")
email_label.grid(row=3, column=1, sticky="e")
password_label.grid(row=4, column=1, sticky="e")

# Inputs
website_entry = Entry(window, width=35)
website_entry.focus()
email_entry = Entry(window, width=57)
email_entry.insert(0, "rjmartin73@outlook.com")
password_entry = Entry(window, width=30)

website_entry.grid(row=2, column=2, columnspan=2, sticky="w", pady=2)
email_entry.grid(row=3, column=2, columnspan=2, sticky="w", pady=2)
password_entry.grid(row=4, column=2, sticky="w", pady=2)

# Buttons
add_button = Button(window, text="Add", width=42, pady=2, background=WHITE,
                    font=BUTTON_FONT, command=lambda: save_password())
gen_pswd_button = Button(window, text="Generate Password", pady=2,
                         background=WHITE, font=BUTTON_FONT,
                         command=lambda: create_password())
search_button = Button(window, text="Search", background=WHITE, width=15,
                       font=BUTTON_FONT, command=lambda: search())

add_button.grid(row=5, column=2, columnspan=2, sticky="w")
gen_pswd_button.grid(row=4, column=3, sticky="e")
search_button.grid(row=2, column=3, sticky="e")

if __name__ == '__main__':
    window.mainloop()
