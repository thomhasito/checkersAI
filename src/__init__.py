import pygame

from random import randint
from data.const import *
from src.display.button import Button

## Initilaisation menu
def init_window() -> pygame.Surface:
    pygame.display.init()
    flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE
    window = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT), flags)
    pygame.display.set_caption(WINDOW_START_TITLE)

    return window

def init_button_menu(start_window:pygame.Surface) -> list:
    button_play = Button (
        text = "Start Game",
        size = 25,
        color = (150, 100, 20),
        text_color = (0, 0, 0),
        rect = pygame.Rect(start_window.get_width() // 2 - Button.BUTTON_WIDTH_STARTGAME // 2, start_window.get_height() // 2 + Button.BUTTON_HEIGHT_STARTGAME, Button.BUTTON_WIDTH_STARTGAME, Button.BUTTON_HEIGHT_STARTGAME),
    )
    button_quit = Button (
        text = "Exit",
        size = 25,
        color = (150, 100, 20),
        text_color = (0, 0, 0),
        rect = pygame.Rect(start_window.get_width() // 2 - Button.BUTTON_WIDTH_STARTGAME // 2, start_window.get_height() - Button.BUTTON_HEIGHT_STARTGAME - 50 , Button.BUTTON_WIDTH_STARTGAME, Button.BUTTON_HEIGHT_STARTGAME),
    )

    button_ai_simple = Button (
        text = "Easy",
        size = 25,
        color = (150, 100, 20),
        text_color = (0, 0, 0),
        rect = pygame.Rect(start_window.get_width() // 2 - Button.BUTTON_WIDTH_GAME*2, start_window.get_height() // 2 + Button.BUTTON_HEIGHT_GAME - 100, Button.BUTTON_WIDTH_GAME, Button.BUTTON_HEIGHT_GAME),
    )

    button_ai_medium = Button (
        text = "Medium",
        size = 25,
        color = (150, 100, 20),
        text_color = (0, 0, 0),
        rect = pygame.Rect(start_window.get_width() // 2 - Button.BUTTON_WIDTH_GAME // 2, start_window.get_height() // 2 + Button.BUTTON_HEIGHT_GAME - 100, Button.BUTTON_WIDTH_GAME, Button.BUTTON_HEIGHT_GAME),
    )

    button_ai_hard = Button (
        text = "Hard",
        size = 25,
        color = (150, 100, 20),
        text_color = (0, 0, 0),
        rect = pygame.Rect(start_window.get_width() // 2 + Button.BUTTON_WIDTH_GAME, start_window.get_height() // 2 + Button.BUTTON_HEIGHT_GAME - 100, Button.BUTTON_WIDTH_GAME, Button.BUTTON_HEIGHT_GAME),
    )
    return button_play, button_quit, button_ai_simple, button_ai_medium, button_ai_hard

def init_menu() -> list:
    pygame.init()
    window = init_window()
    button_play, button_quit, button_ai_simple, button_ai_medium, button_ai_hard = init_button_menu(window)
    return [window, button_play, button_quit, button_ai_simple, button_ai_medium, button_ai_hard]

def init_game_button(window:pygame.Surface) -> list:
    button_surrender = Button (
        text = "Surrender",
        size = 25,
        color = (150, 100, 20),
        text_color = (0, 0, 0),
        rect = pygame.Rect(window.get_width() - Button.BUTTON_WIDTH_GAME - 50, window.get_height() // 2 + Button.BUTTON_HEIGHT_GAME + 50, Button.BUTTON_WIDTH_GAME, Button.BUTTON_HEIGHT_GAME),
    )
    button_exit = Button (
        text = "Exit",
        size = 25,
        color = (150, 100, 20),
        text_color = (0, 0, 0),
        rect = pygame.Rect(window.get_width() - Button.BUTTON_WIDTH_GAME - 50, window.get_height() // 2 + Button.BUTTON_HEIGHT_GAME + 150, Button.BUTTON_WIDTH_GAME, Button.BUTTON_HEIGHT_GAME),
    )
    return [button_surrender, button_exit]

def init_end_button(window:pygame.Surface) -> list:
    button_exit = Button (
        text = "Exit",
        size = 25,
        color = (150, 100, 20),
        text_color = (0, 0, 0),
        rect = pygame.Rect(window.get_width() // 2 - Button.BUTTON_WIDTH_STARTGAME // 2, window.get_height() - Button.BUTTON_HEIGHT_STARTGAME - 50, Button.BUTTON_WIDTH_STARTGAME, Button.BUTTON_HEIGHT_STARTGAME),
    )
    button_revanche = Button (
        text = "Revanche",
        size = 25,
        color = (150, 100, 20),
        text_color = (0, 0, 0),
        rect = pygame.Rect(window.get_width() // 2 - Button.BUTTON_WIDTH_STARTGAME // 2, window.get_height() // 2 + Button.BUTTON_HEIGHT_STARTGAME, Button.BUTTON_WIDTH_STARTGAME, Button.BUTTON_HEIGHT_STARTGAME),
    )
    return [button_exit, button_revanche]

## Initilaisation joueurs
def init_game_players(player_name:str) -> list:
    ai_name = AI_NAME
    if player_name == ai_name:
        player_name = PLAYER_NAME 
    player_color = WHITE if randint(0,1) == 0 else BLACK
    opponent_color = BLACK if player_color == WHITE else WHITE

    return player_name, player_color, ai_name, opponent_color