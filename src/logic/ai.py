import re

from data.const import *
from src.board.board import Board
from src.board.case import Case
from src.board.piece import Piece
from src.board.player import Player
from src.logic.movement import available_moves, get_type_play
from copy import deepcopy
from typing import Union

def score_pawn_initial_row(piece:Piece, player:Player, ai:Player, game_phase:str) -> int:
    """
    Score a pawn if it is in the initial row of the player or the ai

    :param piece: The piece selected
    :param player: The player
    :param ai: The ai
    :param game_phase: The game phase
    """
    protecting_row = None
    if piece.get_color() != player.get_color():
        protecting_row = 0 
    elif piece.get_color() == ai.get_color():
        protecting_row = NB_ROWS - 1
    if piece.get_type() == PAWN and protecting_row:
        row_piece = piece.get_position()[0]
        if row_piece == protecting_row:
            if game_phase == MIDDLE_GAME or game_phase == SLOW_END_GAME:
                return piece.get_grid_value() * 5
            if game_phase == OPENING:
                return piece.get_grid_value() * 2
    return 0

def score_edge(piece:Piece, game_phase:str) -> int:
    """
    Score a pawn if it is on the edge of the board
    
    :param piece: The piece selected
    :param game_phase: The game phase
    """
    if piece.get_type() == PAWN:
        col_piece = piece.get_position()[1]
        if col_piece == 0 or col_piece == NB_COLS - 1:
            if game_phase == MIDDLE_GAME:
                return piece.get_grid_value() * 5
            if game_phase == OPENING:
                return piece.get_grid_value() * 2
    return 0

def calculate_line_difference(case_board:list, player_color:str, ai_color:str) -> int:
    """
    Calculate the difference between the advanced pawns of the player and the ai
    
    :param case_board: Array of cases of the board
    :param player_color: The player color
    :param ai_color: The ai color
    """
    ai_score = 0
    player_score = 0

    for row_idx, row in enumerate(case_board):
        for col_idx, _ in enumerate(row):
            case = case_board[row_idx][col_idx]
            if isinstance(case, Case) and case.get_piece():
                if case.get_piece().get_color() == ai_color:
                    ai_score += (row_idx + 1)
                elif case.get_piece().get_color() == player_color:
                    player_score += (NB_ROWS - row_idx)

    return ai_score - player_score


def score_piece_in_center(piece:Piece, game_phase: str) -> int:
    """
    Score a piece if it is in the center of the board
    
    :param piece: The piece selected
    :param game_phase: The game phase
    """
    if piece.get_position() in [(4,3), (5,4), (4,5), (5,6)]:
        if game_phase == OPENING:
            return piece.get_grid_value() * 10
        elif game_phase == MIDDLE_GAME:
            return piece.get_grid_value() * 3
        elif game_phase == SLOW_END_GAME:
            return piece.get_grid_value() * 2
        elif game_phase == FAST_END_GAME and piece.get_type() == QUEEN:
            return piece.get_grid_value() * 10
    return 0


def score_pieces_protected(piece:Piece, phase:str) -> int:
    if piece.get_type() == PAWN:
        if phase == OPENING:
            return piece.get_grid_value() * 5
        elif phase == MIDDLE_GAME:
            return piece.get_grid_value() * 10
        elif phase == SLOW_END_GAME or phase == FAST_END_GAME:
            return piece.get_grid_value() * 3
        
    return 0
    
                

