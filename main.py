import math

import pgzrun
import pygame
import random

#### CONFIGURATION ####

WIDTH = 1600
HEIGHT = 800

WALL_THICK = 20  # grubość ścian
WALL_COLOR = (0, 0, 255)
FLOOR_COLOR = (0, 255, 0)

RAY_ANGLE = 30
RAY_COUNT = 100
RAY_PREC = 2

#### VARS ####

walls_list = [
    Rect((0, 0), (WIDTH / 2, WALL_THICK)),  # ściana górna
    Rect((0, 0), (WALL_THICK, HEIGHT)),  # ściana lewa
    Rect((0, HEIGHT - WALL_THICK), (WIDTH / 2, WALL_THICK)),  # ściana dolna
    Rect((WIDTH / 2 - WALL_THICK, 0), (WALL_THICK, HEIGHT)),  # ściana prawa
    Rect((80, 120), (200, WALL_THICK)),
    Rect((250, 420), (WALL_THICK, 320)),
    Rect((620, 150), (WALL_THICK, 280)),
]

ball = {
    "x": WIDTH // 4,
    "y": HEIGHT // 2,
    "radius": 20,
    "color": (255, 0, 0),
    "vx": 5,
    "vy": 2,
    "angle": 0,
}

line_points = []


#### DRAW ####
def draw():
    screen.fill("white")
    draw_walls()
    draw_ball()
    draw_rays()
    draw_3d()


def draw_3d():
    rect_width = (WIDTH / 2) / RAY_COUNT
    max_dist = WIDTH / 2
    for i in range(RAY_COUNT):
        px, py, angle = line_points[i]
        distance = dist(ball["x"], ball["y"], px, py)
        distance = distance * math.cos(math.radians(angle - ball["angle"]))
        rect_height = (1 - (distance / max_dist)) * HEIGHT

        wall_rect = Rect(rect_width * i + WIDTH / 2, (HEIGHT - rect_height) / 2, rect_width, rect_height)
        screen.draw.filled_rect(wall_rect, WALL_COLOR)
        # screen.draw.rect(wall_rect, "black")

        floor_rect = Rect(rect_width * i + WIDTH / 2, max((HEIGHT - rect_height) / 2 + rect_height, HEIGHT / 2),
                          rect_width, (HEIGHT - rect_height) / 2)
        screen.draw.filled_rect(floor_rect, FLOOR_COLOR)
        # screen.draw.rect(floor_rect, "black")


# Rysowanie promieni
def draw_rays():
    for point in line_points:
        px, py, angle = point
        screen.draw.line((ball["x"], ball["y"]), (px, py), "yellow")


# Rysowanie ścian
def draw_walls():
    for wall in walls_list:
        screen.draw.filled_rect(wall, WALL_COLOR)


# Rysowanie piłki
def draw_ball():
    screen.draw.filled_circle((ball["x"], ball["y"]), ball["radius"], ball["color"])


#### UPDATE ####
def update():
    move_ball()
    update_ball()


def move_ball():
    if keyboard.q:
        ball["angle"] -= 1

    if keyboard.e:
        ball["angle"] += 1

    if keyboard.w:
        ball["x"] += math.cos(math.radians(ball["angle"]))
        ball["y"] += math.sin(math.radians(ball["angle"]))

    if keyboard.s:
        ball["x"] -= math.cos(math.radians(ball["angle"]))
        ball["y"] -= math.sin(math.radians(ball["angle"]))


def update_ball():
    line_points.clear()
    angle = ball["angle"] - RAY_ANGLE
    while angle < ball["angle"] + RAY_ANGLE:
        x = ball["x"]
        y = ball["y"]
        while not check_collision(x, y):
            x += math.cos(math.radians(angle)) * RAY_PREC
            y += math.sin(math.radians(angle)) * RAY_PREC

        line_points.append((x, y, angle))

        angle += (RAY_ANGLE * 2) / RAY_COUNT


#### HELPERS ####

# Sprawdzamy, czy punkt na obwodzie piłki jest w kolizji ze ścianą
# mvx i mvy oznaczają przesunięcie środka piłki - w ten sposób otrzymamy punkt na okręgu
def check_collision(x, y):
    for wall in walls_list:
        if wall.collidepoint((x, y)):
            return True
    return False


def dist(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


#### INIT ####
pgzrun.go()
