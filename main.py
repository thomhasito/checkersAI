import pygame, sys, asyncio

from data.const import *
from src.game_phase.menu import Menu
from src.game_phase.game import Game
from src.game_phase.end import End

async def main():
    game_finished = False
    state = MENU
    game = None

    while game_finished == False:
        if state == MENU:
            menu = Menu()
            state = menu.run()

        elif state == GAME and menu.get_window():
            if menu.get_name_player() and menu.get_ai_complexity():
                game = Game(menu.get_window(), menu.get_name_player(), menu.get_ai_complexity())
                state = await game.run()

        elif state == END:
            if game and game.get_statut() !=  QUIT:
                end = End(game.get_window(), game.get_statut())
                state = end.run()
                if state == REVANCHE:
                    state = GAME
                elif state == END:
                    game_finished = True
            else:
                game_finished = True
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    asyncio.run(main())