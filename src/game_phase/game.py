import pygame, re, asyncio

from src import init_game_players, init_game_button
from data.const import *
from src.board.player import Player
from src.board.board import Board
from src.board.case import Case
from src.manager.file_manager import FileManager
from src.manager.event_manager import EventManager
from src.display.legende import Legende
from src.logic.movement import available_moves, get_type_play
from src.logic.ai import alphabeta
from copy import deepcopy

class Game:

    instance_count = 0

    def __init__(self, window:pygame.Surface, player_name:str, ai_complexity:str):
        Game.instance_count += 1
        # Initialisation pygame
        self.window = window
        self.clock = pygame.time.Clock()

        # Initialisation des variables de jeu
        self.statut = PLAYING
        self.ai_complexity = ai_complexity
        self.available_moves = {}

        # Initialisation des joueurs
        player_name, player_color, ai_name, ai_color = init_game_players(player_name)
        player = Player(player_name, player_color)
        ai = Player(ai_name, ai_color)

        # Initialisation du gestionnaire de fichiers
        self.file_manager = FileManager()
        start_grid = self.file_manager.get_start_grid()

        # Initialisation du plateau
        self.board = Board(ai, player, start_grid, self.file_manager)

        # Initialisation du gestionnaire d'évènements
        surrender_button, exit_button = init_game_button(self.get_window())
        self.event_manager = EventManager(self.get_board(), player, surrender_button, exit_button)

        self.ai_future = None

    # Getting Part
    def get_window(self) -> pygame.Surface:
        return self.window
    
    def get_clock(self) -> pygame.time.Clock:
        return self.clock
    
    def get_statut(self) -> str:
        return self.statut
    
    def get_ai_complexity(self) -> str:
        return self.ai_complexity
    
    def set_statut(self, statut:str) -> None:
        self.statut = statut
    
    def get_available_moves(self) -> list:
        return self.available_moves
    
    def set_available_moves(self) -> None:
        self.clear_available_moves()
        self.available_moves = available_moves(self.get_board(), self.get_current_player().get_color())

    def clear_available_moves(self) -> None:
        self.available_moves = {}

    def get_ai_move(self) -> asyncio.Future:
        return self.ai_future
    
    def get_file_manager(self) -> FileManager:
        return self.file_manager
    
    def get_board(self) -> Board:
        return self.board
    
    def get_event_manager(self) -> EventManager:
        return self.event_manager
    
    def get_current_player(self) -> Player:
        return self.get_board().get_player() if self.get_board().get_player().is_turn() else self.get_board().get_ai()
    
    def get_opponent_player(self) -> Player:
        return self.get_board().get_player() if self.get_board().get_ai().is_turn() else self.get_board().get_ai()
    
    def change_player_turn(self) -> None:
        self.get_board().get_player().set_turn(not self.get_board().get_player().is_turn())
        self.get_board().get_ai().set_turn(not self.get_board().get_ai().is_turn())


    async def player_play(self, case_origin: Case, case_desti: Case) -> None:
    
        type_play = get_type_play(self.get_available_moves())
        board = self.get_board()
        piece = case_origin.get_piece()
        board.move_piece(case_origin,case_desti, case_origin.get_piece())
        last_movement = {
                    "piece": piece.get_color() + piece.get_type(),
                    "type": type_play,
                    "origin": case_origin.get_position(),
                    "destination": case_desti.get_position(),
                    "eliminated_pawns": None,
                    }
        if type_play == TYPE_ATTACK:
            queens_killed, pawns_killed = board.kill_pieces(to_return=True)
            last_movement["eliminated_pawns"] = pawns_killed + queens_killed
            self.get_board().update_count_materials()
        else:
            queens_killed, pawns_killed = [], []
                
        self.get_file_manager().save_last_move(last_movement)
        if (type_play == TYPE_ATTACK and len(pawns_killed) == 0 and len(queens_killed) > 0) or type_play == TYPE_MOVEMENT:
            self.get_file_manager().save_last_grid(board.get_grid_score())
        else:
            self.get_file_manager().delete_all_grids()

    async def compute_ai_move(self) -> None:
        self.ai_future = asyncio.ensure_future(self.ai_play(self.get_board()))
        await self.ai_future

    async def ai_play(self, current_board:Board) -> None:
        alpha = float('-inf')
        beta = float('inf')
        movement = {}
        copy_board = deepcopy(current_board)
        depth = 0
        if self.get_ai_complexity() == LEVEL_EASY:
            depth = 3
        elif self.get_ai_complexity() == LEVEL_MEDIUM or self.get_ai_complexity() == LEVEL_HARD:
            depth = 4
        best_score, best_board, ai_movement, total_paths = alphabeta(copy_board,
                                                                     movement,
                                                                     self.get_board().get_player(),
                                                                     self.get_board().get_ai(),
                                                                     self.get_board().get_ai().is_max_player(),
                                                                     depth,
                                                                     alpha,
                                                                     beta,
                                                                     self.get_ai_complexity())
        self.get_board().set_case_board(best_board.get_case_board())
        self.get_board().set_player(best_board.get_player())
        self.get_board().set_ai(best_board.get_ai())
        self.get_board().update_count_materials()
        self.get_file_manager().save_last_move(ai_movement)
        self.get_file_manager().save_last_grid(best_board.get_grid_score())
        print(f"{AI_NAME} : {best_score} {AI_NAME} movement: {ai_movement}, ite: {total_paths}")


    def set_if_winner(self) -> None:
        player = self.get_board().get_player()
        ai = self.get_board().get_ai()
        if re.search(rf"{player.get_name()}", self.get_statut()):
            player.set_winner(True)
        elif re.search(rf"{ai.get_name()}", self.get_statut()):
            ai.set_winner(True)


    async def run(self) -> list:
        changes_to_draw = True
        begin_play = True
        end_play = False
        selected_case_piece = None
        selected_case_desti = None

        while self.get_statut() == PLAYING:

            self.get_event_manager().set_events()

            if self.get_event_manager().quit_event():
                self.set_statut(QUIT)
                break

            if self.get_event_manager().surrender():
                self.set_statut(WIN + " " + self.get_board().get_ai().get_name())
                self.set_if_winner()
                break

            if self.get_event_manager().event_display_button():
                changes_to_draw = True

            if end_play:
                self.get_board().unclick_all_cases()
                self.get_board().show_last_move()
                self.change_player_turn()
                begin_play = True
                end_play = False
                changes_to_draw = True

            if changes_to_draw:
                self.draw_all_game()
                changes_to_draw = False

            if begin_play:
                self.set_available_moves()
                game_over, game_statut = self.get_board().game_over(self.get_available_moves(),
                                                                    self.get_current_player(),
                                                                    self.get_opponent_player())
                if game_over:
                    self.set_statut(game_statut)
                    self.set_if_winner()
                    break
                begin_play = False
            

            if self.get_current_player().get_name() == self.get_board().get_ai().get_name():
                await self.compute_ai_move()
                end_play = True

            elif self.get_current_player().get_name() == self.get_board().get_player().get_name():
                if self.get_event_manager().event_board():
                    self.get_event_manager().clear_events()
                    selected_case_piece = self.get_board().get_selected_case(ending=False)
                    hovered_case = self.get_event_manager().get_hovered_case()
                    selected_case_desti = self.get_board().get_selected_case(ending=True)
                    changes_to_draw = True

                if isinstance(selected_case_piece, Case) and isinstance(hovered_case, Case) and changes_to_draw:
                    if hovered_case.get_color() in [GREEN_COLOR, YELLOW_GREEN_COLOR]:
                        self.get_board().show_attacks_paths(self.get_available_moves(), selected_case_piece, hovered_case)
                    else:
                        self.get_board().origin_case_color(exceptions=[selected_case_piece, hovered_case])
                        self.get_board().show_available_cases(self.get_available_moves(), selected_case_piece)
                        
                    if isinstance(selected_case_desti, Case):
                        await self.player_play(selected_case_piece, selected_case_desti)
                        end_play = True

        self.get_file_manager().delete_all_grids()
        self.get_file_manager().delete_last_move()
        
        return END
    

    def __draw_turn_indicator(self, namex, namey) -> None:
        triangle_height = 20
        triangle_x = namex
        triangle_y = namey
        triangle_color = (255, 0, 0)

        pygame.draw.polygon(self.get_window(),
                            triangle_color,
                            [(triangle_x, triangle_y),
                             (triangle_x, triangle_y + triangle_height),
                             (triangle_x + triangle_height, triangle_y + triangle_height // 2)
                             ])
        
    def __draw_names(self, player:Player) -> None:
        nameplayer = "name" + player.get_name()
        
        nameplayer = Legende (
            text = player.get_name(),
            size = 36,
            color = (255, 0, 0) if player.is_turn() == True else (0, 0, 0)
        )
        position_x = self.get_window().get_width() // 2 - nameplayer.get_width() // 2
        position_y = 15 if player.get_name() == self.get_board().get_ai().get_name() else self.get_window().get_height() - nameplayer.get_height() - 15
        nameplayer.set_position(position_x, position_y)

        if player.get_name() == self.get_board().get_ai().get_name():
            nameplayer.draw(self.get_window())
        elif player.get_name() == self.get_board().get_player().get_name():
            nameplayer.draw(self.get_window())

        if player.is_turn():
            self.__draw_turn_indicator(nameplayer.x - 30,
                                        nameplayer.y + nameplayer.height // 2 - 10)


    def __draw_stuff(self, player:Player) -> None:
        pawns = player.get_pawns()
        queens = player.get_queens()

        pawnText = Legende (
            text = "Pions : " + str(pawns),
            size = 36,
            color = (0, 0, 0)
        )

        queenText = Legende (
            text = "Dames : " + str(queens),
            size = 36,
            color = (0, 0, 0)
        )

        position_x = 50
        position_y_pawn = 100 if player.get_name() == self.get_board().get_ai().get_name() else self.get_window().get_height() - 150
        position_y_queen = 150 if player.get_name() == self.get_board().get_ai().get_name() else self.get_window().get_height() - 100
        pawnText.set_position(position_x, position_y_pawn)
        queenText.set_position(position_x, position_y_queen)

        if player.get_name() == self.get_board().get_ai().get_name():
            pawnText.draw(self.get_window())
            queenText.draw(self.get_window())
        elif player.get_name() == self.get_board().get_player().get_name():
            pawnText.draw(self.get_window())
            queenText.draw(self.get_window())

    def draw_all_game(self) -> None:

        self.get_window().fill(WINDOW_BACKGROUND_COLOR)

        self.get_board().draw(self.get_window())
        for player in self.get_board().get_player(), self.get_board().get_ai():
            self.__draw_names(player)
            self.__draw_stuff(player)
        self.get_event_manager().get_surrender_button().draw(self.get_window())
        self.get_event_manager().get_exit_button().draw(self.get_window())

        pygame.display.flip()
        pygame.display.update()

        self.get_clock().tick(FPS)