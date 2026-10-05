import pygame


class Menu:
    BG = (225, 242, 240)
    PANEL = (248, 252, 250)
    BUTTON = (213, 235, 234)
    HOVER = (86, 157, 164)
    BORDER = (160, 202, 201)
    TITLE = (45, 82, 87)
    TEXT = (45, 82, 87)
    MUTED = (103, 139, 141)
    WHITE = (255, 255, 255)
    ERROR = (190, 90, 90)

    def __init__(self):
        pygame.init()

        self.width = 700
        self.height = 520
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Sokoban')

        self.clock = pygame.time.Clock()
        self.title_font = pygame.font.SysFont('Arial', 42, bold=True)
        self.text_font = pygame.font.SysFont('Arial', 17)
        self.button_font = pygame.font.SysFont('Arial', 20, bold=True)

    def reset_screen(self):
        self.screen = pygame.display.set_mode((self.width, self.height))

    def draw_screen(self, subtitle):
        self.screen.fill(self.BG)

        panel = pygame.Rect(130, 55, 440, 410)
        pygame.draw.rect(self.screen, self.PANEL, panel, border_radius=14)
        pygame.draw.rect(self.screen, self.BORDER, panel, 2, border_radius=14)

        title = self.title_font.render('Sokoban', True, self.TITLE)
        self.screen.blit(title, title.get_rect(center=(350, 100)))

        subtitle = self.text_font.render(subtitle, True, self.MUTED)
        self.screen.blit(subtitle, subtitle.get_rect(center=(350, 145)))

    def draw_button(self, rect, text):
        hover = rect.collidepoint(pygame.mouse.get_pos())

        color = self.HOVER if hover else self.BUTTON
        text_color = self.WHITE if hover else self.TEXT

        pygame.draw.rect(self.screen, color, rect, border_radius=8)
        pygame.draw.rect(self.screen, self.BORDER, rect, 2, border_radius=8)

        text = self.button_font.render(text, True, text_color)
        self.screen.blit(text, text.get_rect(center=rect.center))

    def main_menu(self):
        self.reset_screen()

        single = pygame.Rect(190, 215, 320, 55)
        competitive = pygame.Rect(190, 290, 320, 55)
        exit_button = pygame.Rect(190, 365, 320, 55)

        while True:
            self.draw_screen('AI Search & Competitive Game')

            self.draw_button(single, 'Single-agent Solver')
            self.draw_button(competitive, 'Competitive Two-agent')
            self.draw_button(exit_button, 'Exit')

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'exit'

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if single.collidepoint(event.pos):
                        return 'single'

                    if competitive.collidepoint(event.pos):
                        return 'competitive'

                    if exit_button.collidepoint(event.pos):
                        return 'exit'

            self.clock.tick(60)

    def select_map(self, map_files):
        self.reset_screen()

        buttons = []

        for index, file in enumerate(map_files):
            y = 165 + index * 45
            buttons.append((pygame.Rect(190, y, 320, 38), file))

        back = pygame.Rect(250, 415, 200, 40)

        while True:
            self.draw_screen('Select Single-agent Map')

            for rect, file in buttons:
                self.draw_button(rect, file)

            self.draw_button(back, 'Back')
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for rect, file in buttons:
                        if rect.collidepoint(event.pos):
                            return file

                    if back.collidepoint(event.pos):
                        return None

            self.clock.tick(60)

    def enter_steps(self):
        self.reset_screen()

        input_box = pygame.Rect(225, 210, 250, 55)
        start = pygame.Rect(225, 290, 250, 50)
        back = pygame.Rect(225, 380, 250, 50)

        value = ''
        error = ''

        while True:
            self.draw_screen('Competitive Two-agent')

            label = self.text_font.render('Maximum number of steps', True, self.TEXT)
            self.screen.blit(label, label.get_rect(center=(350, 190)))

            pygame.draw.rect(self.screen, self.WHITE, input_box, border_radius=8)
            pygame.draw.rect(self.screen, self.BORDER, input_box, 2, border_radius=8)

            display = value if value else 'Enter n'
            color = self.TITLE if value else self.MUTED

            text = self.button_font.render(display, True, color)
            self.screen.blit(text, text.get_rect(center=input_box.center))

            self.draw_button(start, 'Start Game')
            self.draw_button(back, 'Back')

            if error:
                text = self.text_font.render(error, True, self.ERROR)
                self.screen.blit(text, text.get_rect(center=(350, 445)))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return None

                    if event.key == pygame.K_BACKSPACE:
                        value = value[:-1]

                    elif event.key == pygame.K_RETURN:
                        if value.isdigit() and int(value) > 0:
                            return int(value)

                    elif event.unicode.isdigit():
                        value += event.unicode

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if start.collidepoint(event.pos):
                        if value.isdigit() and int(value) > 0:
                            return int(value)

                        error = 'Please enter a number greater than 0.'

                    if back.collidepoint(event.pos):
                        return None

            self.clock.tick(60)