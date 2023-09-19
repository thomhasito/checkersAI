import pygame

class Button:
    
    BUTTON_WIDTH_STARTGAME = BUTTON_WIDTH_NAME = 350
    BUTTON_HEIGHT_STARTGAME = BUTTON_HEIGHT_NAME = 100

    BUTTON_WIDTH_GAME = 200
    BUTTON_HEIGHT_GAME = 50

    def __init__(self, text, size, color, text_color, rect: pygame.Rect, fontFile=None):
        self.text = text
        self.size = size
        self.font = pygame.font.Font(fontFile, size)
        self.color = color
        self.text_color = text_color
        self.around_color = (0, 0, 0)
        self.rect = rect

    def get_text(self) -> str:
        return self.text
    
    def get_size(self) -> int:
        return self.size
    
    def get_font(self) -> pygame.font.Font:
        return self.font
    
    def get_color(self) -> tuple:
        return self.color
    
    def get_around_color(self) -> tuple:
        return self.around_color
    
    def set_around_color(self, color:tuple):
        self.around_color = color
    
    def get_text_color(self) -> tuple:
        return self.text_color
    
    def set_text_color(self, color:tuple):
        self.text_color = color
    
    def get_rect(self) -> pygame.Rect:
        return self.rect
    
    def set_rect(self, rect: pygame.Rect):
        self.rect = rect
    
    def resize_rect(self, window: pygame.Surface):
        self.set_rect(pygame.Rect(window.get_width() // 2 - self.get_rect().width // 2,
                                self.get_rect().y,
                                self.get_rect().width,
                                self.get_rect().height
                                ))

    def draw(self, window: pygame.Surface):
        pygame.draw.rect(window, self.get_color(), self.get_rect(), 0, 5, 5, 5, 5, 5)
        pygame.draw.rect(window, self.get_around_color(), self.get_rect(), 2, 5, 5, 5, 5, 5)
        text = self.font.render(self.get_text(), True, self.get_text_color())
        window.blit(text, (self.get_rect().centerx - text.get_width() // 2, self.get_rect().centery - text.get_height() // 2))