import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import os
import pygame
pygame.init()
try:
    pygame.mixer.music.load("music/game_bgm.mp3")
    pygame.mixer.music.set_volume(0.5)  
    pygame.mixer.music.play(-1)
except pygame.error as e:
    print(f"Error loading music: {e}")

def register():
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    username = entry_username.get()
    password = entry_password.get()
    confirm_password = entry_confirm_password.get()

    if not first_name or not last_name or not username or not password or not confirm_password:
        messagebox.showerror("Error", "Please fill in all fields")
        return

    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match")
        return

    conn = sqlite3.connect('database/users.db')
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()

    if user:
        messagebox.showerror("Error", "Username already exists")
    else:
        cursor.execute("INSERT INTO users (first_name, last_name, username, password) VALUES (?, ?, ?, ?)",
                       (first_name, last_name, username, password))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful")
        root.destroy()
        pygame.quit()
        os.system('python login.py')

    conn.close()

def go_to_login():
    root.destroy()
    pygame.quit()
    os.system('python login.py')

root = tk.Tk()
root.title("Register")


window_width = 400
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
root.configure(bg="#f0f0f0")


frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20)
frame.place(relx=0.5, rely=0.5, anchor="center")

# Add a logo at the top
logo_path = "logo1.jpg"  
try:
    logo_image = Image.open(logo_path)
    logo_image = logo_image.resize((200, 200), Image.Resampling.LANCZOS)  # Resize the image if needed
    logo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(frame, image=logo, bg="#ffffff")
    logo_label.grid(row=0, column=0, columnspan=2, pady=10)
except Exception as e:
    print(e)
    messagebox.showerror("Image Error", f"An error occurred loading the logo image: {e}")

# Add a title label
title_label = tk.Label(frame, text="Register", font=("Helvetica", 16, "bold"), bg="#ffffff")
title_label.grid(row=1, column=0, columnspan=2, pady=10)

# Add first name, last name, username, password, and confirm password labels and entry fields
tk.Label(frame, text="First Name", font=("Helvetica", 12), bg="#ffffff").grid(row=2, column=0, pady=5, padx=10, sticky="e")
tk.Label(frame, text="Last Name", font=("Helvetica", 12), bg="#ffffff").grid(row=3, column=0, pady=5, padx=10, sticky="e")
tk.Label(frame, text="Username", font=("Helvetica", 12), bg="#ffffff").grid(row=4, column=0, pady=5, padx=10, sticky="e")
tk.Label(frame, text="Password", font=("Helvetica", 12), bg="#ffffff").grid(row=5, column=0, pady=5, padx=10, sticky="e")
tk.Label(frame, text="Confirm Password", font=("Helvetica", 12), bg="#ffffff").grid(row=6, column=0, pady=5, padx=10, sticky="e")

entry_first_name = tk.Entry(frame, font=("Helvetica", 12))
entry_last_name = tk.Entry(frame, font=("Helvetica", 12))
entry_username = tk.Entry(frame, font=("Helvetica", 12))
entry_password = tk.Entry(frame, show="*", font=("Helvetica", 12))
entry_confirm_password = tk.Entry(frame, show="*", font=("Helvetica", 12))

entry_first_name.grid(row=2, column=1, pady=5, padx=10)
entry_last_name.grid(row=3, column=1, pady=5, padx=10)
entry_username.grid(row=4, column=1, pady=5, padx=10)
entry_password.grid(row=5, column=1, pady=5, padx=10)
entry_confirm_password.grid(row=6, column=1, pady=5, padx=10)

# Add register button
register_button = tk.Button(frame, text="Register", command=register, font=("Helvetica", 12), bg="#4CAF50", fg="white")
register_button.grid(row=7, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

# Add a label above the login button
login_prompt = tk.Label(frame, text="If you already have an account", font=("Helvetica", 10), bg="#ffffff")
login_prompt.grid(row=8, column=0, columnspan=2, pady=5)

# Add login button below the register button
login_button = tk.Button(frame, text="Login", command=go_to_login, font=("Helvetica", 12), bg="#008CBA", fg="white")
login_button.grid(row=9, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

root.mainloop()
