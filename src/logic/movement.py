from data.const import *
from src.board.board import Board, Case, Piece


def _attacks_piece(starting_case: Case, current_piece: Piece, case_board: list, color_player: str, possible_attacks: dict, current_path: list, eliminated_pawns: list) -> dict:
    """Return a dictionary containing all authorized attacks from a piece in the starting case .

    :param starting_case: The case where the piece is located
    :param current_piece: The piece to move
    :param case_board: Array containing all cases of the board
    :param color_player: The color of the player
    :param possible_attacks: Previous dictionary containing all authorized attacks (if recursive call)
    :param current_path: Previous path containing all cases to jump (if recursive call)
    :param eliminated_pawns: Previous list containing all eliminated pawns (if recursive call)
    """

    allowed_movements = MAX_QUEEN_MOVEMENT if current_piece.get_type() == QUEEN else MAX_PAWN_MOVEMENT
    enemy_cases = []

    # Step 1 : Find enemy cases in all directions
    for direction in [NORTH_EAST, NORTH_WEST, SOUTH_EAST, SOUTH_WEST]:
        for distance in range(1, allowed_movements + 1):
            case_found = starting_case.adjacent_cases(case_board, distance, direction)
            piece_found = case_found.get_piece() if isinstance(case_found, Case) else None
            if piece_found:
                if (case_found.row, case_found.col) in eliminated_pawns:
                    break
                if piece_found.get_color() == color_player:
                    break
                if piece_found.get_color() != color_player:
                    enemy_cases.append([case_found, direction])
                    break

    if starting_case.piece and starting_case.piece.get_color() == color_player and current_path == []:
        # Start of the recursion
        current_path += [starting_case.get_position()]

    start_case = case_board[current_path[0][0]][current_path[0][1]]
    num_cases_to_jump = 0

    # Step 2: For each enemy case, find the cases empty in goal to jump
    for enemy_case, direction in enemy_cases:
        cases_to_jump = []
        allowed_dist = 0

        if isinstance(enemy_case, Case):
            if direction == NORTH_EAST:
                vect = (-1, 1)
            elif direction == NORTH_WEST:
                vect = (-1, -1)
            elif direction == SOUTH_EAST:
                vect = (1, 1)
            elif direction == SOUTH_WEST:
                vect = (1, -1)

            row, col = enemy_case.get_position()
            while True:
                row += vect[0]
                col += vect[1]

                if not (0 <= row < len(case_board) and 0 <= col < len(case_board[0])):
                    break

                allowed_dist += 1
                if allowed_dist > allowed_movements:
                    break

                current_case = case_board[row][col]
                if not isinstance(current_case, Case):
                    break

                if current_case.get_piece() and current_case.get_position() != start_case.get_position():
                    break
                
                case_to_jump = enemy_case.adjacent_cases(case_board, allowed_dist, direction)

                if isinstance(case_to_jump, Case):
                    num_cases_to_jump += 1
                    cases_to_jump.append(case_to_jump)

        # Step 3: For each case to jump, call the function recursively (rafle)
        if cases_to_jump:
            for case_to_jump in cases_to_jump:
                if isinstance(case_to_jump, Case) and isinstance(start_case, Case):
                    if not case_to_jump.get_piece() or (case_to_jump.get_position() == start_case.get_position()):
                        new_path = current_path + [case_to_jump.get_position()]
                        new_eliminated_pawns = eliminated_pawns + [enemy_case.get_position()]
                        _attacks_piece(case_to_jump, current_piece, case_board, color_player, possible_attacks, new_path, new_eliminated_pawns)

    # Step 4: If the path is complete, add it to the dictionary
    if len(current_path) > 1 and num_cases_to_jump == 0 and current_path not in possible_attacks.values():
        num_eliminated_pawns = len(eliminated_pawns)

        if possible_attacks == {}:
            max_eliminated_pawns = 0
        else:
            max_eliminated_pawns = max(len(possible_attacks[key]["eliminated_pawns"]) for key in possible_attacks)

        if num_eliminated_pawns >= max_eliminated_pawns:
            path_key = tuple(map(tuple, current_path))
            possible_attacks[path_key] = {
                "path": current_path,
                "piece": start_case.piece,
                "eliminated_pawns": eliminated_pawns,
                "type": TYPE_ATTACK
            }

        # Step 5: If there are several paths with different number of eliminated pawns, keep only the maximum
        rafle_results_copy = possible_attacks.copy()
        max_eliminated_pawns = max(len(rafle_results_copy[key]["eliminated_pawns"]) for key in rafle_results_copy)

        for key in rafle_results_copy.keys():
            if len(rafle_results_copy[key]["eliminated_pawns"]) < max_eliminated_pawns:
                del possible_attacks[key]

    return possible_attacks


