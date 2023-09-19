import pygame

from src import init_menu
from data.const import *
from src.display.button import Button
from src.display.legende import Legende

class Menu:

    instance_count = 0

    def __init__(self):
        Menu.instance_count += 1
        self.window, self.button_play, self.button_quit, self.button_ai_simple, self.button_ai_medium, self.button_ai_hard = init_menu()
        self.player_name = ""
        self.menu_finished = False
        self.ai_complexity = None

    def update_name_player(self, events:list) -> None:
        for event in events:
            if isinstance(event, pygame.event.Event):
                if event.type == pygame.KEYDOWN:

                    strlen = len(self.get_name_player())
                    if event.key == pygame.K_RETURN:
                        if strlen == 0:
                            self.set_name_player(PLAYER_NAME)
                    
                    elif event.key == pygame.K_BACKSPACE:
                        if self.get_name_player() != "":
                            self.set_name_player(self.get_name_player()[:-1])

                    else:
                        if strlen < MAX_NAME:
                            self.set_name_player(self.get_name_player() + event.unicode)


    def quit_event_menu(events:list) -> bool:
        for event in events:
            if isinstance(event, pygame.event.Event):
                if event.type == pygame.QUIT:
                    return True
        return False
    
    def resize_window(events:list) -> bool:
        for event in events:
            if isinstance(event, pygame.event.Event):
                if event.type == pygame.VIDEORESIZE:
                    return True
        return False
    
    def reset_display_button(self) -> None:
        self.get_button_play().set_around_color((0, 0, 0))
        self.get_button_play().set_text_color((0, 0, 0))
        self.get_button_quit().set_around_color((0, 0, 0))
        self.get_button_quit().set_text_color((0, 0, 0))

        if self.get_ai_complexity() != LEVEL_EASY:
            self.get_button_ai_simple().set_around_color((0, 0, 0))
            self.get_button_ai_simple().set_text_color((0, 0, 0))
        if self.get_ai_complexity() != LEVEL_MEDIUM:
            self.get_button_ai_medium().set_around_color((0, 0, 0))
            self.get_button_ai_medium().set_text_color((0, 0, 0))
        if self.get_ai_complexity() != LEVEL_HARD:
            self.get_button_ai_hard().set_around_color((0, 0, 0))
            self.get_button_ai_hard().set_text_color((0, 0, 0))


    def selection_menu(self, events:list) -> int:
        for event in events:
            if isinstance(event, pygame.event.Event):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.get_button_play().get_rect().collidepoint(mouse_pos):
                        return GAME
                    elif self.get_button_quit().get_rect().collidepoint(mouse_pos):
                        return END
                    elif self.get_button_ai_simple().get_rect().collidepoint(mouse_pos):
                        if self.get_ai_complexity() != LEVEL_EASY:
                            self.set_ai_complexity(LEVEL_EASY)
                        else:
                            self.set_ai_complexity(None)
                    elif self.get_button_ai_medium().get_rect().collidepoint(mouse_pos):
                        if self.get_ai_complexity() != LEVEL_MEDIUM:
                            self.set_ai_complexity(LEVEL_MEDIUM)
                        else:
                            self.set_ai_complexity(None)
                    elif self.get_button_ai_hard().get_rect().collidepoint(mouse_pos):
                        if self.get_ai_complexity() != LEVEL_HARD:
                            self.set_ai_complexity(LEVEL_HARD)
                        else:
                            self.set_ai_complexity(None)
                self.reset_display_button()

        mouse_pos = pygame.mouse.get_pos()
        if self.get_button_play().get_rect().collidepoint(mouse_pos):
            self.get_button_play().set_around_color((255, 0, 0))
            self.get_button_play().set_text_color((255, 0, 0))

        elif self.get_button_quit().get_rect().collidepoint(mouse_pos):
            self.get_button_quit().set_around_color((255, 0, 0))
            self.get_button_quit().set_text_color((255, 0, 0))

        elif self.get_button_ai_simple().get_rect().collidepoint(mouse_pos):
            self.get_button_ai_simple().set_around_color((255, 0, 0))
            self.get_button_ai_simple().set_text_color((255, 0, 0))

        elif self.get_button_ai_medium().get_rect().collidepoint(mouse_pos):
            self.get_button_ai_medium().set_around_color((255, 0, 0))
            self.get_button_ai_medium().set_text_color((255, 0, 0))

        elif self.get_button_ai_hard().get_rect().collidepoint(mouse_pos):
            self.get_button_ai_hard().set_around_color((255, 0, 0))
            self.get_button_ai_hard().set_text_color((255, 0, 0))
        
        else:
            self.reset_display_button()

        return MENU
    
    def draw_all_menu(self) -> None:

        title_text = Legende (
            text = "Checkers",
            size = 115,
            color = (255, 127, 0)
        )
        credits_text = Legende (
            text = "Credits : Thomas Balsalobre",
            size = 25,
            color = (205, 40, 60)
        )
        name_text = Legende (    
            text = "Enter your name (Player by default):",
            size = 36,
            color = (255, 127, 0)
        )
        ai_complexity_text = Legende (
            text = "Select the complexity of the AI :",
            size = 36,
            color = (255, 127, 0)
        )

        self.get_window().fill(WINDOW_BACKGROUND_COLOR)

        # image_fond = pygame.image.load(WINDOW_START_IMAGE)
        # fond = image_fond.convert()
        # self.get_window().blit(fond,(0,0))

        title_text_position_x = self.get_window().get_width() // 2 - title_text.width // 2
        title_text_position_y = 50
        title_text.set_position(title_text_position_x, title_text_position_y)

        credits_text_position_x = 0
        credits_text_position_y = self.get_window().get_height() - credits_text.height
        credits_text.set_position(credits_text_position_x, credits_text_position_y)

        name_text_position_x = self.get_window().get_width() // 2 - name_text.width // 2
        name_text_position_y = self.get_window().get_height() // 2 - 250
        name_text.set_position(name_text_position_x, name_text_position_y)

        ai_complexity_text_position_x = self.get_window().get_width() // 2 - ai_complexity_text.width // 2
        ai_complexity_text_position_y = self.get_window().get_height() // 2 - 100
        ai_complexity_text.set_position(ai_complexity_text_position_x, ai_complexity_text_position_y)

        title_text.draw(self.get_window())
        credits_text.draw(self.get_window())
        name_text.draw(self.get_window())
        ai_complexity_text.draw(self.get_window())

        self.get_button_play().draw(self.get_window())
        self.get_button_quit().draw(self.get_window())
        self.get_button_ai_simple().draw(self.get_window())
        self.get_button_ai_medium().draw(self.get_window())
        self.get_button_ai_hard().draw(self.get_window())

        input_rect = pygame.Rect(self.get_window().get_width() // 2 - 100, self.get_window().get_height() // 2 - 200, 200, 40)
        font = pygame.font.Font(None, 36)

        input_surface = font.render(self.get_name_player(), True, (255, 127, 0))
        self.get_window().blit(input_surface, (input_rect.centerx - input_surface.get_width() // 2, input_rect.centery - input_surface.get_height() // 2))
        pygame.draw.rect(self.get_window(), (0, 0, 0), input_rect, 2)

        pygame.display.flip()
    
    def run(self) -> list:
        while not self.is_finished():

            events = pygame.event.get()
            if Menu.quit_event_menu(events):
                self.finished()
                return END
            
            if Menu.resize_window(events):
                self.get_button_play().resize_rect(self.get_window())
                self.get_button_quit().resize_rect(self.get_window())
                self.get_button_ai_simple().resize_rect(self.get_window())
                self.get_button_ai_medium().resize_rect(self.get_window())
                self.get_button_ai_hard().resize_rect(self.get_window())
            
            self.update_name_player(events)
            statut = self.selection_menu(events)

            if statut == GAME:
                if self.get_name_player() in ["",AI_NAME]:
                    self.set_name_player(PLAYER_NAME)
                if self.get_ai_complexity():
                    self.finished()
                    return GAME

            elif statut == END:
                self.finished()
                return END
                
            self.draw_all_menu()

    def get_window(self) -> pygame.Surface:
        return self.window
    
    def get_button_play(self) -> Button:
        return self.button_play
    
    def get_button_quit(self) -> Button:
        return self.button_quit
    
    def get_button_ai_simple(self) -> Button:
        return self.button_ai_simple
    
    def get_button_ai_medium(self) -> Button:
        return self.button_ai_medium
    
    def get_button_ai_hard(self) -> Button:
        return self.button_ai_hard
    
    def get_name_player(self) -> str:
        return self.player_name
    
    def set_name_player(self, player_name:str):
        self.player_name = player_name

    def is_finished(self) -> bool:
        return self.menu_finished
    
    def finished(self) -> None:
        self.menu_finished = True

    def get_ai_complexity(self) -> str:
        return self.ai_complexity
    
    def set_ai_complexity(self, ai_complexity:str):
        self.ai_complexity = ai_complexity