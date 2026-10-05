import os
import pygame


class CompetitiveGUI:
    def __init__(self, game, agent1, agent2):
        pygame.init()

        self.game = game
        self.agent1 = agent1
        self.agent2 = agent2

        self.cell = 64
        self.margin = 32
        self.rows = max(row for row, col in game.walls) + 1
        self.cols = max(col for row, col in game.walls) + 1

        board_width = self.cols * self.cell
        board_height = self.rows * self.cell

        self.panel_x = self.margin + board_width + 45
        width = self.panel_x + 230
        height = max(board_height + self.margin * 2, 630)

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Competitive Sokoban')

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 18)
        self.small = pygame.font.SysFont('Arial', 15)
        self.title = pygame.font.SysFont('Arial', 27, bold=True)

        self.grass = self.load('grass.png')
        self.wall = self.load('wall.png')
        self.goal = self.load('goal.png', 36)
        self.box = self.load('box.png')
        self.box1 = self.load('blue_box.png')
        self.box2 = self.load('pink_box.png')

        self.duck1 = {
            'North': self.load('duck_back.png', 68),
            'South': self.load('duck_front.png', 68),
            'West': self.load('duck_left.png', 68),
            'East': self.load('duck_right.png', 68)
        }

        self.duck2 = {
            'North': self.load('duck2_back.png', 68),
            'South': self.load('duck2_front.png', 68),
            'West': self.load('duck2_left.png', 68),
            'East': self.load('duck2_right.png', 68)
        }

        self.direction1 = 'South'
        self.direction2 = 'South'
        self.last_action1 = 'Stay'
        self.last_action2 = 'Stay'
        self.last_step_time = 0
        self.step_interval = 1000

        self.back = pygame.Rect(self.panel_x, 555, 185, 38)

    def load(self, name, size=64):
        path = os.path.join('assets', name)
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, (size, size))

    def draw_board(self):
        for row in range(self.rows):
            walls = [col for col in range(self.cols) if (row, col) in self.game.walls]

            if not walls:
                continue

            for col in range(min(walls), max(walls) + 1):
                pos = (row, col)
                x = self.margin + col * self.cell
                y = self.margin + row * self.cell

                if pos in self.game.walls:
                    self.screen.blit(self.wall, (x, y))
                    continue

                self.screen.blit(self.grass, (x, y))

                if pos in self.game.destinations:
                    self.screen.blit(self.goal, (x + 14, y + 14))

                if pos in self.game.boxes:
                    owner = self.game.box_owner.get(pos)

                    if owner == 1:
                        image = self.box1
                    elif owner == 2:
                        image = self.box2
                    else:
                        image = self.box

                    self.screen.blit(image, (x, y))

        self.draw_agent(self.game.agent1, self.duck1, self.direction1)
        self.draw_agent(self.game.agent2, self.duck2, self.direction2)

    def draw_agent(self, position, images, direction):
        row, col = position
        x = self.margin + col * self.cell
        y = self.margin + row * self.cell
        self.screen.blit(images[direction], (x - 2, y - 7))

    def draw_button(self):
        hover = self.back.collidepoint(pygame.mouse.get_pos())

        if hover:
            color = (86, 157, 164)
            text_color = (255, 255, 255)
        else:
            color = (213, 235, 234)
            text_color = (45, 82, 87)

        pygame.draw.rect(self.screen, color, self.back, border_radius=8)
        pygame.draw.rect(self.screen, (160, 202, 201), self.back, 2, border_radius=8)

        text = self.font.render('Back to Menu', True, text_color)
        self.screen.blit(text, text.get_rect(center=self.back.center))

    def draw_panel(self):
        x = self.panel_x
        panel = pygame.Rect(x - 20, 30, 220, 585)

        pygame.draw.rect(self.screen, (248, 252, 250), panel, border_radius=14)
        pygame.draw.rect(self.screen, (160, 202, 201), panel, 2, border_radius=14)

        self.screen.blit(self.title.render('Competitive', True, (45, 82, 87)), (x, 50))
        self.screen.blit(self.title.render('Sokoban', True, (45, 82, 87)), (x, 82))

        score1, score2 = self.game.get_score()

        self.screen.blit(self.small.render('SCORE', True, (103, 139, 141)), (x, 135))
        self.screen.blit(self.font.render(f'Agent 1: {score1}', True, (75, 125, 180)), (x, 165))
        self.screen.blit(self.font.render(f'Agent 2: {score2}', True, (190, 100, 130)), (x, 195))

        step = f'Step: {self.game.current_step}/{self.game.max_steps}'
        self.screen.blit(self.font.render(step, True, (45, 82, 87)), (x, 250))

        status = 'FINISHED' if self.game.is_finished() else 'RUNNING'
        self.screen.blit(self.small.render(f'Status: {status}', True, (103, 139, 141)), (x, 280))

        self.screen.blit(self.small.render('LAST ACTIONS', True, (103, 139, 141)), (x, 330))
        self.screen.blit(self.small.render(f'Agent 1: {self.last_action1}', True, (45, 82, 87)), (x, 360))
        self.screen.blit(self.small.render(f'Decision: {self.agent1.last_decision_time:.4f}s', True, (103, 139, 141)), (x, 382))

        self.screen.blit(self.small.render(f'Agent 2: {self.last_action2}', True, (45, 82, 87)), (x, 420))
        self.screen.blit(self.small.render(f'Decision: {self.agent2.last_decision_time:.4f}s', True, (103, 139, 141)), (x, 442))

        if self.game.is_finished():
            self.screen.blit(self.small.render('GAME OVER', True, (103, 139, 141)), (x, 490))
            self.screen.blit(self.font.render(self.game.get_winner(), True, (45, 82, 87)), (x, 515))

        self.draw_button()

    def run_ai_step(self):
        action1 = self.agent1.choose_action(self.game)
        action2 = self.agent2.choose_action(self.game)

        if action1 is None:
            action1 = 'Stay'

        if action2 is None:
            action2 = 'Stay'

        self.last_action1 = action1
        self.last_action2 = action2

        if action1 != 'Stay':
            self.direction1 = action1

        if action2 != 'Stay':
            self.direction2 = action2

        self.agent1.last_action = action1
        self.agent2.last_action = action2

        self.game.step(action1, action2)

    def draw(self):
        self.screen.fill((225, 242, 240))
        self.draw_board()
        self.draw_panel()
        pygame.display.flip()

    def run(self):
        self.last_step_time = pygame.time.get_ticks()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.back.collidepoint(event.pos):
                        return

            now = pygame.time.get_ticks()

            if now - self.last_step_time >= self.step_interval:
                if not self.game.is_finished():
                    self.run_ai_step()

                self.last_step_time = now

            self.draw()
            self.clock.tick(60)