import pygame

from sokoban import search


class GUI:
    def __init__(self, game):
        pygame.init()

        self.game = game
        self.algorithm = 'UCS'
        self.paused = True

        self.cell = 64
        self.margin = 32

        self.board_width = self.game.sokoban.width * self.cell
        self.panel_x = self.board_width + 80

        width = self.panel_x + 250
        height = max(self.game.sokoban.height * self.cell + 64, 490)

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Sokoban Solver')

        self.font = pygame.font.SysFont('Arial', 18)
        self.small_font = pygame.font.SysFont('Arial', 15)
        self.title_font = pygame.font.SysFont('Arial', 27, bold=True)
        self.clock = pygame.time.Clock()

        button_width = 85
        button_gap = 15

        self.ucs_button = pygame.Rect(self.panel_x, 105, button_width, 42)
        self.astar_button = pygame.Rect(self.panel_x + button_width + button_gap, 105, button_width, 42)
        self.back_button = pygame.Rect(self.panel_x, 380, 185, 38)

        self.last_move = 0
        self.solve('UCS')

    def solve(self, algorithm):
        self.algorithm = algorithm
        self.paused = True

        actions, _, _ = search(self.game.sokoban, algorithm == 'A*')
        self.game.set_actions(actions)

    def draw_floor(self, rect):
        pygame.draw.rect(self.screen, (244, 230, 195), rect)
        pygame.draw.line(self.screen, (235, 216, 176), (rect.left + 8, rect.top + 15), (rect.left + 18, rect.top + 15), 2)
        pygame.draw.line(self.screen, (235, 216, 176), (rect.right - 20, rect.bottom - 15), (rect.right - 10, rect.bottom - 15), 2)

    def draw_wall(self, rect):
        base = (151, 143, 87)
        line = (92, 87, 57)

        pygame.draw.rect(self.screen, base, rect)

        h = self.cell // 3
        left = rect.left + 1
        right = rect.right - 1
        top = rect.top + 1
        bottom = rect.bottom - 1

        pygame.draw.line(self.screen, line, (left, rect.top + h), (right, rect.top + h), 2)
        pygame.draw.line(self.screen, line, (left, rect.top + h * 2), (right, rect.top + h * 2), 2)
        pygame.draw.line(self.screen, line, (rect.centerx, top), (rect.centerx, rect.top + h), 2)
        pygame.draw.line(self.screen, line, (rect.left + self.cell // 4, rect.top + h), (rect.left + self.cell // 4, rect.top + h * 2), 2)
        pygame.draw.line(self.screen, line, (rect.centerx, rect.top + h * 2), (rect.centerx, bottom), 2)
        pygame.draw.rect(self.screen, line, rect, 2)

    def draw_goal(self, rect):
        pygame.draw.circle(self.screen, (218, 142, 132), rect.center, 12)
        pygame.draw.circle(self.screen, (235, 174, 160), rect.center, 7)

    def draw_box(self, rect, completed=False):
        x = rect.left
        y = rect.top
        s = self.cell // 8

        if completed:
            box = (151, 91, 47)
            top = (176, 111, 57)
            border = (92, 57, 34)
            tape = (205, 155, 94)
        else:
            box = (211, 151, 81)
            top = (230, 174, 101)
            border = (125, 81, 44)
            tape = (242, 207, 145)

        pygame.draw.rect(self.screen, border, (x + s, y + s, s * 6, s * 6))
        pygame.draw.rect(self.screen, box, (x + s + 3, y + s + 3, s * 6 - 6, s * 6 - 6))
        pygame.draw.rect(self.screen, top, (x + s + 3, y + s + 3, s * 6 - 6, s * 2))
        pygame.draw.rect(self.screen, tape, (x + s * 3, y + s + 3, s * 2, s * 6 - 6))

    def draw_agent(self, rect):
        x = rect.left
        y = rect.top
        s = self.cell // 8

        orange = (242, 158, 69)
        light = (255, 181, 91)
        shadow = (218, 122, 42)
        cream = (255, 239, 205)
        dark = (67, 55, 45)
        collar = (181, 59, 77)

        pygame.draw.rect(self.screen, orange, (x + s * 2, y + s * 4, s * 4, s * 3))

        pygame.draw.rect(self.screen, light, (x + s * 2, y + s, s * 4, s * 4))
        pygame.draw.rect(self.screen, light, (x + s * 2, y, s, s * 2))
        pygame.draw.rect(self.screen, light, (x + s * 5, y, s, s * 2))

        pygame.draw.rect(self.screen, shadow, (x + s * 2, y, s, s))
        pygame.draw.rect(self.screen, shadow, (x + s * 5, y, s, s))

        pygame.draw.rect(self.screen, cream, (x + s * 2, y + s * 3, s * 4, s))

        pygame.draw.rect(self.screen, dark, (x + s * 3, y + s * 2, s, s))
        pygame.draw.rect(self.screen, dark, (x + s * 5, y + s * 2, s, s))

        pygame.draw.rect(self.screen, collar, (x + s * 2, y + s * 4, s * 4, s // 2))

        pygame.draw.rect(self.screen, orange, (x + s * 6, y + s * 4, s, s * 3))
        pygame.draw.rect(self.screen, orange, (x + s * 7, y + s * 3, s, s * 2))
        pygame.draw.rect(self.screen, shadow, (x + s * 7, y + s * 3, s, s))

    def draw_board(self):
        sokoban = self.game.sokoban

        for row in range(sokoban.height):
            wall_cols = [col for col in range(sokoban.width) if (row, col) in sokoban.walls]

            if not wall_cols:
                continue

            left = min(wall_cols)
            right = max(wall_cols)

            for col in range(left, right + 1):
                position = (row, col)
                rect = pygame.Rect(self.margin + col * self.cell, self.margin + row * self.cell, self.cell, self.cell)

                if position in sokoban.walls:
                    self.draw_wall(rect)
                    continue

                self.draw_floor(rect)

                if position in sokoban.goals:
                    self.draw_goal(rect)

                if position in self.game.boxes:
                    self.draw_box(rect, position in sokoban.goals)

                if position == self.game.agent:
                    self.draw_agent(rect)

    def draw_button(self, rect, text, selected=False):
        hover = rect.collidepoint(pygame.mouse.get_pos())

        if selected or hover:
            color = (128, 96, 65)
            text_color = (255, 250, 235)
        else:
            color = (218, 201, 166)
            text_color = (91, 75, 57)

        pygame.draw.rect(self.screen, color, rect, border_radius=7)
        pygame.draw.rect(self.screen, (137, 113, 81), rect, 2, border_radius=7)

        text_surface = self.font.render(text, True, text_color)
        self.screen.blit(text_surface, text_surface.get_rect(center=rect.center))

    def draw_panel(self):
        x = self.panel_x
        panel = pygame.Rect(x - 20, 30, 220, 430)

        pygame.draw.rect(self.screen, (247, 238, 216), panel, border_radius=12)
        pygame.draw.rect(self.screen, (186, 164, 124), panel, 2, border_radius=12)

        title = self.title_font.render('Sokoban', True, (75, 61, 47))
        self.screen.blit(title, (x, 50))

        label = self.small_font.render('ALGORITHM', True, (139, 116, 83))
        self.screen.blit(label, (x, 83))

        self.draw_button(self.ucs_button, 'UCS', self.algorithm == 'UCS')
        self.draw_button(self.astar_button, 'A*', self.algorithm == 'A*')

        actions = self.font.render('Actions', True, (112, 91, 65))
        actions_value = self.title_font.render(f'{self.game.current_step}/{len(self.game.actions)}', True, (75, 61, 47))

        self.screen.blit(actions, (x, 180))
        self.screen.blit(actions_value, (x, 205))

        pygame.draw.line(self.screen, (211, 193, 157), (x, 250), (x + 180, 250), 1)

        controls = [
            ('SPACE', 'Play / Pause'),
            ('RIGHT', 'Forward'),
            ('LEFT', 'Backward')
        ]

        y = 270

        for key, action in controls:
            key_text = self.small_font.render(key, True, (94, 74, 55))
            action_text = self.small_font.render(action, True, (139, 116, 83))

            self.screen.blit(key_text, (x, y))
            self.screen.blit(action_text, (x + 70, y))
            y += 26

        self.draw_button(self.back_button, 'Back to Menu')

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.paused = not self.paused

            elif event.key == pygame.K_RIGHT:
                self.paused = True
                self.game.forward()

            elif event.key == pygame.K_LEFT:
                self.paused = True
                self.game.backward()

            elif event.key == pygame.K_ESCAPE:
                return 'back'

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.ucs_button.collidepoint(event.pos):
                self.solve('UCS')

            elif self.astar_button.collidepoint(event.pos):
                self.solve('A*')

            elif self.back_button.collidepoint(event.pos):
                return 'back'

        return None

    def update(self):
        if self.paused:
            return

        now = pygame.time.get_ticks()

        if now - self.last_move >= 500:
            if self.game.current_step < len(self.game.actions):
                self.game.forward()
            else:
                self.paused = True

            self.last_move = now

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                if self.handle_event(event) == 'back':
                    return

            self.update()

            self.screen.fill((226, 215, 185))
            self.draw_board()
            self.draw_panel()

            pygame.display.flip()
            self.clock.tick(60)