def evaluate(board:Board, player:Player, ai:Player) -> int:
    """
    Evaluate the board and return a score
    
    :param board: The board of the game
    :param player: The player
    :param ai: The ai
    """
    score = 0
    ai_pawns, ai_queens, player_pawns, player_queens = board.count_players_stuff()
    phase = board.game_phase(ai_pawns, ai_queens, player_pawns, player_queens)
    multiplicator = 0
    if phase == OPENING:
        multiplicator = 200
    elif phase == MIDDLE_GAME:
        multiplicator = 300
    elif phase == FAST_END_GAME:
        multiplicator = 400
        ai_queens *= 2
        player_queens *= 2
    elif phase == SLOW_END_GAME:
        multiplicator = 400
    score += (board.static_evaluation(ai_pawns, ai_queens, player_pawns, player_queens) * multiplicator)
    
    if phase == OPENING:
        score += (calculate_line_difference(board.get_case_board(), player.get_color(), ai.get_color()) * 2)
    elif phase == MIDDLE_GAME:
        score += (calculate_line_difference(board.get_case_board(), player.get_color(), ai.get_color()) * 3)
    elif phase == FAST_END_GAME:
        score += (calculate_line_difference(board.get_case_board(), player.get_color(), ai.get_color()) * 5)
    elif phase == SLOW_END_GAME:
        score += (calculate_line_difference(board.get_case_board(), player.get_color(), ai.get_color()) * 10)
    

    case_board = board.get_case_board()
    for row_idx, row in enumerate(case_board):
        for col_idx, _ in enumerate(row):
            case = case_board[row_idx][col_idx]
            if isinstance(case, Case) and isinstance(case.get_piece(), Piece):
                piece = case.get_piece()
                score += score_pawn_initial_row(piece, player, ai, phase)
                score += score_edge(piece, phase)
                score += score_piece_in_center(piece, phase)
                if row_idx != 0 and row_idx != NB_ROWS - 1 and col_idx != 0 and col_idx != NB_COLS - 1:
                    if case.get_piece().get_color() == player.get_color():
                        case_gauche = case_board[row_idx + 1][col_idx - 1]
                        case_droite = case_board[row_idx + 1][col_idx + 1]
                        if isinstance(case_gauche, Case) and isinstance(case_droite, Case):
                            if isinstance(case_gauche.get_piece(), Piece) and isinstance(case_droite.get_piece(), Piece):
                                if (case_gauche.get_piece().get_color() == player.get_color()
                                    and case_droite.get_piece().get_color() == player.get_color()):
                                    score += score_pieces_protected(piece, phase)
                    elif case.get_piece().get_color() == ai.get_color():
                        case_gauche = case_board[row_idx - 1][col_idx - 1]
                        case_droite = case_board[row_idx - 1][col_idx + 1]
                        if isinstance(case_gauche, Case) and isinstance(case_droite, Case):
                            if isinstance(case_gauche.get_piece(), Piece) and isinstance(case_droite.get_piece(), Piece):
                                if (case_gauche.get_piece().get_color() == ai.get_color()
                                    and case_droite.get_piece().get_color() == ai.get_color()):
                                    score += score_pieces_protected(piece, phase)
    return score
    
def simulate_move(board:Board, case_origin:Case, case_desti:Case, eliminated_pawns:Union[list,None]) -> Board:
    """
    Simulate a move on the board
    
    :param board: The board of the game
    :param case_origin: The case of the piece to move
    :param case_desti: The case of the destination
    :param eliminated_pawns: The list of eliminated pawns (if there is any)
    """
    board.move_piece(case_origin, case_desti, case_origin.get_piece())
    if eliminated_pawns:
        case_board = board.get_case_board()
        for (case_row,case_col) in eliminated_pawns:
            case_to_remove_piece = case_board[case_row][case_col]
            if isinstance(case_to_remove_piece, Case) and isinstance(case_to_remove_piece.get_piece(), Piece):
                case_to_remove_piece.get_piece().set_statut(DEAD)
        board.kill_pieces(to_return=False)
    return board