def _movement_piece(starting_case: Case, current_piece: Piece, case_board: list, color_player: str, board:Board) -> dict:
    """Return a dictionary containing all authorized movements from the starting case.

    :param starting_case: The case where the piece is located
    :param current_piece: The piece to move
    :param case_board: The board of the game
    :param color_player: The color of the player
    :param board: The board of the game
    :return: A dictionary containing all authorized movements from the starting case
    """
    listCase = {}
    type_piece = current_piece.get_type()
    starting_piece = starting_case.get_piece()

    if starting_piece and starting_piece.get_color() == color_player:
        allowed_movements = MAX_QUEEN_MOVEMENT if type_piece == QUEEN else MAX_PAWN_MOVEMENT
        cases_to_move = []

        if type_piece == QUEEN:
            directions = [NORTH_WEST, NORTH_EAST, SOUTH_WEST, SOUTH_EAST]

        elif type_piece == PAWN:
            directions = [SOUTH_WEST, SOUTH_EAST] if color_player == board.get_ai_color() else [NORTH_WEST, NORTH_EAST]

        for direction in directions:
            for distance in range(1, allowed_movements + 1):
                case_found = starting_case.adjacent_cases(case_board, distance, direction)
                if isinstance(case_found, Case):
                    if case_found.get_piece():
                        break
                    elif not case_found.get_piece():
                        cases_to_move.append(case_found)

        if cases_to_move:
            for case in cases_to_move:
                if isinstance(case, Case):
                    key = tuple(map(tuple, [starting_case.get_position(), case.get_position()]))
                    listCase[key] = {
                        "path": [starting_case.get_position(), case.get_position()],
                        "piece": starting_case.get_piece(),
                        "piece_type": starting_case.get_piece().get_type(),
                        "case": case.get_position(),
                        "type": TYPE_MOVEMENT
                    }

    return listCase


def available_moves(board: Board, color_player: str) -> dict:
    """Return a dictionary containing all available movements and attacks from the player.

    :param board: The board of the game
    :param color_player: The color of the player
    """
    
    available_attacks = {}
    available_movements = {}

    case_board = board.get_case_board()

    # Step 1 : Attacks
    for row_idx,row in enumerate(case_board):
        for col_idx, _ in enumerate(row):
            current_case = case_board[row_idx][col_idx]
            if isinstance(current_case, Case) and current_case.get_piece() and current_case.get_piece().get_color() == color_player:
                paths = []
                eliminated_pawns = []
                attacks = _attacks_piece(current_case, current_case.get_piece(), case_board, color_player, available_attacks, paths, eliminated_pawns)
                available_attacks.update(attacks)
    
    # Step 2 : Movements
    if available_attacks == {}:
        for row_idx,row in enumerate(case_board):
            for col_idx, _ in enumerate(row):
                current_case = case_board[row_idx][col_idx]
                if isinstance(current_case, Case) and current_case.get_piece() and current_case.get_piece().get_color() == color_player:
                    moves = _movement_piece(current_case, current_case.get_piece(), case_board, color_player, board)
                    available_movements.update(moves)
        available_movements_sorted = dict(sorted(available_movements.items(), key=lambda item: (item[1]["piece_type"] != QUEEN, item[1]["piece_type"])))

    return available_attacks if available_attacks != {} else available_movements_sorted


def get_type_play(availables_moves:dict) -> str:
    """
    Return the type of play (movement or attack) from the availables moves

    :param availables_moves: The dictionary containing all available movements and attacks from the player
    """
    for key in availables_moves.keys():
        return availables_moves[key]["type"]