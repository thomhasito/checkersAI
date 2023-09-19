from data.const import *

class Player:

    def __init__(self, name:str, color:str):
        self.name = name
        self.color = color
        self.turn = True if self.get_color() == WHITE else False
        self.max_player = False if self.get_name() == AI_NAME else True
        self.pawns = None
        self.queens = None
        self.winner = False
    
    def get_name(self):
        return self.name
    
    def get_color(self):
        return self.color
    
    def get_info_player(self) -> dict:
        return {
            "name": self.get_name(),
            "color": self.get_color(),
            "max_player": self.max_player,
            "turn": self.is_turn(),
            "winner": self.winner
        }
    
    def is_turn(self):
        return self.turn
    
    def set_turn(self, turn:bool):
        self.turn = turn
    
    def get_queens(self) -> int:
        return self.queens
    
    def get_pawns(self) -> int:
        return self.pawns

    def set_pawns(self, nb_pawns:int):
        self.pawns = nb_pawns

    def set_queens(self, nb_queens:int):
        self.queens = nb_queens

    def set_winner(self, winner:bool):
        self.winner = winner

    def is_winner(self) -> bool:
        return self.winner
    
    def is_max_player(self) -> bool:
        return self.max_player