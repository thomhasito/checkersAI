import pygame

from data.const import *
from src.board.piece import Piece
from typing import Union

class Case:

    instance_count = 0

    def __init__(self, row, col, color):
        Case.instance_count += 1
        self.row = row
        self.col = col
        self.color = color
        self.piece = None
        self.rect = pygame.Rect(self.col * SQUARE_SIZE + BOARD_X_OFFSET, self.row * SQUARE_SIZE + BOARD_Y_OFFSET, SQUARE_SIZE, SQUARE_SIZE)
        self.selected = False


    def adjacent_cases(self, case_board:list, distance:int, direction:str=None) -> Union[list, object]:
        adjacent_cases = []

        if direction:
            if not direction in [NORTH_EAST, NORTH_WEST, SOUTH_EAST, SOUTH_WEST]:
                raise ValueError(f"direction inconnue")

        for row_idx, row in enumerate(case_board):
            for col_idx, _ in enumerate(row):
                case = case_board[row_idx][col_idx]
                if isinstance(case, Case):
                    row_diff = self.row - case.row
                    col_diff = self.col - case.col

                    to_append = None

                    if row_diff == distance and col_diff == -distance:
                        if direction is None:
                            case_direction = NORTH_EAST
                            to_append = [case, case_direction]
                        elif direction == NORTH_EAST:
                            return case

                    elif row_diff == distance and col_diff == distance:
                        if direction is None:
                            case_direction = NORTH_WEST
                            to_append = [case, case_direction]
                        elif direction == NORTH_WEST:
                            return case

                    elif row_diff == -distance and col_diff == -distance:
                        if direction is None:
                            case_direction = SOUTH_EAST
                            to_append = [case, case_direction]
                        elif direction == SOUTH_EAST:
                            return case

                    elif row_diff == -distance and col_diff == distance:
                        if direction is None:
                            case_direction = SOUTH_WEST
                            to_append = [case, case_direction]
                        elif direction == SOUTH_WEST:
                            return case

                    if to_append:
                        adjacent_cases.append(to_append)

        return adjacent_cases
    
    def get_rect(self) -> pygame.Rect:
        return self.rect
    
    def get_piece(self) -> Union[None, Piece]:
        if self.piece == VIDE:
            return None
        return self.piece
    
    def set_piece(self, piece:Piece) -> None:
        self.piece = piece

    def remove_piece(self) -> None:
        self.piece = VIDE

    def get_color(self) -> str:
        return self.color
    
    def set_color(self, color:str) -> None:
        self.color = color

    def get_position(self) -> tuple:
        return (self.row, self.col)
    
    def is_selected(self) -> bool:
        return self.selected
    
    def is_mouse_hover(self, mouse_pos:tuple) -> bool:
        return self.get_rect().collidepoint(mouse_pos)
    
    def is_clicked(self, mouse_pos:tuple) -> bool:
        return self.get_rect().collidepoint(mouse_pos)

    def origin_color(self) -> None:
        self.set_color(BEIGE_COLOR) if (self.row + self.col) % 2 == 0 else self.set_color(BROWN_COLOR)
        

    def click(self):   
        if not self.is_selected():
            self.selected = True
            if self.color in [BEIGE_COLOR, BROWN_COLOR]:
                self.set_color(YELLOW_COLOR)

            
    def unclick(self):
        self.origin_color()
        if self.is_selected():
            self.selected = False
 

    def draw(self, screen:pygame.Surface):
        pygame.draw.rect(screen, self.get_color(), pygame.Rect(self.get_rect()))
        # font = pygame.font.Font(None, 20)
        # text = font.render(f"({self.row}, {self.col})", True, (0, 0, 0))
        # screen.blit(text, (self.rect.x + 5, self.rect.y + 5))
        if self.piece:
            x = self.rect.x + SQUARE_SIZE // 2
            y = self.rect.y + SQUARE_SIZE // 2
            self.piece.draw(screen, x, y)