import pygame
import requests
from PIL import Image
from io import BytesIO
import math
import tkinter as tk
from tkinter import messagebox
import sys
import sqlite3
import os
import subprocess
pygame.init()

try:
    pygame.mixer.music.load("music/game_music.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
except pygame.error as e:
    print(f"Error loading music: {e}")

width = 1366
height = 768
username = sys.argv[1] 
def get_quiz():
    response = requests.get('https://marcconrad.com/uob/banana/api.php', verify=False)
    if response.status_code == 200:
        data = response.json()
        image_url = data['question']
        answer = data['solution']
        response = requests.get(image_url, verify=False)

        if response.status_code == 200:
            image_data = BytesIO(response.content)
            quiz = pygame.image.load(image_data)
            quiz = pygame.transform.scale(quiz, (440, 240))
            return quiz, answer
        else:
            print(f"Failed to retrieve image: {response.status_code}")
            return None, None
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None, None

def show_popup(level, score):
    root = tk.Tk()
    root.withdraw() 
    result = messagebox.askyesno("Wrong Answer", f"You hit the wrong answer! \nLevel: {level} \nScore: {score} \nDo you want to restart the game?")
    root.destroy()
    return result

def show_time_over_popup(level, score):
    root = tk.Tk()
    root.withdraw()
    result = messagebox.askyesno("Time Over", f"Time is over! \nLevel: {level} \nScore: {score} \nDo you want to restart the game?")
    root.destroy()
    return result

def save_game_result(user_id, level, score):
    conn = sqlite3.connect('database/users.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO game_results (user_id, level, score) VALUES (?, ?, ?)", (user_id, level, score))
    conn.commit()
    conn.close()

window = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()

car_obj = pygame.image.load("car.png")
background_img = pygame.image.load("image/background_4.jpg")

pygame.display.update()
car_size = car_obj.get_size()
print("Car size:", car_size)

pygame.display.set_caption("Quiz Car Blast")
pygame.display.update()

font = pygame.font.Font(None, 56)
text = font.render(f"Hello, {username}...!", True, (255, 255, 255))
text_rect = text.get_rect(topleft=(40, 20))

def car(x, y, z):
    rotated_car_obj = pygame.transform.rotate(car_obj, z)
    new_rect = rotated_car_obj.get_rect(center=car_obj.get_rect(topleft=(x, y)).center)
    window.blit(rotated_car_obj, new_rect.topleft)

def answer_obj(t, x, y):
    square_color = (255, 0, 0)
    square_size = 50
    square_position = (x, y)

    text_color = (255, 255, 255)
    font_size = 24
    font = pygame.font.Font(None, font_size)
    text = t

    pygame.draw.rect(window, square_color, (*square_position, square_size, square_size))
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(square_position[0] + square_size // 2, square_position[1] + square_size // 2))
    window.blit(text_surface, text_rect)

def barrier(w, h, x, y):
    square_color = (254, 221, 0)
    square_position = (x, y)
    pygame.draw.rect(window, square_color, (*square_position, w, h))

def dashboard_info(level, score, timer):
    font_1 = pygame.font.Font(None, 36)
    level_text = font_1.render(f"Level : {level}", True, (255, 255, 255))
    score_text = font_1.render(f"Score : {score}", True, (255, 255, 255))
    question_text = font_1.render(f"Question :", True, (255, 255, 255))
    question_p1 = font_1.render(f"Find the number behind the banana,", True, (255, 255, 255))
    question_p2 = font_1.render(f"and hit that number with a car....? ", True, (255, 255, 255))
    timer_text = font_1.render(f"Time Left: {int(timer) // 60}:{int(timer) % 60:02d}", True, (255, 255, 255))
    level_rect = level_text.get_rect(topleft=(40, 75))
    score_rect = score_text.get_rect(topleft=(40, 100))
    question_rect = question_text.get_rect(topleft=(40, 425))
    question_p1_rect = question_p1.get_rect(topleft=(40, 475))
    question_p2_rect = question_p2.get_rect(topleft=(40, 500))
    timer_rect = timer_text.get_rect(topleft=(40, 550))
    window.blit(level_text, level_rect)
    window.blit(score_text, score_rect)
    window.blit(question_text, question_rect)
    window.blit(question_p1, question_p1_rect)
    window.blit(question_p2, question_p2_rect)
    window.blit(timer_text, timer_rect)

def get_answer(x, y):
    if ((x > 640) and (x < 720)) and ((y > 10) and (y < 90)):
        return 1
    elif ((x > 940) and (x < 1220)) and ((y > 10) and (y < 90)):
        return 2
    elif ((x > 1240) and (x < 1320)) and ((y > 10) and (y < 90)):
        return 3
    elif ((x > 1240) and (x < 1320)) and ((y > 210) and (y < 290)):
        return 4
    elif ((x > 1240) and (x < 1320)) and ((y > 460) and (y < 540)):
        return 5
    elif ((x > 1230) and (x < 1270)) and ((y > 600) and (y < 640)):
        return 6
    elif ((x > 940) and (x < 1020)) and ((y > 600) and (y < 660)):
        return 7
    elif ((x > 640) and (x < 720)) and ((y > 600) and (y < 660)):
        return 8
    elif ((x > 640) and (x < 720)) and ((y > 460) and (y < 540)):
        return 9
    elif ((x > 640) and (x < 720)) and ((y > 210) and (y < 290)):
        return 0
    return None

def reset_game():
    global x, y, z, x_value, y_value, z_value, speed, level, score, quiz, correct_answer, timer
    x = width // 1.4
    y = height // 2
    z = 0
    x_value = 0
    y_value = 0
    z_value = 0
    speed = 5
    level = 1
    score = 0
    timer = 120 
    quiz, correct_answer = get_quiz()

def reset_car_position():
    global x, y, z, x_value, y_value, z_value
    x = width // 1.4
    y = height // 2
    z = 0
    x_value = 0
    y_value = 0
    z_value = 0

if len(sys.argv) > 1:
    user_id = sys.argv[1]
    print(f"User ID: {user_id}")
else:
    user_id = None
    print("No User ID provided")

running = True
reset_game()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                z_value = -2
            if event.key == pygame.K_RIGHT:
                z_value = 2
            if event.key == pygame.K_UP:
                y_value = speed
            if event.key == pygame.K_DOWN:
                y_value = -speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                z_value = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                y_value = 0

    z -= z_value
    x += y_value * math.sin(math.radians(-z))
    y -= y_value * math.cos(math.radians(-z))

    if x < width // 2 - car_size[0]:
        x = width // 2 - car_size[0]
    elif x > 1280:
        x = 1280

    if y < 0:
        y = 0
    elif y > height - car_size[1]:
        y = height - car_size[1]

    window.blit(background_img, (0, 0)) 

    window.blit(text, text_rect)
    dashboard_info(level, score, timer)
    barrier(25, 800, 560, 0)
    answer_obj('1', 680, 50)
    answer_obj('2', 980, 50)
    answer_obj('3', 1280, 50)
    answer_obj('4', 1280, 250)
    answer_obj('5', 1280, 500)
    answer_obj('6', 1280, 700)
    answer_obj('7', 980, 700)
    answer_obj('8', 680, 700)
    answer_obj('9', 680, 500)
    answer_obj('0', 680, 250)

    if quiz:
        window.blit(quiz, (40, 150))

    car(x, y, z)

    ans_hit = get_answer(x, y)

    if ans_hit is not None:
        if ans_hit == correct_answer:
            level += 1
            score += 100
            timer += 10 
            quiz, correct_answer = get_quiz()
            reset_car_position()
        else:
            save_game_result(user_id, level, score)
            if show_popup(level, score):
                reset_game()
            else:
                running = False

    # Update the timer
    timer -= 1 / 60 
    if timer <= 0:
        save_game_result(user_id, level, score)
        if show_time_over_popup(level, score):
            reset_game()
        else:
            
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
subprocess.Popen(['python', 'dashboard.py', str(username)])