import pygame

from gui.base import BaseGUI
from gui.assets import single_assets
from sokoban import search


class GUI(BaseGUI):
    def __init__(self, game):
        super().__init__()

        self.game = game
        self.algorithm = 'UCS'
        self.direction = 'South'

        board_w = game.sokoban.width * self.cell
        board_h = game.sokoban.height * self.cell

        self.panel_x = self.margin + board_w + 45
        width = self.panel_x + 230
        height = max(board_h + self.margin * 2, 490)

        self.set_screen(width, height, 'Sokoban Solver')

        self.assets = single_assets()

        self.ucs = pygame.Rect(self.panel_x, 105, 85, 42)
        self.astar = pygame.Rect(self.panel_x + 100, 105, 85, 42)
        self.back = pygame.Rect(self.panel_x, 380, 185, 38)

        self.solve('UCS')

    def solve(self, algorithm):
        self.algorithm = algorithm
        self.paused = True

        actions, cost, expanded = search(self.game.sokoban, algorithm == 'A*')
        self.game.set_actions(actions)
        self.direction = 'South'

    def forward(self):
        if self.game.current_step >= len(self.game.actions):
            return

        self.direction = self.game.actions[self.game.current_step]
        self.game.forward()

    def backward(self):
        self.game.backward()

        if self.game.current_step > 0:
            self.direction = self.game.actions[self.game.current_step - 1]
        else:
            self.direction = 'South'

    def draw_board(self):
        s = self.game.sokoban
        a = self.assets

        for row in range(s.height):
            walls = [col for col in range(s.width) if (row, col) in s.walls]

            if not walls:
                continue

            for col in range(min(walls), max(walls) + 1):
                pos = (row, col)
                x, y = self.cell_position(row, col)

                if pos in s.walls:
                    self.screen.blit(a['wall'], (x, y))
                    continue

                self.screen.blit(a['grass'], (x, y))

                if pos in s.goals:
                    self.screen.blit(a['goal'], (x + 14, y + 14))

                if pos in self.game.boxes:
                    box = a['box_goal'] if pos in s.goals else a['box']
                    self.screen.blit(box, (x, y))

        row, col = self.game.agent
        x, y = self.cell_position(row, col)
        self.screen.blit(a['duck'][self.direction], (x - 2, y - 7))

    def draw_panel(self):
        x = self.panel_x

        self.draw_panel_box(pygame.Rect(x - 20, 30, 220, 430))

        self.screen.blit(self.title.render('Sokoban', True, self.text), (x, 50))
        self.screen.blit(self.small.render('ALGORITHM', True, self.muted), (x, 83))

        self.button(self.ucs, 'UCS', self.algorithm == 'UCS')
        self.button(self.astar, 'A*', self.algorithm == 'A*')

        self.screen.blit(self.font.render('Steps', True, self.muted), (x, 180))

        count = f'{self.game.current_step}/{len(self.game.actions)}'
        self.screen.blit(self.title.render(count, True, self.text), (x, 205))

        self.controls(x, 270)
        self.button(self.back, 'Back to Menu')

    def handle_event(self, event):
        if self.handle_controls(event):
            return True

        if event.type != pygame.MOUSEBUTTONDOWN:
            return False

        if self.ucs.collidepoint(event.pos):
            self.solve('UCS')
        elif self.astar.collidepoint(event.pos):
            self.solve('A*')
        elif self.back.collidepoint(event.pos):
            return True

        return False

    def update(self):
        if self.paused:
            return

        now = pygame.time.get_ticks()

        if now - self.last_move >= 500:
            self.forward()
            self.last_move = now

            if self.game.current_step >= len(self.game.actions):
                self.paused = True