import pygame

from gui.base import BaseGUI
from gui.assets import competitive_assets


class CompetitiveGUI(BaseGUI):
    def __init__(self, game, agent1, agent2):
        super().__init__()

        self.game = game
        self.agent1 = agent1
        self.agent2 = agent2

        self.action_history = []
        self.action_step = 0

        self.rows = max(row for row, col in game.walls) + 1
        self.cols = max(col for row, col in game.walls) + 1

        board_w = self.cols * self.cell
        board_h = self.rows * self.cell

        self.panel_x = self.margin + board_w + 45
        width = self.panel_x + 230
        height = max(board_h + self.margin * 2, 590)

        self.set_screen(width, height, 'Competitive Sokoban')

        self.assets = competitive_assets()
        self.back = pygame.Rect(self.panel_x, 500, 185, 38)

    def forward(self):
        if self.game.is_finished():
            return

        if self.action_step < len(self.action_history):
            action1, action2 = self.action_history[self.action_step]
        else:
            action1 = self.agent1.choose_action(self.game) or 'Stay'
            action2 = self.agent2.choose_action(self.game) or 'Stay'
            self.action_history.append((action1, action2))

        self.game.step(action1, action2)
        self.action_step += 1

    def backward(self):
        if self.game.current_step == 0:
            return

        self.game.backward()
        self.action_step -= 1

    def draw_board(self):
        a = self.assets

        for row in range(self.rows):
            walls = [col for col in range(self.cols) if (row, col) in self.game.walls]

            if not walls:
                continue

            for col in range(min(walls), max(walls) + 1):
                pos = (row, col)
                x, y = self.cell_position(row, col)

                if pos in self.game.walls:
                    self.screen.blit(a['wall'], (x, y))
                    continue

                self.screen.blit(a['grass'], (x, y))

                if pos in self.game.destinations:
                    self.screen.blit(a['goal'], (x + 14, y + 14))

                if pos in self.game.boxes:
                    owner = self.game.box_owner.get(pos)

                    if owner == 1:
                        box = a['box1']
                    elif owner == 2:
                        box = a['box2']
                    else:
                        box = a['box']

                    self.screen.blit(box, (x, y))

        self.draw_agent(self.game.agent1, a['duck1'], self.game.direction1)
        self.draw_agent(self.game.agent2, a['duck2'], self.game.direction2)

    def draw_agent(self, position, duck, direction):
        row, col = position
        x, y = self.cell_position(row, col)
        self.screen.blit(duck[direction], (x - 2, y - 7))

    def draw_panel(self):
        x = self.panel_x
        score1, score2 = self.game.get_score()

        self.draw_panel_box(pygame.Rect(x - 20, 30, 220, 530))

        self.screen.blit(self.title.render('Competitive', True, self.text), (x, 50))
        self.screen.blit(self.title.render('Sokoban', True, self.text), (x, 82))

        self.screen.blit(self.small.render('SCORE', True, self.muted), (x, 130))
        self.screen.blit(self.font.render(f'Agent 1: {score1}', True, self.text), (x, 155))
        self.screen.blit(self.font.render(f'Agent 2: {score2}', True, self.text), (x, 180))

        self.screen.blit(self.font.render('Steps', True, self.muted), (x, 215))

        count = f'{self.game.current_step}/{self.game.max_steps}'
        self.screen.blit(self.title.render(count, True, self.text), (x, 240))

        self.screen.blit(self.small.render('LAST ACTIONS', True, self.muted), (x, 285))
        self.screen.blit(self.small.render(f'Agent 1: {self.game.last_action1}', True, self.text), (x, 310))
        self.screen.blit(self.small.render(f'Agent 2: {self.game.last_action2}', True, self.text), (x, 335))

        if self.game.is_finished():
            self.screen.blit(self.small.render('THE WINNER IS:', True, self.muted), (x, 375))
            self.screen.blit(self.font.render(self.game.get_winner(), True, self.text), (x, 400))
        else:
            self.controls(x, 375)

        self.button(self.back, 'Back to Menu')

    def handle_event(self, event):
        if self.handle_controls(event):
            return True

        if event.type == pygame.MOUSEBUTTONDOWN and self.back.collidepoint(event.pos):
            return True

        return False

    def update(self):
        if self.paused or self.game.is_finished():
            return

        now = pygame.time.get_ticks()

        if now - self.last_move >= 500:
            self.forward()
            self.last_move = now