import pygame

class Legende:

    def __init__(self, text:str, size:int, color:tuple, fontFile:str=None):
        self.text = text
        self.size = size
        self.font = pygame.font.Font(fontFile, size)
        self.color = color
        self.width, self.height = self.font.size(self.text)

    def get_text(self) -> str:
        return self.text
    
    def get_size(self) -> int:
        return self.size
    
    def get_font(self) -> pygame.font.Font:
        return self.font
    
    def get_color(self) -> tuple:
        return self.color
    
    def get_width(self) -> int:
        return self.width
    
    def get_height(self) -> int:
        return self.height
    
    def set_position(self, x:int, y:int):
        self.x = x
        self.y = y

    def get_x(self) -> int:
        return self.x
    
    def get_y(self) -> int:
        return self.y

    def draw(self, window: pygame.Surface):
        text = self.get_font().render(self.get_text(), True, self.get_color())
        window.blit(text, (self.get_x(), self.get_y()))