from random import randint
from button import Button
from matrix import *
import pygame
from pygame.locals import *
from design import *
from save import *

class Main:
    def __init__(self):
        self.local_save = Save()
        self.button_list = []
        self.counter = 0
        self.score = self.local_save.get_data(1) # get data from save.py and '1' is the index in data list
        self.win = self.local_save.get_data(2)
        self.loose = self.local_save.get_data(3)

        self.previous_line = 0
        self.previous_column = 0
        self.code_matrix = None

        self.matrix_len_bounds = [4, 5]
        self.sequence_len_bounds = [3, 4]

        self.generate_game_level()
        self.ds = Design()
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) # create a full screen window
        self.draw_game_level()
        self.loop()
     
    def generate_game_level(self):
        self.update_difficulty()
        matrix_len = randint(self.matrix_len_bounds[0], self.matrix_len_bounds[1]) # set random size for the matrix
        sequence_len = randint(self.sequence_len_bounds[0], self.sequence_len_bounds[1]) # set random size for the sequence

        self.code_matrix = CodeMatrix(matrix_len, sequence_len) # by default : matrix_len = 5 and seq_len = 4
        self.code_matrix.create_code_matrix() # create the matrix
        self.code_matrix.generate_sequence() # create the sequence
        self.code_matrix.show_code_matrix() # show matrix in console or terminal
        self.code_matrix.show_sequence() # show sequence in console or terminal

    def draw_game_level(self):
        self.screen.fill(self.ds.matrix_plane_color) # set the background color of the window
        self.ui_score()
        self.ui_matrix()
        self.ui_sequence()

    def new_game(self):
        print("NEW GAME")
        self.button_list.clear() # clear the button list to avoid, possibly, click on deleted button
        self.counter = 0

        self.previous_line = 0
        self.previous_column = 0
        self.code_matrix = None

        self.generate_game_level()
        self.draw_game_level()

    # explications of ui drawing (text and rectangle = plane) are in button.py
    def ui_score(self):
        # Plane
        font_size = self.ds.score_font_size
        plane = pygame.Rect((0, 0), (self.screen.get_width(), 2*font_size)) 
        pygame.draw.rect(self.screen, self.ds.border_color, plane, 2)
        
        # Score
        font = pygame.font.SysFont('calibri', font_size, True, False)
        score_text = font.render(str(self.score), True, self.ds.score_text_color)
        self.screen.blit(score_text, score_text.get_rect(center = plane.center))

        # Win rate
        font_size = self.ds.win_rate_font_size
        font = pygame.font.SysFont('calibri', font_size, True, False)

        win_rate = 0
        try: # the try allows to avoid, when launching the game for the first time, dividing by 0
            win_rate = int(self.win/(self.win+self.loose)*100)
        except Exception:
            print("Diving by 0")

        score_text = font.render(f"Win rate : {win_rate} %", True, self.ds.win_rate_text_color)
        self.screen.blit(score_text, (font_size//2, plane.centery - font_size//2))

    def ui_matrix(self):
        # Plane
        plane = pygame.Rect((0, 2*self.ds.score_font_size), (self.screen.get_width(), self.screen.get_height() - 2*self.ds.sequence_size - 2*self.ds.score_font_size)) # pygame object for storing rectangular coordinates
        pygame.draw.rect(self.screen, self.ds.matrix_plane_color, plane) # draw a rectangle

        # Title
        font = pygame.font.SysFont('calibri', self.ds.matrix_font_size, True, False)
        ui_text = font.render("CODE MATRIX", True, self.ds.matrix_text_color)
        self.screen.blit(ui_text, (plane.centerx - ui_text.get_width()//2, plane.top + self.ds.matrix_margin))

        # Matrix
        matrix_len = self.code_matrix.get_matrix_len()
        for l in range(matrix_len):
            for c in range(matrix_len):
                self.button_list.append(Button(str(self.code_matrix.get_code(l, c)), (plane.width, plane.height), matrix_len, l, c))
                self.button_list[len(self.button_list)-1].draw(self.screen)
        # every button are added in a list to check later if there are clicked

    def ui_sequence(self): 
        # Plane
        size = self.ds.sequence_size
        plane = pygame.Rect((0, self.screen.get_height()-2*size), (self.screen.get_width(), 2*size))
        pygame.draw.rect(self.screen, self.ds.sequence_text_color, plane, 2)

        # Title
        marge = self.ds.sequence_margin
        font_size = self.ds.sequence_font_size
        font = pygame.font.SysFont('calibri', font_size, True, False)
        ui_text = font.render("SEQUENCE REQUIRED TO UPLOAD", True, self.ds.sequence_text_color)
        self.screen.blit(ui_text, (size, plane.top + marge))

        # Sequence
        for i in range(self.code_matrix.get_seq_len()):
            ui_text = font.render(str(self.code_matrix.get_sequence(i)), True, self.ds.sequence_text_color)
            self.screen.blit(ui_text, (size + size*i, plane.bottom - font_size - marge//2))

    # this function verify, according to counter value, if the button clicked is on the same line or same column than the previous click
    # for the first click, you must click on the first so we have : "elif self.counter != 0"
    # after the first click, you must click on the same column so counter is odd for column and even for line. We use : "self.counter%2 == 0" 
    def on_same_line_or_column(self, button_list):
            if self.counter%2 == 0:
                if self.counter == 0 and button_list.get_pos()[0] == 0:
                    self.previous_line = button_list.get_pos()[0]
                    self.previous_column = button_list.get_pos()[1]
                    return True
                elif self.counter != 0:
                    if button_list.get_pos()[0] != self.previous_line:
                        return False
                    self.previous_line = button_list.get_pos()[0]
                    self.previous_column = button_list.get_pos()[1]
                    return True
            elif button_list.get_pos()[1] == self.previous_column:
                self.previous_line = button_list.get_pos()[0]
                self.previous_column = button_list.get_pos()[1]
                return True
            else:
                return False
        
    def update_difficulty(self):
        if self.score <= 10:
            self.matrix_len_bounds = [4, 5]
            self.sequence_len_bounds = [3, 4]
        elif self.score <= 20:
            self.matrix_len_bounds = [6, 8]
            self.sequence_len_bounds = [6, 7]
        else:
            self.matrix_len_bounds = [8, 10]
            self.sequence_len_bounds = [8, 9]


    def loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # if escape button is pressed and released
                    running = False # and of the game : you leave it
                for i in range(len(self.button_list)): # we check every button
                    if event.type == pygame.MOUSEBUTTONDOWN and self.button_list[i].mouse_over_button() and not self.button_list[i].is_already_click(): # if the mouse button is pressed and released on a matrix button and this button is not already click
                        self.button_list[i].put_it_already_click(True) # we set this matrix button already clicked
                        if self.button_list[i].code == self.code_matrix.get_sequence(self.counter) and self.on_same_line_or_column(self.button_list[i]): # if the matrix button value match with the corresponding sequence value and if his location is correct
                            self.counter += 1 
                            self.button_list[i].draw_click(self.screen) # the button is redraw with "already clicked" design
                            print("GOOD MOVE")
                        else:
                            self.score -= 1
                            self.loose += 1
                            self.ui_score() # the score ui is update
                            print("BAD MOVE")
                            self.new_game() # the game is relaunched 
                            break

            self.update_difficulty()

            if self.counter == self.code_matrix.get_seq_len():
                self.score += 1
                self.win += 1
                print(f"SCORE : {self.score}")
                self.new_game()

            pygame.display.update()

        self.local_save.save_data((self.score, self.win, self.loose)) # save data as the score, the number of win and loose
        pygame.quit()

main = Main()