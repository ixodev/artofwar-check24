import random
import pygame as pg
from game_settings import *
from asset_manager import *
from src.task import Task

FONT_PATH = ASSET_MANAGER.get_file_path("HUD/Font/Font.ttf")
FONT_SIZE = 20

TYPING_SPEED = 60


MESSAGEBOX_OK = 0
MESSAGEBOX_OK_CANCEL = 1
MESSAGEBOX_YES_NO = 2
MESSAGEBOX_YES_NO_CANCEL = 3
MESSAGEBOX_OK_YES_STATUS = 4
MESSAGEBOX_NO_STATUS = 5
MESSAGEBOX_CANCEL_STATUS = 6
MESSAGEBOX_STANDARD = 7
MESSAGEBOX_FACESET = 8

MESSAGEBOX_X_OFFSET = 25
MESSAGEBOX_Y_OFFSET = 25


MESSAGEBOX_START_TITLE_X = 25
MESSAGEBOX_START_TITLE_Y = MESSAGEBOX_Y_OFFSET / 2

MESSAGEBOX_MAX_LINES = 4

MESSAGEBOX_MAX_CHARS_TITLE = 15
MESSAGEBOX_DEFAULT_FACESET = "FacesetUnknown"



messagebox_key_strings = {
    MESSAGEBOX_OK: "[Enter] OK",
    MESSAGEBOX_OK_CANCEL: "[Enter] OK   [Esc] Cancel",
    MESSAGEBOX_YES_NO: "[Y] Yes   [N] No",
    MESSAGEBOX_YES_NO_CANCEL: "[Y] Yes   [N] No   [Esc] Cancel"
}

messagebox_keys = {
    MESSAGEBOX_OK: [pg.K_RETURN],
    MESSAGEBOX_OK_CANCEL: [pg.K_RETURN, pg.K_ESCAPE],
    MESSAGEBOX_YES_NO: [pg.K_y, pg.K_n],
    MESSAGEBOX_YES_NO_CANCEL: [pg.K_y, pg.K_n, pg.K_ESCAPE]
}

messagebox_actions = {
    pg.K_RETURN: MESSAGEBOX_OK_YES_STATUS,
    pg.K_ESCAPE: MESSAGEBOX_CANCEL_STATUS,
    pg.K_y: MESSAGEBOX_OK_YES_STATUS,
    pg.K_n: MESSAGEBOX_NO_STATUS
}

messagebox_types = {
    MESSAGEBOX_STANDARD: ASSET_MANAGER.get_file_path("HUD/Dialog/DialogBox.png"),
    MESSAGEBOX_FACESET: ASSET_MANAGER.get_file_path("HUD/Dialog/DialogBoxFaceset.png")
}

messagebox_start_text_coords = {
    MESSAGEBOX_STANDARD: [MESSAGEBOX_X_OFFSET, MESSAGEBOX_Y_OFFSET * 2.3],
    MESSAGEBOX_FACESET: [200, 60]
}

messagebox_max_chars = {
    MESSAGEBOX_STANDARD: 310,
    MESSAGEBOX_FACESET: 260
}

