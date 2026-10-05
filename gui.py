import os
import pygame

from sokoban import search


class GUI:
    def __init__(self, game):
        pygame.init()

        self.game = game
        self.cell = 64
        self.margin = 32
        self.algorithm = 'UCS'
        self.paused = True
        self.direction = 'South'
        self.last_move = 0

        board_w = game.sokoban.width * self.cell
        board_h = game.sokoban.height * self.cell

        self.panel_x = self.margin + board_w + 45
        width = self.panel_x + 230
        height = max(board_h + self.margin * 2, 490)

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Sokoban Solver')

        self.font = pygame.font.SysFont('Arial', 18)
        self.small = pygame.font.SysFont('Arial', 15)
        self.title = pygame.font.SysFont('Arial', 27, bold=True)
        self.clock = pygame.time.Clock()

        self.grass = self.load('grass.png')
        self.wall = self.load('wall.png')
        self.goal = self.load('goal.png', 36)
        self.box = self.load('box.png')
        self.box_goal = self.load('brown_box.png')

        self.duck = {
            'North': self.load('duck_back.png', 68),
            'South': self.load('duck_front.png', 68),
            'West': self.load('duck_left.png', 68),
            'East': self.load('duck_right.png', 68)
        }

        self.ucs = pygame.Rect(self.panel_x, 105, 85, 42)
        self.astar = pygame.Rect(self.panel_x + 100, 105, 85, 42)
        self.back = pygame.Rect(self.panel_x, 380, 185, 38)

        self.solve('UCS')

    def load(self, name, size=64):
        path = os.path.join('assets', name)
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, (size, size))

    def solve(self, algorithm):
        self.algorithm = algorithm
        self.paused = True
        actions, cost, expanded = search(self.game.sokoban, algorithm == 'A*')
        self.game.set_actions(actions)
        self.direction = 'South'

    def forward(self):
        if self.game.current_step < len(self.game.actions):
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

        for row in range(s.height):
            walls = [col for col in range(s.width) if (row, col) in s.walls]

            if not walls:
                continue

            for col in range(min(walls), max(walls) + 1):
                pos = (row, col)
                x = self.margin + col * self.cell
                y = self.margin + row * self.cell

                if pos in s.walls:
                    self.screen.blit(self.wall, (x, y))
                else:
                    self.screen.blit(self.grass, (x, y))

                    if pos in s.goals:
                        self.screen.blit(self.goal, (x + 14, y + 14))

                    if pos in self.game.boxes:
                        image = self.box_goal if pos in s.goals else self.box
                        self.screen.blit(image, (x, y))

        row, col = self.game.agent
        x = self.margin + col * self.cell
        y = self.margin + row * self.cell
        self.screen.blit(self.duck[self.direction], (x - 2, y - 7))

    def button(self, rect, text, selected=False):
        hover = rect.collidepoint(pygame.mouse.get_pos())

        if selected or hover:
            color = (86, 157, 164)
            text_color = (255, 255, 255)
        else:
            color = (213, 235, 234)
            text_color = (45, 82, 87)

        pygame.draw.rect(self.screen, color, rect, border_radius=8)
        pygame.draw.rect(self.screen, (160, 202, 201), rect, 2, border_radius=8)

        label = self.font.render(text, True, text_color)
        self.screen.blit(label, label.get_rect(center=rect.center))

    def draw_panel(self):
        x = self.panel_x
        panel = pygame.Rect(x - 20, 30, 220, 430)

        pygame.draw.rect(self.screen, (248, 252, 250), panel, border_radius=14)
        pygame.draw.rect(self.screen, (160, 202, 201), panel, 2, border_radius=14)

        self.screen.blit(self.title.render('Sokoban', True, (45, 82, 87)), (x, 50))
        self.screen.blit(self.small.render('ALGORITHM', True, (103, 139, 141)), (x, 83))

        self.button(self.ucs, 'UCS', self.algorithm == 'UCS')
        self.button(self.astar, 'A*', self.algorithm == 'A*')

        self.screen.blit(self.font.render('Actions', True, (103, 139, 141)), (x, 180))

        count = f'{self.game.current_step}/{len(self.game.actions)}'
        self.screen.blit(self.title.render(count, True, (45, 82, 87)), (x, 205))

        controls = [('SPACE', 'Play / Pause'), ('RIGHT', 'Forward'), ('LEFT', 'Backward')]

        for i, (key, text) in enumerate(controls):
            y = 270 + i * 26
            self.screen.blit(self.small.render(key, True, (45, 82, 87)), (x, y))
            self.screen.blit(self.small.render(text, True, (103, 139, 141)), (x + 70, y))

        self.button(self.back, 'Back to Menu')

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.paused = not self.paused
            elif event.key == pygame.K_RIGHT:
                self.paused = True
                self.forward()
            elif event.key == pygame.K_LEFT:
                self.paused = True
                self.backward()
            elif event.key == pygame.K_ESCAPE:
                return True

        if event.type == pygame.MOUSEBUTTONDOWN:
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

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                if self.handle_event(event):
                    return

            self.update()

            self.screen.fill((225, 242, 240))
            self.draw_board()
            self.draw_panel()

            pygame.display.flip()
            self.clock.tick(60)