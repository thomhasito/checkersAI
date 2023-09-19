import pygame, time

from data.const import *
from src.board.board import Board
from src.board.case import Case
from src.board.piece import Piece
from src.display.button import Button
from src.board.player import Player
from typing import Union
from functools import wraps


def interval_time(seconds):
    def decorator(func):
        last_call_time = 0

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal last_call_time
            current_time = time.time()
            
            if current_time - last_call_time >= seconds:
                result = func(*args, **kwargs)
                if result == True:
                    last_call_time = current_time
                return result
            
            return False 
        return wrapper
    return decorator

class EventManager:

    def __init__(self, board:Board, player: Player, surrender_button:Button, exit_button:Button):
        self.events = []
        self.board = board
        self.player = player
        self.mouse_pos = None
        self.hovered_case = None
        self.surrender_button = surrender_button
        self.exit_button = exit_button

    def set_mouse_pos(self) -> tuple:
        self.mouse_pos = pygame.mouse.get_pos()
        
    def get_mouse_pos(self) -> Union[None, tuple]:
        return self.mouse_pos
    
    def ensure_mouse_in_board(self) -> bool:
        return self.board.get_rect().collidepoint(self.mouse_pos)

    def get_hovered_case(self) -> Union[None, Case]:
        if self.mouse_pos:
            if self.ensure_mouse_in_board():
                case_board = self.board.case_board
                for row_idx, row in enumerate(case_board):
                    for col_idx, _ in enumerate(row):
                        case = self.board.case_board[row_idx][col_idx]
                        if case.is_mouse_hover(self.mouse_pos):
                            self.hovered_case = case
                            return self.hovered_case
        return None
    
    def get_events(self) -> list:
        return self.events

    def set_events(self) -> list:
        self.events = pygame.event.get()
    
    def get_board(self) -> Board:
        return self.board
    
    def get_surrender_button(self) -> Button:
        return self.surrender_button
    
    def get_exit_button(self) -> Button:
        return self.exit_button

    def clear_events(self):
        self.events.clear()

    def quit_event(self) -> bool:
        for event in self.get_events():
            if isinstance(event, pygame.event.Event) and event.type == pygame.QUIT:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.get_mouse_pos():
                    if self.get_exit_button().get_rect().collidepoint(self.get_mouse_pos()):
                        return True  
        return False
    
    def surrender(self) -> bool:
        for event in self.get_events():
            if isinstance(event, pygame.event.Event) and event.type == pygame.MOUSEBUTTONDOWN:
                if self.get_mouse_pos():
                    if self.get_surrender_button().get_rect().collidepoint(self.get_mouse_pos()):
                        return True
        return False
    
    def clear_display_button(self) -> None:
        self.get_surrender_button().set_around_color((0, 0, 0))
        self.get_surrender_button().set_text_color((0, 0, 0))
        self.get_exit_button().set_around_color((0, 0, 0))
        self.get_exit_button().set_text_color((0, 0, 0))
    
    def event_display_button(self) -> bool:
        for event in self.get_events():
            if isinstance(event, pygame.event.Event) and event.type == pygame.MOUSEMOTION:
                self.set_mouse_pos()
                if self.get_exit_button().get_rect().collidepoint(self.get_mouse_pos()):
                    self.get_exit_button().set_around_color((255, 0, 0))
                    self.get_exit_button().set_text_color((255, 0, 0))
                    return True

                elif self.get_surrender_button().get_rect().collidepoint(self.get_mouse_pos()):
                    self.get_surrender_button().set_around_color((255, 0, 0))
                    self.get_surrender_button().set_text_color((255, 0, 0))
                    return True
                else:
                    if self.get_exit_button().get_around_color() == (255, 0, 0) or self.get_surrender_button().get_around_color() == (255, 0, 0):
                        self.clear_display_button()
                        return True
        return False

    
    @interval_time(0.2)
    def event_case(self, case: Case, board:Board) -> bool:
    
        piece = case.get_piece()

        if isinstance(piece, Piece) and piece.get_color() == self.player.get_color():
            if not case.is_selected() and not self.get_board().get_selected_case(ending=False):
                case.click()
                return True

            elif case.is_selected() and case.get_color() == YELLOW_COLOR:
                board.unclick_all_cases()
                return True
            
            elif (isinstance(self.get_board().get_selected_case(ending=False), Case)
                  and case.get_position() != self.get_board().index_case_selected(ending=False)):
                board.unclick_all_cases()
                case.click()
                return True
            
        if case.get_color() in [GREEN_COLOR, YELLOW_GREEN_COLOR]:
            if case.get_color() == YELLOW_GREEN_COLOR and case.is_selected():
                case.set_color(GREEN_COLOR)
            case.click()
            return True
            
        return False
    

    def event_board(self) -> bool:
        events = self.get_events()
        self.set_mouse_pos()
        global hovered_case
        previous_hovered_case = hovered_case

        if not self.ensure_mouse_in_board():
            return False
        
        for event in events:
            if isinstance(event, pygame.event.Event):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for row_idx, row in enumerate(self.board.case_board):
                        for col_idx, _ in enumerate(row):
                            case = self.board.case_board[row_idx][col_idx]
                            if case.is_clicked(self.get_mouse_pos()):
                                if self.event_case(case, self.board):
                                    return True
                            
                elif event.type == pygame.MOUSEMOTION:
                    hovered_case = self.get_hovered_case()
                    if hovered_case and previous_hovered_case and previous_hovered_case != hovered_case:
                        return True
                    
        return False