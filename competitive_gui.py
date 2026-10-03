import pygame


class CompetitiveGUI:
    def __init__(self, game, agent1, agent2):
        pygame.init()

        self.game = game
        self.agent1 = agent1
        self.agent2 = agent2

        self.cell = 64
        self.margin = 32
        self.panel_width = 260

        self.rows = self.get_rows()
        self.cols = self.get_cols()

        self.board_width = self.cols * self.cell
        self.board_height = self.rows * self.cell

        width = self.board_width + self.panel_width + self.margin * 3
        height = max(self.board_height + self.margin * 2, 630)

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Competitive Sokoban')

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 18)
        self.small_font = pygame.font.SysFont('Arial', 15)
        self.title_font = pygame.font.SysFont('Arial', 27, bold=True)

        self.background = (226, 215, 185)
        self.text_color = (75, 61, 47)
        self.light_text = (139, 116, 83)

        self.agent1_color = (90, 130, 190)
        self.agent2_color = (190, 90, 90)

        self.running = True
        self.last_action1 = 'Stay'
        self.last_action2 = 'Stay'
        self.last_step_time = 0
        self.step_interval = 1000

        panel_x = self.margin + self.board_width + self.margin
        self.back_button = pygame.Rect(panel_x, 555, 180, 38)

    def get_rows(self):
        if not self.game.walls:
            return 10

        return max(row for row, col in self.game.walls) + 1

    def get_cols(self):
        if not self.game.walls:
            return 10

        return max(col for row, col in self.game.walls) + 1

    def get_rect(self, position):
        row, col = position
        x = self.margin + col * self.cell
        y = self.margin + row * self.cell
        return pygame.Rect(x, y, self.cell, self.cell)

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

    def draw_box(self, rect, owner=None):
        x = rect.left
        y = rect.top
        s = self.cell // 8

        if owner == 1:
            box = (125, 157, 190)
            top = (151, 181, 211)
            border = (72, 94, 119)
            tape = (202, 217, 229)

        elif owner == 2:
            box = (190, 122, 112)
            top = (214, 150, 137)
            border = (119, 72, 65)
            tape = (235, 197, 183)

        else:
            box = (211, 151, 81)
            top = (230, 174, 101)
            border = (125, 81, 44)
            tape = (242, 207, 145)

        pygame.draw.rect(self.screen, border, (x + s, y + s, s * 6, s * 6))
        pygame.draw.rect(self.screen, box, (x + s + 3, y + s + 3, s * 6 - 6, s * 6 - 6))
        pygame.draw.rect(self.screen, top, (x + s + 3, y + s + 3, s * 6 - 6, s * 2))
        pygame.draw.rect(self.screen, tape, (x + s * 3, y + s + 3, s * 2, s * 6 - 6))

    def draw_agent(self, rect, player):
        x = rect.left
        y = rect.top
        s = self.cell // 8

        if player == 1:
            main = (245, 241, 229)
            collar = (70, 112, 173)
            eye = (145, 112, 58)
        else:
            main = (55, 52, 50)
            collar = (181, 59, 77)
            eye = (238, 190, 76)

        pygame.draw.rect(self.screen, main, (x + s * 2, y + s * 4, s * 4, s * 3))

        pygame.draw.rect(self.screen, main, (x + s * 2, y + s, s * 4, s * 4))
        pygame.draw.rect(self.screen, main, (x + s * 2, y, s, s * 2))
        pygame.draw.rect(self.screen, main, (x + s * 5, y, s, s * 2))

        pygame.draw.rect(self.screen, eye, (x + s * 3, y + s * 2, s, s))
        pygame.draw.rect(self.screen, eye, (x + s * 5, y + s * 2, s, s))

        pygame.draw.rect(self.screen, collar, (x + s * 2, y + s * 4, s * 4, s // 2))
    
        pygame.draw.rect(self.screen, main, (x + s * 6, y + s * 4, s, s * 3))
        pygame.draw.rect(self.screen, main, (x + s * 7, y + s * 3, s, s * 2))

    def draw_board(self):
        for row in range(self.rows):
            wall_cols = [col for col in range(self.cols) if (row, col) in self.game.walls]

            if not wall_cols:
                continue

            left = min(wall_cols)
            right = max(wall_cols)

            for col in range(left, right + 1):
                position = (row, col)
                rect = self.get_rect(position)

                if position in self.game.walls:
                    self.draw_wall(rect)
                    continue

                self.draw_floor(rect)

                if position in self.game.destinations:
                    self.draw_goal(rect)

                if position in self.game.boxes:
                    owner = self.game.box_owner.get(position)
                    self.draw_box(rect, owner)

                if position == self.game.agent1:
                    self.draw_agent(rect, 1)

                if position == self.game.agent2:
                    self.draw_agent(rect, 2)

    def draw_button(self, rect, text):
        hover = rect.collidepoint(pygame.mouse.get_pos())

        if hover:
            color = (128, 96, 65)
            text_color = (255, 250, 235)
        else:
            color = (218, 201, 166)
            text_color = (91, 75, 57)

        pygame.draw.rect(self.screen, color, rect, border_radius=7)
        pygame.draw.rect(self.screen, (137, 113, 81), rect, 2, border_radius=7)

        label = self.small_font.render(text, True, text_color)
        self.screen.blit(label, label.get_rect(center=rect.center))

    def draw_panel(self):
        x = self.margin + self.board_width + self.margin
        panel = pygame.Rect(x - 20, 30, 220, 585)

        pygame.draw.rect(self.screen, (247, 238, 216), panel, border_radius=12)
        pygame.draw.rect(self.screen, (186, 164, 124), panel, 2, border_radius=12)

        title = self.title_font.render('Competitive', True, self.text_color)
        title2 = self.title_font.render('Sokoban', True, self.text_color)

        self.screen.blit(title, (x, 50))
        self.screen.blit(title2, (x, 82))

        score1, score2 = self.game.get_score()

        y = 135

        label = self.small_font.render('SCORE', True, self.light_text)
        self.screen.blit(label, (x, y))

        y += 30

        score1_text = self.font.render(f'Agent 1: {score1}', True, self.agent1_color)
        self.screen.blit(score1_text, (x, y))

        y += 30

        score2_text = self.font.render(f'Agent 2: {score2}', True, self.agent2_color)
        self.screen.blit(score2_text, (x, y))

        y += 45
        pygame.draw.line(self.screen, (211, 193, 157), (x, y), (x + 180, y), 1)

        y += 25

        step = self.font.render(f'Step: {self.game.current_step}/{self.game.max_steps}', True, self.text_color)
        self.screen.blit(step, (x, y))

        y += 30

        if self.game.is_finished():
            status = 'FINISHED'
        else:
            status = 'RUNNING'

        status_text = self.small_font.render(f'Status: {status}', True, self.light_text)
        self.screen.blit(status_text, (x, y))

        y += 45

        action_label = self.small_font.render('LAST ACTIONS', True, self.light_text)
        self.screen.blit(action_label, (x, y))

        y += 28

        action1 = self.small_font.render(f'Agent 1: {self.last_action1}', True, self.text_color)
        self.screen.blit(action1, (x, y))

        y += 22

        time1 = self.small_font.render(f'Decision: {self.agent1.last_decision_time:.4f}s', True, self.light_text)
        self.screen.blit(time1, (x, y))

        y += 30

        action2 = self.small_font.render(f'Agent 2: {self.last_action2}', True, self.text_color)
        self.screen.blit(action2, (x, y))

        y += 22

        time2 = self.small_font.render(f'Decision: {self.agent2.last_decision_time:.4f}s', True, self.light_text)
        self.screen.blit(time2, (x, y))

        if self.game.is_finished():
            y += 35
            pygame.draw.line(self.screen, (211, 193, 157), (x, y), (x + 180, y), 1)

            y += 18

            game_over = self.small_font.render('GAME OVER', True, self.light_text)
            self.screen.blit(game_over, (x, y))

            y += 25

            winner = self.font.render(self.game.get_winner(), True, self.text_color)
            self.screen.blit(winner, (x, y))

        self.draw_button(self.back_button, 'Back to Menu')

    def draw(self):
        self.screen.fill(self.background)
        self.draw_board()
        self.draw_panel()
        pygame.display.flip()

    def run_ai_step(self):
        action1 = self.agent1.choose_action(self.game)
        action2 = self.agent2.choose_action(self.game)

        if action1 is None:
            action1 = 'Stay'

        if action2 is None:
            action2 = 'Stay'

        self.last_action1 = action1
        self.last_action2 = action2

        self.agent1.last_action = action1
        self.agent2.last_action = action2

        self.game.step(action1, action2)

    def run(self):
        self.running = True
        self.last_step_time = pygame.time.get_ticks()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.back_button.collidepoint(event.pos):
                        return

            current_time = pygame.time.get_ticks()

            if current_time - self.last_step_time >= self.step_interval:
                if not self.game.is_finished():
                    self.run_ai_step()

                self.last_step_time = current_time

            self.draw()
            self.clock.tick(60)