class DialogBox(Task):
    def __init__(self, title: str, text: str, window_hints: int, messagebox_type: int, screen: pg.Surface):
        self.title = title
        self.text = text
        self.window_hints = window_hints
        self.screen = screen
        self.messagebox_type = messagebox_type

        self.font = pg.font.Font(FONT_PATH, FONT_SIZE)
        self.surface = pg.image.load(messagebox_types[self.messagebox_type])

        self.resizing = ((self.screen.get_width() - MESSAGEBOX_X_OFFSET * 2) / self.surface.get_width())

        self.surface = pg.transform.scale(self.surface, (self.surface.get_width() * self.resizing,
                                                         self.surface.get_height() * self.resizing))

        self.current_char_surface = None

        self.clock = pg.time.Clock()

        self.key_string_surface = self.font.render(messagebox_key_strings[self.window_hints], False, [0, 0, 0])

        self.choice = MESSAGEBOX_CANCEL_STATUS

        self.start_x = self.screen.get_width() / 2 - self.surface.get_width() / 2
        self.start_y = self.screen.get_height() / 2 - self.surface.get_height() / 2

        self.check_title_length()
        self.title_surface = self.font.render(self.title, 0, [255, 255, 255])

        self.ellipsis_surface = self.font.render('.', 0, [0, 0, 0])

        self.letter_index = 0

        self.continue_surface = self.font.render("Press space to continue...", 0, [0, 0, 0])

    def check_title_length(self):
        if len(self.title) > MESSAGEBOX_MAX_CHARS_TITLE:
            self.title = self.title[:MESSAGEBOX_MAX_CHARS_TITLE]
            self.title += "..."

    def get_choice(self):
        return self.choice
    
    # Should be overloaded by FacesetBox, to draw the faceset
    def draw_other_stuff(self):
        ...

    def show(self):

        letter_x = self.start_x + messagebox_start_text_coords[self.messagebox_type][0]
        letter_y = self.start_y + messagebox_start_text_coords[self.messagebox_type][1]

        self.screen.blit(self.surface, (self.screen.get_width() / 2 - self.surface.get_width() / 2, 
                                        self.screen.get_height() / 2 - self.surface.get_height() / 2))

        self.screen.blit(self.title_surface, (self.start_x + MESSAGEBOX_START_TITLE_X, self.start_y + MESSAGEBOX_START_TITLE_Y))

        self.draw_other_stuff()

        label_down = self.key_string_surface

        pg.display.flip()

        self.is_running = True
        self.is_typing = True

        self.spacechar = False
        current_line_number = 1

        ellipsis_counter = 0

        press_space_to_continue = False

        while self.is_running:

            self.clock.tick(TYPING_SPEED)

            if self.letter_index > len(self.text) - 1:
                self.is_typing = False

            if self.is_typing:

                if letter_x >= self.start_x + self.surface.get_width() - MESSAGEBOX_X_OFFSET * 2:
                    
                    if letter_y >= self.start_y + self.surface.get_height() - MESSAGEBOX_Y_OFFSET * 4:
                        self.is_typing = False
                        press_space_to_continue = False

                    else:
                        current_line_number += 1

                        letter_y += MESSAGEBOX_Y_OFFSET
                        letter_x = self.start_x + messagebox_start_text_coords[self.messagebox_type][0]

                        if self.text[self.letter_index] == " ":
                            self.spacechar = True
                        else:
                            self.spacechar = False
                else:
                    self.spacechar = False

            if self.is_typing:

                if letter_x >= self.start_x + self.surface.get_width() - MESSAGEBOX_X_OFFSET * 2 - self.ellipsis_surface.get_width() * 4 and current_line_number == MESSAGEBOX_MAX_LINES:
                    
                    ellipsis_counter += 1

                    if ellipsis_counter == 3:
                        ellipsis_counter = 0
                        self.is_typing = False
                        label_down = self.continue_surface
                        press_space_to_continue = True
                    
                    self.current_char_surface = self.font.render('.', False, [0, 0, 0])

                else:
                    self.current_char_surface = self.font.render(self.text[self.letter_index], False, [0, 0, 0])
                    self.letter_index += 1

                self.screen.blit(self.current_char_surface, (letter_x, letter_y))

                if not self.spacechar:
                    letter_x += self.current_char_surface.get_width()

            else:
                self.screen.blit(label_down,
                                 (self.start_x + self.surface.get_width() / 2 - label_down.get_width() / 2,
                                  self.start_y + self.surface.get_height() - MESSAGEBOX_Y_OFFSET * 2))

            pg.display.flip()

            for evt in pg.event.get():
                if evt.type == pg.KEYDOWN:
                    if evt.key == pg.K_ESCAPE:
                        self.choice = MESSAGEBOX_CANCEL_STATUS
                        self.is_running = False
                    if evt.key in messagebox_keys[self.window_hints] and not press_space_to_continue and not self.is_typing:
                        self.choice = messagebox_actions[evt.key]
                        self.is_running = False
                    if evt.key == pg.K_SPACE and press_space_to_continue and not self.is_typing:
                        self.show()

    def run(self):
        self.show()


class MessageBox(DialogBox):
    def __init__(self, title: str, text: str, window_hints: int, screen: pg.Surface):
        super().__init__(title, text, window_hints, MESSAGEBOX_STANDARD, screen)

class FacesetBox(DialogBox):
    def __init__(self, title: str, text: str, window_hints: int,  faceset_image: str, screen: pg.Surface):
        super().__init__(title, text, window_hints, MESSAGEBOX_FACESET, screen)

        self.messagebox_faceset_x = round(7 * self.resizing)
        self.messagebox_faceset_y = round(14 * self.resizing)
        
        if faceset_image == MESSAGEBOX_DEFAULT_FACESET:
            # By default but you can change it if you want
            self.faceset = ASSET_MANAGER.get_surface("FacesetUnknown.png")
        else:
            self.faceset = ASSET_MANAGER.get_surface(f"Facesets/{faceset_image}")

        self.faceset = pg.transform.scale(self.faceset,
                                         (self.faceset.get_width() * self.resizing,
                                          self.faceset.get_height() * self.resizing))


    def draw_other_stuff(self):
        self.screen.blit(self.faceset,
                        (self.start_x + self.messagebox_faceset_x, self.start_y + self.messagebox_faceset_y))