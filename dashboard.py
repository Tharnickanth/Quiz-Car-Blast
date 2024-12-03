import tkinter as tk
from PIL import Image, ImageTk
import os
from tkinter import messagebox
import sys
import os
import subprocess
import pygame
pygame.init()
try:
    pygame.mixer.music.load("music/game_bgm.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
except pygame.error as e:
    print(f"Error loading music: {e}")

def play_game():
    root.destroy()
    pygame.quit()
    subprocess.Popen(['python', 'game.py', str(username)])

def view_scorecard():
    root.destroy()
    pygame.quit()
    subprocess.Popen(['python', 'scorecard.py', str(username)])

def logout():
    root.destroy()
    pygame.quit()
    os.system('python login.py')

root = tk.Tk()
root.title("Dashboard")


username = sys.argv[1] 

# Set the window size and center it on the screen
window_width = 800
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
root.resizable(False, False)

# Load the background image
dashboard_image_path = "image/dashboard.jpg"
try:
    dashboard_image = Image.open(dashboard_image_path)
    dashboard_image = dashboard_image.resize((window_width, window_height), Image.Resampling.LANCZOS)
    background_image = ImageTk.PhotoImage(dashboard_image)
    background_label = tk.Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)
except Exception as e:
    tk.messagebox.showerror("Image Error", f"An error occurred loading the dashboard image: {e}")

# Create a frame for the welcome message
welcome_frame = tk.Frame(root, bg="#05031B", padx=10, pady=5)
welcome_frame.place(relx=0.5, rely=0.7, anchor="center")

# Add welcome message
welcome_label = tk.Label(welcome_frame, text=f"Hello {username}....", font=("Helvetica", 16, "bold"), bg="#05031B", fg="white")
welcome_label.grid(row=0, column=0, padx=10)

# Create a frame for the buttons
button_frame = tk.Frame(root, bg="#05031B", padx=10, pady=5)
button_frame.place(relx=0.5, rely=0.8, anchor="center")  # Keep the button frame near the bottom of the window

# Add buttons to the frame
play_button = tk.Button(button_frame, text="Play Game", command=play_game, font=("Helvetica", 12), bg="#4CAF50", fg="white", padx=20, pady=5)
play_button.grid(row=0, column=0, padx=10)

scorecard_button = tk.Button(button_frame, text="Scorecard", command=view_scorecard, font=("Helvetica", 12), bg="#008CBA", fg="white", padx=20, pady=5)
scorecard_button.grid(row=0, column=1, padx=10)

logout_button = tk.Button(button_frame, text="Logout", command=logout, font=("Helvetica", 12), bg="#f44336", fg="white", padx=20, pady=5)
logout_button.grid(row=0, column=2, padx=10)

root.mainloop()
