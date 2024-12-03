import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import os
import subprocess
import hashlib

import pygame
pygame.init()
try:
    pygame.mixer.music.load("music/game_bgm.mp3")
    pygame.mixer.music.set_volume(0.5)  
    pygame.mixer.music.play(-1)  
except pygame.error as e:
    print(f"Error loading music: {e}")


def open_registration():
    root.destroy()
    pygame.quit()
    os.system('python registration.py')

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login():
    username = entry_username.get()
    password = entry_password.get()
    

    try:
        conn = sqlite3.connect('database/users.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()

        conn.close()

        if user:
            user_id = f"{user[2]} {user[1][0]}"
            messagebox.showinfo("Login Successful", "Welcome, " + username + "!")
            root.destroy()
            pygame.quit()
            subprocess.Popen(['python', 'dashboard.py', str(user_id)])
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

root = tk.Tk()
root.title("Login")

# Set the window size and center it on the screen
window_width = 400
window_height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
root.configure(bg="#ffffff")

# Create a frame to center all content
center_frame = tk.Frame(root, bg="#ffffff")
center_frame.pack(expand=True)

# Add a logo image using PIL
logo_path = "logo1.jpg"
try:
    logo_image = Image.open(logo_path)
    logo_image = logo_image.resize((200, 200), Image.Resampling.LANCZOS)  # Resize the image if needed
    logo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(center_frame, image=logo, bg="#f0f0f0")
    logo_label.grid(row=0, column=0, columnspan=2, pady=10)
except Exception as e:
    print(e)
    messagebox.showerror("Image Error", f"An error occurred loading the logo image: {e}")

# Add username and password labels and entry fields
tk.Label(center_frame, text="Username", font=("Helvetica", 12), bg="#ffffff").grid(row=1, column=0, pady=10, padx=10, sticky="e")
tk.Label(center_frame, text="Password", font=("Helvetica", 12), bg="#ffffff").grid(row=2, column=0, pady=10, padx=10, sticky="e")

entry_username = tk.Entry(center_frame, font=("Helvetica", 12))
entry_password = tk.Entry(center_frame, show="*", font=("Helvetica", 12))

entry_username.grid(row=1, column=1, pady=10, padx=10)
entry_password.grid(row=2, column=1, pady=10, padx=10)

# Add login button
login_button = tk.Button(center_frame, text="Login", command=login, font=("Helvetica", 12), bg="#4CAF50", fg="white")
login_button.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

# Add the "If you don't have an account" text
tk.Label(center_frame, text="If you don't have an account", font=("Helvetica", 10), bg="#ffffff").grid(row=4, column=0, columnspan=2, pady=(10, 0))


register_button = tk.Button(center_frame, text="Register", command=open_registration, font=("Helvetica", 12), bg="#008CBA", fg="white")
register_button.grid(row=5, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

root.mainloop()
