import pygame

from data.const import *
from src.board.player import Player
from src.board.case import Case
from src.board.piece import Piece
from src.manager.file_manager import FileManager
from typing import Union


class Board:

    instance_count = 0

    def __init__(self, ai: Player, player: Player, start_grid: list, file_manager:FileManager):
        Board.instance_count += 1
        self.ai = ai
        self.player = player
        self.ai_color = self.ai.get_color()
        self.player_color = self.player.get_color()
        self.rect = pygame.Rect(BOARD_X_OFFSET, BOARD_Y_OFFSET, BOARD_WIDTH, BOARD_HEIGHT)
        self.rect_color = (0, 0, 0)
        self.rect_thickness = 3
        self.start_grid = start_grid
        self.case_board = [[Case for _ in range(NB_COLS)] for _ in range(NB_ROWS)]
        self.init_case_board()
        self.file_manager = file_manager
        self.update_count_materials()

        self.moves_draw = 0
        self.moves_draw_composition = 0

        # Initialisation des compositions nulles
        # Directement
        self.draw_compositions = [
            {
                "player_1": {"queens": 2,"pawns": 0},
                "player_2": {"queens": 1,"pawns": 0}
            },
            {
                "player_1": {"queens": 1,"pawns": 0},
                "player_2": {"queens": 1,"pawns": 0}
            }
        ] 
        # Après 16 coups
        self.draw_compositions_16 = [
            {
                "player_1": {"queens": 3,"pawns": 0},
                "player_2": {"queens": 1,"pawns": 0}
            },
            {
                "player_1": {"queens": 2,"pawns": 1},
                "player_2": {"queens": 1,"pawns": 0}
            },
            {
                "player_1": {"queens": 1,"pawns": 2},
                "player_2": {"queens": 1,"pawns": 0}
            }
        ]


    def init_case_board(self) -> None:
        for row_idx, row in enumerate(self.start_grid):
            for col_idx, _ in enumerate(row):

                if (row_idx + col_idx) % 2 == 0:
                    case_color = BEIGE_COLOR
                else:
                    case_color = BROWN_COLOR
                value = self.start_grid[row_idx][col_idx]

                if value in [AI_PAWN,AI_QUEEN,PLAYER_PAWN,PLAYER_QUEEN]:
                    if value == AI_PAWN:
                        piece_type = PAWN
                        piece_color = self.get_ai_color()
                    elif value == AI_QUEEN:
                        piece_type = QUEEN
                        piece_color = self.get_ai_color()
                    elif value == PLAYER_PAWN:
                        piece_type = PAWN
                        piece_color = self.get_player_color()
                    elif value == PLAYER_QUEEN:
                        piece_type = QUEEN
                        piece_color = self.get_player_color()
                    case_piece = Piece(piece_type, piece_color, row_idx, col_idx, value)

                else:
                    if value == VIDE:
                        case_piece = VIDE
                    else:
                        raise ValueError(f"Unknown value {value} in grid")
                    
                current_case = Case(row_idx, col_idx, case_color)
                current_case.set_piece(case_piece)
                self.case_board[row_idx][col_idx] = current_case


    def count_players_stuff(self) -> tuple:
        ai_pawns = 0
        ai_queens = 0
        player_pawns = 0
        player_queens = 0

        for row_idx, row in enumerate(self.case_board):
            for col_idx, _ in enumerate(row):
                case = self.case_board[row_idx][col_idx]
                piece = case.get_piece()
                if isinstance(piece, Piece):
                    if piece.type == PAWN:
                        if piece.color == self.get_ai_color():
                            ai_pawns += 1
                        elif piece.color == self.get_player_color():
                            player_pawns += 1
                    elif piece.type == QUEEN:
                        if piece.color == self.get_ai_color():
                            ai_queens += 1
                        elif piece.color == self.get_player_color():
                            player_queens += 1

        return (ai_pawns, ai_queens, player_pawns, player_queens)
    
    def update_count_materials(self) -> None:
        ai_pawns, ai_queens, player_pawns, player_queens = self.count_players_stuff()
        self.get_ai().set_pawns(ai_pawns)
        self.get_ai().set_queens(ai_queens)
        self.get_player().set_pawns(player_pawns)
        self.get_player().set_queens(player_queens)
    
    def get_grid_score(self) -> list:
        current_grid = [[VIDE for _ in range(NB_COLS)] for _ in range(NB_ROWS)]

        for row_idx, row in enumerate(self.case_board):
            for col_idx, _ in enumerate(row):
                case = self.case_board[row_idx][col_idx]
                piece = case.get_piece()
                if isinstance(piece, Piece):
                    if piece.get_type() == PAWN:
                        if piece.get_color() == self.get_ai_color():
                            current_grid[row_idx][col_idx] = AI_PAWN
                        elif piece.get_color() == self.get_player_color():
                            current_grid[row_idx][col_idx] = PLAYER_PAWN
                    elif piece.get_type() == QUEEN:
                        if piece.get_color() == self.get_ai_color():
                            current_grid[row_idx][col_idx] = AI_QUEEN
                        elif piece.get_color() == self.get_player_color():
                            current_grid[row_idx][col_idx] = PLAYER_QUEEN

        return current_grid

    def static_evaluation(self, ai_pawns, ai_queens, player_pawns, player_queens) -> int:
        return (ai_pawns * AI_PAWN + ai_queens * AI_QUEEN) + (player_pawns * PLAYER_PAWN + player_queens * PLAYER_QUEEN)

    def game_phase(self, nb_ai_pawns, nb_ai_queens, nb_player_pawns, nb_player_queens) -> str:
        total_pawns = nb_ai_pawns + nb_player_pawns
        total_queens = nb_ai_queens + nb_player_queens

        opening_threshold_pawns = 30
        middle_game_threshold_pawns = 15
        end_game_threshold_pawns = 15

        if total_pawns >= opening_threshold_pawns:
            if total_queens == 0:
                return OPENING
            else:
                return MIDDLE_GAME
        elif total_pawns >= middle_game_threshold_pawns:
                return MIDDLE_GAME
        elif total_pawns <= end_game_threshold_pawns:
            if total_queens >= 1:
                return FAST_END_GAME
            else:
                return SLOW_END_GAME


    
    def index_case_selected(self, ending: bool) -> Union[tuple,None]:
        for row_idx, row in enumerate(self.case_board):
            for col_idx, _ in enumerate(row):
                case = self.case_board[row_idx][col_idx]
                piece = case.get_piece()
                if (not ending
                    and isinstance(piece, Piece)
                    and case.is_selected()):
                    return (row_idx, col_idx)
                if (ending
                    and piece
                    and case.is_selected()
                    and case.get_color() == GREEN_COLOR
                    and self.get_selected_case(ending=False)):
                    return (row_idx, col_idx)
                if (ending
                    and not piece
                    and case.is_selected()):
                    return (row_idx, col_idx)
        return None
    

    def get_selected_case(self, ending: bool) -> Union[Case,None]:
        index_case_selected = self.index_case_selected(ending)
        if index_case_selected:
            return self.case_board[index_case_selected[0]][index_case_selected[1]]
        return None


    def move_piece(self, case_origin: Case, case_desti: Case, piece_to_move: Piece) -> None:
        if case_origin.get_position() == case_desti.get_position():
            return None
        piece_to_move.set_position(case_desti.row, case_desti.col)
        case_desti.set_piece(piece_to_move)
        case_origin.remove_piece()
        
        if piece_to_move.get_type() == PAWN:
            if piece_to_move.get_color() == self.get_ai_color():
                if piece_to_move.get_position()[0] == NB_ROWS - 1:
                    piece_to_move.promo_queen(self.get_player())
            elif piece_to_move.get_color() == self.get_player_color():
                if piece_to_move.get_position()[0] == 0:
                    piece_to_move.promo_queen(self.get_player())


    def origin_case_color(self, exceptions: Union[list,None]) -> None:
        for row_idx, row in enumerate(self.get_case_board()):
            for col_idx, _ in enumerate(row):
                case = self.get_case_board()[row_idx][col_idx]
                if isinstance(case, Case) and case not in exceptions:
                    case.origin_color()

    def origin_piece_statut(self, exceptions: Union[list,None]) -> None:
        for row_idx, row in enumerate(self.get_case_board()):
            for col_idx, _ in enumerate(row):
                case = self.get_case_board()[row_idx][col_idx]
                if isinstance(case, Case) and case not in exceptions:
                    piece = case.get_piece()
                    if isinstance(piece, Piece) and piece.get_statut() == DEAD:
                        piece.set_statut(ALIVE)


    def show_available_cases(self, availables_moves: dict, selected_case: Case) -> None:

        for key in availables_moves.keys():
            path = availables_moves[key]["path"]
            if path[0] == selected_case.get_position():
                case_desti = self.get_case_board()[path[-1][0]][path[-1][1]]
                if isinstance(case_desti, Case):
                    if not case_desti.is_selected():
                        case_desti.set_color(GREEN_COLOR)
                    elif case_desti.get_position() == selected_case.get_position() and case_desti.get_color() != GREEN_COLOR:
                        case_desti.set_color(YELLOW_GREEN_COLOR)


    def show_attacks_paths(self, availables_moves: dict, selected_case: Case, hovered_case: Case) -> None:

        self.origin_case_color(exceptions=[selected_case, hovered_case])
        self.origin_piece_statut(exceptions=[selected_case, hovered_case])
        attacks_paths = []

        for key in availables_moves.keys():
            path = availables_moves[key]["path"]
            if availables_moves[key]["type"] == "ATTACK":
                eliminated_pawns = availables_moves[key]["eliminated_pawns"]
                if selected_case.get_position() == path[0] and hovered_case.get_position() == path[-1]:
                    to_append = [path, eliminated_pawns]
                    attacks_paths.append(to_append)

        if attacks_paths != []:
            if len(attacks_paths) > 1:
                attacks_paths = attacks_paths[:1]
            for path, eliminated_pawns in attacks_paths:
                for i in range(1, len(path) - 1):
                    case = self.get_case_board()[path[i][0]][path[i][1]]
                    if isinstance(case, Case) and not case.is_selected() and case.get_position() != path[-1]:
                        case.set_color(ORANGE_COLOR)

                for row_case, col_case in eliminated_pawns:
                    case = self.get_case_board()[row_case][col_case]
                    if isinstance(case, Case) and not case.is_selected():
                        case.set_color(RED_COLOR)
                        case.get_piece().set_statut(DEAD)


    def show_last_move(self) -> None:
        last_movement = self.get_file_manager().get_last_move()
        if last_movement != {}:
            type_play = last_movement["type"]
            index_case_origin = last_movement["origin"]
            index_case_destination = last_movement["destination"]
            case_origin = self.get_case_board()[index_case_origin[0]][index_case_origin[1]]
            case_destination = self.get_case_board()[index_case_destination[0]][index_case_destination[1]]
            if isinstance(case_origin, Case) and isinstance(case_destination, Case):
                case_origin.set_color(ORANGE_COLOR)
                case_destination.set_color(ORANGE_COLOR)
            if type_play == TYPE_ATTACK:
                eliminated_pawns = last_movement["eliminated_pawns"]
                for eliminated_pawn in eliminated_pawns:
                    case = self.get_case_board()[eliminated_pawn[0]][eliminated_pawn[1]]
                    if isinstance(case, Case):
                        case.set_color(RED_COLOR)


    def kill_pieces(self, to_return=False) -> Union[list,None]:
        queens_killed = []
        pawns_killed = []

        for row_idx, row in enumerate(self.get_case_board()):
            for col_idx, _ in enumerate(row):
                case = self.get_case_board()[row_idx][col_idx]
                if isinstance(case, Case) and isinstance(case.get_piece(), Piece) and case.get_piece().get_statut() == DEAD:
                    
                    if case.get_piece().get_type() == QUEEN:
                        queens_killed.append(case.get_piece().get_position())
                    elif case.get_piece().get_type() == PAWN:
                        pawns_killed.append(case.get_piece().get_position())

                    case.get_piece().kill_pawn()
                    case.remove_piece()
        
        if to_return:
            return list(queens_killed), list(pawns_killed)
        return None


    def unclick_all_cases(self):
        for row_idx, row in enumerate(self.case_board):
            for col_idx, _ in enumerate(row):
                case = self.case_board[row_idx][col_idx]
                if case.get_color() not in [BEIGE_COLOR, BROWN_COLOR]:
                    case.unclick()

    def __find_occurence_compo(self, compositions:list) -> bool:
        ai_pawns, ai_queens, player_pawns, player_queens = self.count_players_stuff()
        for composition in compositions:
            if isinstance(composition, dict):
                players = list(composition.keys())
                for player in players:
                    opponent = players[0] if player == players[1] else players[1]
                    if composition[player]["queens"] == player_queens and composition[player]["pawns"] == player_pawns and \
                        composition[opponent]["queens"] == ai_queens and composition[opponent]["pawns"] == ai_pawns:
                        return True
        return False

    def cmpt_moves_draw(self) -> None:
        last_move = self.file_manager.get_last_move()
        if last_move != {}:
            piece = last_move["piece"]
            type_movement = last_move["type"]
            if piece == QUEEN and type_movement == TYPE_MOVEMENT:
                self.moves_draw += 1
            else:
                self.moves_draw = 0
    
    def found_draw_compositions(self) -> bool:
        if self.__find_occurence_compo(self.get_draw_compositions()):
            return True
        else:
            return False

    def cmpt_moves_draw_composition(self) -> None: 
        if self.__find_occurence_compo(self.get_draw_compositions_16()):
            self.moves_draw_composition += 1
        else:
            self.moves_draw_composition = 0

    def check_draw(self) -> list:
        grids = self.file_manager.get_all_grids()
        if grids and grids.count(grids[-1]) >= REPETITIVE_POSITION:
            return True, "REPETITIVE POSITION (3 times)"
        
        self.cmpt_moves_draw()
        if self.moves_draw >= MOVES_DRAW:
            return True, "NO MOVES PAWN OR NO ATTACK DURING 25 MOVES"

        if self.found_draw_compositions():
            return True, "DRAW COMPOSITION"

        self.cmpt_moves_draw_composition()
        if self.moves_draw_composition >= MOVES_DRAW_COMPOSITION:
            return True, "DRAW COMPOSITION AFTER 16 MOVES" 
        return False, None
    
    def can_play(self, possibles_moves:dict) -> bool:
        return False if possibles_moves == {} else True   
    

    def game_over(self, possibles_moves:dict, current_player:Player, opponent_player:Player) -> list:
        if current_player.get_pawns() == VIDE and current_player.get_queens() == VIDE:
            statut = WIN + " " + opponent_player.get_name()
            return True, statut
        
        if not self.can_play(possibles_moves):
            statut = WIN + " " + opponent_player.get_name()
            return True, statut
        
        draw, reason = self.check_draw()
        if draw:
            statut = DRAW + " due to " + reason
            return True , statut
        return False, PLAYING 


    def count_board_instance(self) -> int:
        return self.instance_count
    
    def get_file_manager(self) -> FileManager:
        return self.file_manager
    
    def get_ai(self) -> Player:
        return self.ai
    
    def get_player(self) -> Player:
        return self.player
    
    def get_ai_color(self) -> str:
        return self.ai_color
    
    def set_player(self, player:Player) -> None:
        self.player = player

    def set_ai(self, ai:Player) -> None:
        self.ai = ai
    
    def get_player_color(self) -> str:
        return self.player_color
        
    def get_rect(self) -> pygame.Rect:
        return self.rect
    
    def get_case_board(self) -> list:
        return self.case_board
    
    def set_case_board(self, case_board:list) -> None:
        self.case_board = case_board
    
    def get_draw_compositions(self) -> list:
        return self.draw_compositions
    
    def get_draw_compositions_16(self) -> list:
        return self.draw_compositions_16
    
    def get_info_rect(self) -> dict:
        return {
            "rect": self.rect,
            "color": self.rect_color,
            "thickness": self.rect_thickness
        }
    
    def get_info_case(self, row_idx:int, col_idx:int):

        case = self.case_board[row_idx][col_idx]
        piece = case.get_piece()
        if case and isinstance(piece, Piece):
            infopiece = {
                "type": piece.get_type(),
                "color": piece.get_color()
            }
        else:
            infopiece = "Vide"

        return {
            "position": (row_idx, col_idx),
            "color": case.get_color(),
            "piece": infopiece,
        }
                    
    def get_info_case_board(self) -> dict:
        info_case_board = {}

        for row_idx, row in enumerate(self.case_board):
            for col_idx, _ in enumerate(row):
                info_case_board.update(self.get_info_case(row_idx, col_idx))

        return info_case_board
    
    
    def draw(self, screen: pygame.Surface):
        for row_idx, row in enumerate(self.case_board):
            for col_idx, _ in enumerate(row):
                case = self.case_board[row_idx][col_idx]
                case.draw(screen)
        info_rect = self.get_info_rect()
        pygame.draw.rect(screen, info_rect["color"], info_rect["rect"], info_rect["thickness"])