import pygame
import sys
import os
import random
from datetime import datetime

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 600 #You can increase these to get a bigger drawing area
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Creativity Castle HD Deluxe Edition")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)

drawing_surface = pygame.Surface((WIDTH, HEIGHT - 50))
drawing_surface.fill(WHITE)

pen_color = BLACK
pen_size = 2 #Bigger sizes are bugged currently (the cursor becomes a plus sign and doesn't fill in properly)

undo_history = []
max_undo_steps = 50

stamps_folder = "stamps"
stamps = []
if os.path.exists(stamps_folder):
    for i in range(1, 24):  #This range controls how many stamps can get loaded.
        stamp_path = os.path.join(stamps_folder, f"{i}.png")
        if os.path.exists(stamp_path):
            stamp = pygame.image.load(stamp_path)
            stamps.append(stamp)

pygame.mixer.music.set_volume(0.5)
title_music = "title.wav"
drawing_music_folder = "music"
drawing_music_files = [f for f in os.listdir(drawing_music_folder) if f.endswith(".wav")]

def play_title_music():
    pygame.mixer.music.load(title_music)
    pygame.mixer.music.play(-1)

def play_random_drawing_music():
    if drawing_music_files:
        random_music = random.choice(drawing_music_files)
        pygame.mixer.music.load(os.path.join(drawing_music_folder, random_music))
        pygame.mixer.music.play(-1)

class Button:
    def __init__(self, x, y, width, height, color, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.action = action

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        font = pygame.font.Font(None, 24)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.action()
                return True
        return False

def open_color_menu():
    global pen_color
    colors = [RED, GREEN, BLUE, BLACK, WHITE]
    color_rects = [pygame.Rect(10 + i * 30, HEIGHT - 40, 20, 20) for i in range(len(colors))]
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(color_rects):
                    if rect.collidepoint(event.pos):
                        pen_color = colors[i]
                        return

        screen.fill(WHITE)
        screen.blit(drawing_surface, (0, 0))
        for i, rect in enumerate(color_rects):
            pygame.draw.rect(screen, colors[i], rect)
            pygame.draw.rect(screen, BLACK, rect, 2)
        pygame.display.flip()

def open_size_menu():
    global pen_size
    sizes = [1, 3, 5, 10, 20]
    size_rects = [pygame.Rect(10 + i * 30, HEIGHT - 40, 20, 20) for i in range(len(sizes))]
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(size_rects):
                    if rect.collidepoint(event.pos):
                        pen_size = sizes[i]
                        return

        screen.fill(WHITE)
        screen.blit(drawing_surface, (0, 0))
        for i, rect in enumerate(size_rects):
            pygame.draw.circle(screen, BLACK, rect.center, sizes[i])
            pygame.draw.rect(screen, BLACK, rect, 2)
        pygame.display.flip()

def open_bg_color_menu():
    colors = [RED, GREEN, BLUE, BLACK, WHITE]
    color_rects = [pygame.Rect(10 + i * 30, HEIGHT - 40, 20, 20) for i in range(len(colors))]
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(color_rects):
                    if rect.collidepoint(event.pos):
                        save_undo_state()
                        drawing_surface.fill(colors[i])
                        return

        screen.fill(WHITE)
        screen.blit(drawing_surface, (0, 0))
        for i, rect in enumerate(color_rects):
            pygame.draw.rect(screen, colors[i], rect)
            pygame.draw.rect(screen, BLACK, rect, 2)
        pygame.display.flip()

def open_stamp_menu():
    global stamp
    stamp_rects = [pygame.Rect(10 + i * 70, HEIGHT - 100, 60, 60) for i in range(len(stamps))]
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(stamp_rects):
                    if rect.collidepoint(event.pos):
                        stamp = stamps[i]
                        return
                if event.pos[1] < HEIGHT - 100:
                    stamp = None
                    return

        screen.fill(WHITE)
        screen.blit(drawing_surface, (0, 0))
        for i, stamp in enumerate(stamps):
            screen.blit(pygame.transform.scale(stamp, (60, 60)), stamp_rects[i])
            pygame.draw.rect(screen, BLACK, stamp_rects[i], 2)
        pygame.display.flip()

def undo():
    global drawing_surface
    if undo_history:
        drawing_surface = undo_history.pop()

def clear():
    global drawing_surface
    save_undo_state()
    drawing_surface.fill(WHITE)

def save_undo_state():
    global undo_history
    undo_history.append(drawing_surface.copy())
    if len(undo_history) > max_undo_steps:
        undo_history.pop(0)

def save_picture():
    if not os.path.exists("saved_pictures"):
        os.makedirs("saved_pictures")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"saved_pictures/drawing_{timestamp}.png"
    pygame.image.save(drawing_surface, filename)
    print(f"Picture saved as {filename}")

def show_menu():
    global in_menu
    in_menu = True
    play_title_music()

buttons = [
    Button(10, HEIGHT - 40, 80, 30, LIGHT_GRAY, "Color", open_color_menu),
    Button(100, HEIGHT - 40, 80, 30, LIGHT_GRAY, "Size", open_size_menu),
    Button(190, HEIGHT - 40, 80, 30, LIGHT_GRAY, "Background", open_bg_color_menu),
    Button(280, HEIGHT - 40, 80, 30, LIGHT_GRAY, "Stamps", open_stamp_menu),
    Button(370, HEIGHT - 40, 80, 30, LIGHT_GRAY, "Undo", undo),
    Button(460, HEIGHT - 40, 80, 30, LIGHT_GRAY, "Clear", clear),
    Button(550, HEIGHT - 40, 80, 30, LIGHT_GRAY, "Save", save_picture),
    Button(710, HEIGHT - 40, 80, 30, LIGHT_GRAY, "Menu", show_menu),
]

def draw_line(start, end):
    pygame.draw.line(drawing_surface, pen_color, start, end, pen_size * 2)

def menu_screen():
    global in_menu
    menu_font = pygame.font.Font(None, 36)
    title = menu_font.render("Creativity Castle HD Deluxe Edition", True, BLACK)
    start_text = menu_font.render("Click anywhere to begin", True, BLACK)
    
    while in_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                in_menu = False
                play_random_drawing_music()
        
        screen.fill(WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()

drawing = False
stamp = None
last_pos = None
in_menu = True

play_title_music()

while True:
    if in_menu:
        menu_screen()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if event.pos[1] < HEIGHT - 50:
                    save_undo_state()
                    drawing = True
                    last_pos = event.pos
                    if stamp:
                        drawing_surface.blit(stamp, (event.pos[0] - stamp.get_width() // 2, event.pos[1] - stamp.get_height() // 2))
                    else:
                        pygame.draw.circle(drawing_surface, pen_color, event.pos, pen_size)
                else:
                    for button in buttons:
                        if button.handle_event(event):
                            break
        
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                drawing = False
                last_pos = None
        
        if event.type == pygame.MOUSEMOTION:
            if drawing and not stamp:
                current_pos = event.pos
                if last_pos:
                    draw_line(last_pos, current_pos)
                last_pos = current_pos

    screen.fill(WHITE)
    screen.blit(drawing_surface, (0, 0))
    for button in buttons:
        button.draw(screen)
    
    pygame.draw.line(screen, BLACK, (0, HEIGHT - 50), (WIDTH, HEIGHT - 50), 2)
    
    if stamp:
        x, y = pygame.mouse.get_pos()
        screen.blit(stamp, (x - stamp.get_width() // 2, y - stamp.get_height() // 2))

    pygame.display.flip()
