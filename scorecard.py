import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from PIL import Image, ImageTk
import os
import subprocess
import sys
import pygame
pygame.init()
try:
    pygame.mixer.music.load("music/game_bgm.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
except pygame.error as e:
    print(f"Error loading music: {e}")

username = sys.argv[1]
def back_to_welcome():
    root.destroy()
    pygame.quit()
    subprocess.Popen(['python', 'dashboard.py', str(username)])

root = tk.Tk()
root.title("Scorecard")

# Set the window size and center it on the screen
window_width = 800
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
root.resizable(False, False)

# Create a Canvas widget to display the background image
canvas = tk.Canvas(root, width=window_width, height=window_height)
canvas.place(relx=0, rely=0)  # Fill the entire window

# Load the background image
scorecard_image_path = "image/scorecard.jpg"
try:
    scorecard_image = Image.open(scorecard_image_path)
    scorecard_image = scorecard_image.resize((window_width, window_height), Image.Resampling.LANCZOS)
    background_image = ImageTk.PhotoImage(scorecard_image)
    canvas.create_image(0, 0, image=background_image, anchor="nw")  # Display the image on the canvas
except Exception as e:
    messagebox.showerror("Image Error", f"An error occurred loading the scorecard image: {e}")

# Function to fetch the top 10 scores from the database
def fetch_top_scores():
    try:
        conn = sqlite3.connect('database/users.db')
        cursor = conn.cursor()

        # Query to get top 10 scores
        cursor.execute("SELECT user_id, level, score FROM game_results ORDER BY score DESC LIMIT 10")
        scores = cursor.fetchall()

        conn.close()

        return scores
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred while fetching data: {e}")
        return []

# Create a frame for the table view with background color for contrast
table_frame = tk.Frame(root, bg="#ffffff", bd=10, relief="solid")
table_frame.place(relx=0.5, rely=0.5, anchor="center")  # Centered horizontally and vertically

# Add table headers
columns = ("Rank", "User ID", "Level", "Score")
treeview = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

# Styling the table with padding and font
treeview.grid(row=0, column=0, padx=10, pady=10)

# Configure column headings
treeview.heading("Rank", text="Rank", anchor="center")
treeview.heading("User ID", text="User ID", anchor="center")
treeview.heading("Level", text="Level", anchor="center")
treeview.heading("Score", text="Score", anchor="center")

# Style column widths and padding
treeview.column("Rank", width=50, anchor="center")
treeview.column("User ID", width=150, anchor="center")
treeview.column("Level", width=100, anchor="center")
treeview.column("Score", width=100, anchor="center")

# Add padding inside the cells
treeview.tag_configure('oddrow', background="#f9f9f9")
treeview.tag_configure('evenrow', background="#ffffff")

# Fetch and display top 10 scores
scores = fetch_top_scores()
for idx, score in enumerate(scores, 1):
    # Alternate row color for better readability
    tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
    treeview.insert("", "end", values=(idx, score[0], score[1], score[2]), tags=(tag,))

# Add the "Back to Welcome Page" button with padding and styling
back_button = tk.Button(root, text="Back to Dashboard", command=back_to_welcome, font=("Helvetica", 14), bg="#4CAF50", fg="white", relief="raised", bd=4)
back_button.place(relx=0.5, rely=0.85, anchor="center")  # Positioned below the table

root.mainloop()
