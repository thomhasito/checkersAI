import pygame

from src import init_end_button
from data.const import *
from src.display.button import Button
from src.display.legende import Legende

class End:

    def __init__(self, window:pygame.Surface, final_statut:str):
        self.window = window
        self.final_statut = final_statut
        self.exit_button, self.revanche_button = init_end_button(self.get_window())

    def get_window(self) -> pygame.Surface:
        return self.window
    
    def get_final_statut(self) -> str:
        return self.final_statut
    
    def get_exit_button(self) -> Button:
        return self.exit_button
    
    def get_revanche_button(self) -> Button:
        return self.revanche_button
    
    def draw_all_end(self) -> None:
        self.get_window().fill(WINDOW_BACKGROUND_COLOR)
        self.get_exit_button().draw(self.get_window())
        self.get_revanche_button().draw(self.get_window())

        end_text = Legende (
            text = self.get_final_statut(),
            size = 54,
            color = (0, 0, 0)
        )

        position_x = self.get_window().get_width() // 2 - end_text.get_width() // 2
        position_y = self.get_window().get_height() // 2 - end_text.get_height() // 2 - 100
        end_text.set_position(position_x, position_y)
        end_text.draw(self.get_window())

        pygame.display.flip()
        pygame.display.update()

    def run(self) -> int:
        state = None
        while not state:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.get_exit_button().get_rect().collidepoint(mouse_pos):
                        state = END
                        break
                    elif self.get_revanche_button().get_rect().collidepoint(mouse_pos):
                        state = REVANCHE
                        break
                elif event.type == pygame.QUIT:
                    state = END
                    break
                elif event.type == pygame.MOUSEMOTION:
                    if self.get_exit_button().get_rect().collidepoint(mouse_pos):
                        self.get_exit_button().set_around_color((255, 0, 0))
                        self.get_exit_button().set_text_color((255, 0, 0))
                        self.get_revanche_button().set_around_color((0, 0, 0))
                        self.get_revanche_button().set_text_color((0, 0, 0))
                    
                    elif self.get_revanche_button().get_rect().collidepoint(mouse_pos):
                        self.get_revanche_button().set_around_color((255, 0, 0))
                        self.get_revanche_button().set_text_color((255, 0, 0))
                        self.get_exit_button().set_around_color((0, 0, 0))
                        self.get_exit_button().set_text_color((0, 0, 0))

                    else:
                        if self.get_exit_button().get_around_color() == (255, 0, 0) or self.get_revanche_button().get_around_color() == (255, 0, 0):
                            self.get_exit_button().set_around_color((0, 0, 0))
                            self.get_exit_button().set_text_color((0, 0, 0))
                            self.get_revanche_button().set_around_color((0, 0, 0))
                            self.get_revanche_button().set_text_color((0, 0, 0))

            self.draw_all_end()
        
        return state
