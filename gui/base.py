import pygame


class BaseGUI:
    def __init__(self):
        pygame.init()

        self.cell = 64
        self.margin = 32
        self.paused = True
        self.last_move = 0

        self.font = pygame.font.SysFont('Arial', 18)
        self.small = pygame.font.SysFont('Arial', 15)
        self.title = pygame.font.SysFont('Arial', 27, bold=True)
        self.clock = pygame.time.Clock()

        self.bg = (225, 242, 240)
        self.panel = (248, 252, 250)
        self.button_color = (213, 235, 234)
        self.primary = (86, 157, 164)
        self.border = (160, 202, 201)
        self.text = (45, 82, 87)
        self.muted = (103, 139, 141)
        self.white = (255, 255, 255)

    def set_screen(self, width, height, caption='Sokoban'):
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)

    def cell_position(self, row, col):
        return self.margin + col * self.cell, self.margin + row * self.cell

    def draw_panel_box(self, rect):
        pygame.draw.rect(self.screen, self.panel, rect, border_radius=14)
        pygame.draw.rect(self.screen, self.border, rect, 2, border_radius=14)

    def button(self, rect, text, selected=False):
        hover = rect.collidepoint(pygame.mouse.get_pos())
        active = selected or hover

        color = self.primary if active else self.button_color
        text_color = self.white if active else self.text

        pygame.draw.rect(self.screen, color, rect, border_radius=8)
        pygame.draw.rect(self.screen, self.border, rect, 2, border_radius=8)

        label = self.font.render(text, True, text_color)
        self.screen.blit(label, label.get_rect(center=rect.center))

    def center_text(self, text, y, font=None, color=None):
        font = font or self.font
        color = color or self.text

        label = font.render(text, True, color)
        rect = label.get_rect(center=(self.screen.get_width() // 2, y))
        self.screen.blit(label, rect)

    def controls(self, x, y):
        items = [
            ('SPACE', 'Play / Pause'),
            ('RIGHT', 'Forward'),
            ('LEFT', 'Backward')
        ]

        for i, (key, label) in enumerate(items):
            py = y + i * 26
            self.screen.blit(self.small.render(key, True, self.text), (x, py))
            self.screen.blit(self.small.render(label, True, self.muted), (x + 70, py))

    def handle_controls(self, event):
        if event.type != pygame.KEYDOWN:
            return False

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

        return False

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                if self.handle_event(event):
                    return

            self.update()
            self.screen.fill(self.bg)
            self.draw_board()
            self.draw_panel()

            pygame.display.flip()
            self.clock.tick(60)