import os
import pygame

from sokoban import Sokoban
from game import Game
from gui import GUI
from competitive import CompetitiveGame, load_competitive_map
from competitive_gui import CompetitiveGUI
from agents.agent1 import Agent1
from agents.agent2 import Agent2
from menu import Menu


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAPS_DIR = os.path.join(BASE_DIR, 'maps')


def get_single_maps():
    return sorted([file for file in os.listdir(MAPS_DIR) if file.endswith('.txt') and file != 'competitive_map.txt'])


def run_solver(menu):
    map_name = menu.select_map(get_single_maps())

    if not map_name:
        return

    try:
        game = Game(Sokoban(os.path.join(MAPS_DIR, map_name)))
        GUI(game).run()
    except Exception as error:
        print('Error:', error)


def run_competitive(menu):
    max_steps = menu.enter_steps()

    if not max_steps:
        return

    try:
        path = os.path.join(MAPS_DIR, 'competitive_map.txt')
        walls, boxes, destinations, agent1, agent2, height, width = load_competitive_map(path)
        game = CompetitiveGame(walls, boxes, destinations, agent1, agent2, max_steps, height, width)
        CompetitiveGUI(game, Agent1(), Agent2()).run()
        
    except Exception as error:
        print('Error:', error)


def main():
    menu = Menu()

    while True:
        choice = menu.main_menu()

        if choice == 'single':
            run_solver(menu)
        elif choice == 'competitive':
            run_competitive(menu)
        else:
            pygame.quit()
            break


if __name__ == '__main__':
    main()