import os
import pygame


def load_image(name, size=64):
    path = os.path.join('assets', name)
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, (size, size))


def load_duck(name='duck'):
    return {
        'North': load_image(f'{name}_back.png', 68),
        'South': load_image(f'{name}_front.png', 68),
        'West': load_image(f'{name}_left.png', 68),
        'East': load_image(f'{name}_right.png', 68)
    }


def single_assets():
    return {
        'grass': load_image('grass.png'),
        'wall': load_image('wall.png'),
        'goal': load_image('goal.png', 36),
        'box': load_image('box.png'),
        'box_goal': load_image('brown_box.png'),
        'duck': load_duck()
    }


def competitive_assets():
    return {
        'grass': load_image('grass.png'),
        'wall': load_image('wall.png'),
        'goal': load_image('goal.png', 36),
        'box': load_image('box.png'),
        'box1': load_image('blue_box.png'),
        'box2': load_image('pink_box.png'),
        'duck1': load_duck(),
        'duck2': load_duck('duck2')
    }