import pygame


class Menu:
    BG = (226, 215, 185)
    PANEL = (247, 238, 216)
    BUTTON = (218, 201, 166)
    BUTTON_HOVER = (128, 96, 65)
    BORDER = (137, 113, 81)
    PANEL_BORDER = (186, 164, 124)
    TITLE = (75, 61, 47)
    TEXT = (91, 75, 57)
    MUTED = (139, 116, 83)
    WHITE = (255, 250, 235)
    ERROR = (160, 80, 70)

    def __init__(self):
        pygame.init()

        self.width = 700
        self.height = 520
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Sokoban')

        self.clock = pygame.time.Clock()
        self.title_font = pygame.font.SysFont('Arial', 42, bold=True)
        self.subtitle_font = pygame.font.SysFont('Arial', 17)
        self.button_font = pygame.font.SysFont('Arial', 20, bold=True)
        self.text_font = pygame.font.SysFont('Arial', 17)

    def reset_screen(self):
        if not pygame.display.get_init():
            pygame.display.init()

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Sokoban')

    def draw_panel(self):
        panel = pygame.Rect(130, 55, 440, 410)
        pygame.draw.rect(self.screen, self.PANEL, panel, border_radius=14)
        pygame.draw.rect(self.screen, self.PANEL_BORDER, panel, 2, border_radius=14)

    def draw_header(self, subtitle):
        title = self.title_font.render('Sokoban', True, self.TITLE)
        self.screen.blit(title, title.get_rect(center=(self.width // 2, 100)))

        text = self.subtitle_font.render(subtitle, True, self.MUTED)
        self.screen.blit(text, text.get_rect(center=(self.width // 2, 145)))

    def draw_button(self, rect, text):
        hover = rect.collidepoint(pygame.mouse.get_pos())
        color = self.BUTTON_HOVER if hover else self.BUTTON
        text_color = self.WHITE if hover else self.TEXT

        pygame.draw.rect(self.screen, color, rect, border_radius=8)
        pygame.draw.rect(self.screen, self.BORDER, rect, 2, border_radius=8)

        label = self.button_font.render(text, True, text_color)
        self.screen.blit(label, label.get_rect(center=rect.center))

    def main_menu(self):
        self.reset_screen()

        single = pygame.Rect(190, 215, 320, 55)
        competitive = pygame.Rect(190, 290, 320, 55)
        exit_button = pygame.Rect(190, 365, 320, 55)

        while True:
            self.screen.fill(self.BG)
            self.draw_panel()
            self.draw_header('AI Search & Competitive Game')

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
        button_height = 38
        gap = 7
        start_y = 165

        for index, file in enumerate(map_files):
            y = start_y + index * (button_height + gap)
            buttons.append((pygame.Rect(190, y, 320, button_height), file))

        back = pygame.Rect(250, 415, 200, 40)

        while True:
            self.screen.fill(self.BG)
            self.draw_panel()
            self.draw_header('Select Single-agent Map')

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

        input_rect = pygame.Rect(225, 210, 250, 55)
        start_button = pygame.Rect(225, 290, 250, 50)
        back_button = pygame.Rect(225, 380, 250, 50)

        value = ''
        error = ''

        while True:
            self.screen.fill(self.BG)
            self.draw_panel()
            self.draw_header('Competitive Two-agent')

            label = self.text_font.render('Maximum number of steps', True, self.TEXT)
            self.screen.blit(label, label.get_rect(center=(self.width // 2, 190)))

            pygame.draw.rect(self.screen, self.WHITE, input_rect, border_radius=8)
            pygame.draw.rect(self.screen, self.BORDER, input_rect, 2, border_radius=8)

            display_value = value if value else 'Enter n'
            input_color = self.TITLE if value else self.MUTED
            input_text = self.button_font.render(display_value, True, input_color)
            self.screen.blit(input_text, input_text.get_rect(center=input_rect.center))

            self.draw_button(start_button, 'Start Game')
            self.draw_button(back_button, 'Back')

            if error:
                error_text = self.text_font.render(error, True, self.ERROR)
                self.screen.blit(error_text, error_text.get_rect(center=(self.width // 2, 445)))

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

                        error = 'Please enter a number greater than 0.'

                    elif event.unicode.isdigit():
                        value += event.unicode

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if start_button.collidepoint(event.pos):
                        if value.isdigit() and int(value) > 0:
                            return int(value)

                        error = 'Please enter a number greater than 0.'

                    if back_button.collidepoint(event.pos):
                        return None

            self.clock.tick(60)