def get_all_possible_boards(board:Board, possibles_moves:dict) -> list:
    """
    Return all possible boards that can be generated from the current board in the next move

    :param board: The board of the game
    :param possibles_moves: The dictionary of possible moves
    """
    all_boards = []
    for key in possibles_moves.keys():
        path = possibles_moves[key]["path"]
        if get_type_play(possibles_moves) == TYPE_ATTACK:
            eliminated_pawns = possibles_moves[key]["eliminated_pawns"]
        else:
            eliminated_pawns = None

        temp_board = deepcopy(board)
        temp_case_board = temp_board.get_case_board()
        temp_case_origin = temp_case_board[path[0][0]][path[0][1]]
        temp_case_desti = temp_case_board[path[-1][0]][path[-1][1]]
        if isinstance(temp_case_origin, Case) and isinstance(temp_case_desti, Case):
            temp_piece = temp_case_origin.get_piece()
            new_board = simulate_move(temp_board, temp_case_origin, temp_case_desti, eliminated_pawns)
            movement = {
                "piece": temp_piece.get_color() + temp_piece.get_type(),
                "type": get_type_play(possibles_moves),
                "origin": temp_case_origin.get_position(),
                "destination": temp_case_desti.get_position(),
                "eliminated_pawns": eliminated_pawns if eliminated_pawns else None,
            }
            all_boards.append([new_board, movement])

    return all_boards


def alphabeta(board:Board, movement:dict, player:Player, ai:Player, max_player: bool, depth: int, alpha: float, beta: float, ai_complexity:str):
    """
    Return the best board and the best movement from the current board to allow the ai to play
    
    :param board: The board of the game
    :param movement: The path best movement
    :param player: The player
    :param ai: The ai
    :param max_player: True if current player is the player, False otherwise
    :param depth: The depth of the tree
    :param alpha: The alpha value (float('-inf'))
    :param beta: The beta value (float('inf'))
    :param ai_complexity: The complexity of the ai could be easy, medium or hard
    """
    total_explored = 0
    if max_player:
        current_player = player
        opponent_player = ai
    else:
        current_player = ai
        opponent_player = player

    possibles_moves = available_moves(board, current_player.get_color())
    game_over, game_statut = board.game_over(possibles_moves, current_player, opponent_player)

    if depth == 0 or (game_over and game_statut != PLAYING):
        if not game_over:
            if ai_complexity == LEVEL_EASY or ai_complexity == LEVEL_MEDIUM:
                score = board.static_evaluation(*board.count_players_stuff())
            elif ai_complexity == LEVEL_HARD:
                score = evaluate(board, player, ai)
        else:
            if re.search(rf"{DRAW}", game_statut):
                score = 0
            elif re.search(rf"{WIN}", game_statut):
                win_score_player = 1000000
                win_score_ai = -1000000
                
                if re.search(rf"{player.get_name()}", game_statut):
                    score = win_score_player
                elif re.search(rf"{ai.get_name()}", game_statut):
                    score = win_score_ai
            else:
                raise ValueError(f"game_statut inconnu")
            
        return score, board, movement, 1  # Retourne 1 pour indiquer la fin d'un chemin
    
    if max_player:
        maxEval = float('-inf')
        best_board = None
        best_movement = None
        all_possible_boards = get_all_possible_boards(board, possibles_moves)

        for possible_board, possible_movement in all_possible_boards:
            evaluation, _, _, explored = alphabeta(possible_board, possible_movement, player, ai, not max_player, depth - 1, alpha, beta, ai_complexity)
            maxEval = max(maxEval, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
            if maxEval == evaluation:
                best_board = possible_board
                best_movement = possible_movement
            total_explored += explored

        return maxEval, best_board, best_movement, total_explored
    else:
        minEval = float('inf')
        best_board = None
        best_movement = None
        all_possible_boards = get_all_possible_boards(board, possibles_moves)

        for possible_board, possible_movement in all_possible_boards:
            evaluation, _, _, explored = alphabeta(possible_board, possible_movement, player, ai, not max_player, depth - 1, alpha, beta, ai_complexity)
            minEval = min(minEval, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
            if minEval == evaluation:
                best_board = possible_board
                best_movement = possible_movement  
            total_explored += explored

        return minEval, best_board, best_movement, total_explored