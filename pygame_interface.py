import pygame
import sys

COLORS = {
    'black': pygame.Color(0, 0, 0),
    'gray': pygame.Color(150, 150, 150),
    'white': pygame.Color(255, 255, 255)
}

class PygameInterface:
    def __init__(self, width=800, height=600, input_callback=None, char_limit=100):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption("Pygame Window")
        self.clock = pygame.time.Clock()
        self.text_box = TextBox(0, height - 50, width, 50, char_limit)
        self.input_callback = input_callback
        self.response_text = ""
        self.user_input_active = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                self.text_box.update_size(event.w, 50, event.h - 50)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    text = self.text_box.get_text()
                    if self.input_callback:
                        response = self.input_callback(text)  # Call the OpenAIClient here
                        self.update_with_response(response)  # Update the screen with the AI's response
                    self.text_box.clear_text()
                else:
                    self.text_box.handle_key(event)

    def update_screen(self):
        self.screen.fill(COLORS['black'])  # Fill the screen with black
        self.text_box.draw(self.screen)
        self.draw_response(self.screen)
        pygame.display.flip()
        self.clock.tick(60)

    def draw_response(self, screen):
        # Clear the area where the response is displayed
        pygame.draw.rect(screen, COLORS['black'], pygame.Rect(0, 0, self.screen.get_width(), self.text_box.rect.y - 10))

        font = pygame.font.Font(None, 32)
        lines = self.response_text.split('\n')
        y_offset = self.text_box.rect.y - 30*len(lines)  # Adjust the starting y position

        for line in lines:
            txt_surface = font.render(line, True, COLORS['white'])
            screen.blit(txt_surface, (5, y_offset))
            y_offset += 30  # Move down for each line

    def update_with_response(self, response):
        self.response_text = self.wrap_text(response, self.screen.get_width() - 10)
        self.user_input_active = False

    def wrap_text(self, text, max_width):
        font = pygame.font.Font(None, 32)
        words = text.split(' ')
        lines = []
        current_line = words[0]
        for word in words[1:]:
            if font.size(current_line + ' ' + word)[0] <= max_width:
                current_line += ' ' + word
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        return '\n'.join(lines)  # Not limited to any number of lines of text

    def run(self):
        while True:
            self.handle_events()
            self.update_screen()

class TextBox:
    def __init__(self, x, y, width, height, char_limit=100):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = COLORS['white']
        self.text_prefix = 'YOU: '
        self.text = ''
        self.char_limit = char_limit
        self.font = pygame.font.Font(None, 32)
        self.txt_surface = self.font.render(self.text_prefix + self.text, True, self.color)
        self.active = True

    def handle_key(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        elif event.key == pygame.K_SPACE:
            if len(self.text) < self.char_limit:
                self.text += ' '
        elif event.unicode.isprintable():
            if len(self.text) < self.char_limit:
                self.text += event.unicode
        self.txt_surface = self.font.render(self.text_prefix + self.text, True, self.color)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def clear_text(self):
        self.text = ''
        self.txt_surface = self.font.render(self.text_prefix, True, self.color)

    def get_text(self):
        return self.text

    def update_size(self, width, height, y):
        self.rect.update(self.rect.x, y, width, height)
        self.txt_surface = self.font.render(self.text, True, self.color)
