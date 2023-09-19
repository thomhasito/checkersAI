import pygame

from data.const import *
from src.board.player import Player

class Piece:
    PIECE_RADIUS = SQUARE_SIZE // 3

    instance_count = 0

    def __init__(self, type:str, color:str, row_idx:int, col_idx:int, grid_value: int):
        Piece.instance_count += 1
        self.type = type
        self.movement = self.get_movement()
        self.color = color
        self.row_idx = row_idx
        self.col_idx = col_idx
        self.grid_value = grid_value
        self.statut = ALIVE


    def __str__(self) -> str:
        return f"{self.color} {self.type} at position: {self.get_position()}"
    
    def get_type(self) -> str:
        return self.type

    def get_movement(self) -> int:
        if self.type not in [PAWN,QUEEN]:
            raise ValueError(f"Unknown type piece expected '{PAWN}' or '{QUEEN}', got '{self.type}'")
        if self.type == PAWN:
            self.movement = MAX_PAWN_MOVEMENT
        elif self.type == QUEEN:
            self.movement = MAX_QUEEN_MOVEMENT
        return self.movement
    
    def get_color(self) -> str:
        return self.color
    
    def get_grid_value(self) -> int:
        return self.grid_value
    
    def get_position(self)-> tuple:
        return (self.row_idx,self.col_idx)

    def set_position(self, row_idx, col_idx) -> None:
        self.row_idx = row_idx
        self.col_idx = col_idx

    def get_statut(self) -> str:
        return self.statut
    
    def set_statut(self, statut:str) -> None:
        self.statut = statut
    
    def promo_queen(self, player:Player) -> None:
        self.type = QUEEN
        self.movement = self.get_movement()
        self.grid_value = PLAYER_QUEEN if player.get_color() == self.get_color() else AI_QUEEN 
    
    def draw(self, window :pygame.Surface, x:int, y:int) -> None:
        if self.type == PAWN:
            pygame.draw.circle(window, self.get_color(), (x, y), self.PIECE_RADIUS)
        elif self.type == QUEEN:
            pygame.draw.circle(window, self.get_color(), (x, y), self.PIECE_RADIUS + 5)
            pygame.draw.rect(window, self.get_color(), pygame.Rect(x - 25, y, 50, 25))
            # image_crown_queen = pygame.image.load(QUEEN_CROWN_IMAGE)
            # fond = image_crown_queen.convert_alpha()
            # window.blit(fond,(x-fond.get_width()//2, y-fond.get_height()//2 - 3))
    
    def kill_pawn(self) -> None:
        Piece.instance_count -= 1
        del self