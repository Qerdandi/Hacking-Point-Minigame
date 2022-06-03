from random import randint
from button import Button
from matrix import *
import pygame
from pygame.locals import *
from design import *

class Main:
    def __init__(self):
        self.button_list = []
        self.score = 0
        self.counter = 0

        self.previous_line = 0
        self.previous_column = 0
        self.code_matrix = None

        self.matrix_len_bounds = [4, 5]
        self.sequence_len_bounds = [4, 4]
        
        self.generate_game_level()
        self.ds = Design()
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.draw_game_level()
        self.loop()

    def generate_game_level(self):
        matrix_len = randint(self.matrix_len_bounds[0], self.matrix_len_bounds[1])
        sequence_len = randint(self.sequence_len_bounds[0], self.sequence_len_bounds[1])

        self.code_matrix = CodeMatrix(matrix_len, sequence_len) # by default : matrix_len = 5 and seq_len = 4
        self.code_matrix.create_code_matrix()
        self.code_matrix.generate_sequence()
        self.code_matrix.show_code_matrix()
        self.code_matrix.show_sequence()

    def draw_game_level(self):
        self.screen.fill(self.ds.matrix_plane_color)
        self.ui_score()
        self.ui_matrix()
        self.ui_sequence()

    def new_game(self):
        print("NEW GAME")
        self.button_list.clear()
        self.counter = 0

        self.previous_line = 0
        self.previous_column = 0
        self.code_matrix = None

        self.generate_game_level()
        self.draw_game_level()

    def ui_score(self):
        font_size = self.ds.score_font_size
        font = pygame.font.SysFont('calibri', font_size, True, False)

        plane = pygame.Rect((0, 0), (self.screen.get_width(), 2*font_size)) # pygame object for storing rectangular coordinates
        pygame.draw.rect(self.screen, self.ds.border_color, plane, 2) # draw a rectangle
        
        score_text = font.render(str(self.score), True, self.ds.score_text_color)
        self.screen.blit(score_text, score_text.get_rect(center = plane.center))

    def ui_matrix(self):
        marge = self.ds.marge
        font_size = self.ds.matrix_font_size
        font = pygame.font.SysFont('calibri', font_size, True, False)
        size = self.ds.matrix_size

        # Plane
        plane = pygame.Rect((0, 2*self.ds.score_font_size), (self.screen.get_width(), self.screen.get_height() - 2*self.ds.sequence_size - 2*self.ds.score_font_size)) # pygame object for storing rectangular coordinates
        pygame.draw.rect(self.screen, self.ds.matrix_plane_color, plane) # draw a rectangle

        # Affiche la partie : Code matrice
        matrix_len = self.code_matrix.get_matrix_len()
        offsetL = (plane.height - matrix_len*size)//2 + 2*self.ds.score_font_size
        offsetC = (self.screen.get_width() - matrix_len*size)//2

        ui_text = font.render("CODE MATRIX", True, self.ds.matrix_text_color)
        self.screen.blit(ui_text, (plane.centerx - ui_text.get_width()//2, plane.top + marge))

        for l in range(matrix_len):
            for c in range(matrix_len):
                self.button_list.append(Button(str(self.code_matrix.get_code(l, c)), size, size, (size*c + offsetC, size*l + offsetL), l, c))
                self.button_list[len(self.button_list)-1].draw(self.screen)

    def ui_sequence(self):
        marge = self.ds.marge
        font_size = self.ds.sequence_font_size
        font = pygame.font.SysFont('calibri', font_size, True, False)
        size = self.ds.sequence_size 

        # Plane
        plane = pygame.Rect((0, self.screen.get_height()-2*size), (self.screen.get_width(), 2*size)) # pygame object for storing rectangular coordinates
        pygame.draw.rect(self.screen, self.ds.sequence_text_color, plane, 2) # draw a rectangle

        # Title
        ui_text = font.render("SEQUENCE REQUIRED TO UPLOAD", True, self.ds.sequence_text_color)
        self.screen.blit(ui_text, (size, plane.top + marge))

        # Sequence
        for i in range(self.code_matrix.get_seq_len()):
            ui_text = font.render(str(self.code_matrix.get_sequence(i)), True, self.ds.sequence_text_color)
            self.screen.blit(ui_text, (size + size*i, plane.bottom - font_size - marge//2))

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

    def loop(self):  # sourcery skip: low-code-quality, remove-redundant-if 
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                for i in range(len(self.button_list)):
                    if event.type == pygame.MOUSEBUTTONDOWN and self.button_list[i].mouse_over_button() and not self.button_list[i].is_already_click():
                        self.button_list[i].put_it_already_click(True)
                        if self.button_list[i].code == self.code_matrix.get_sequence(self.counter) and self.on_same_line_or_column(self.button_list[i]):
                            self.counter += 1
                            self.button_list[i].draw_click(self.screen)
                            print(f"GOOD MOVE : {self.counter}/{self.code_matrix.get_seq_len()}")
                        else:
                            self.score -= 1
                            self.ui_score()
                            print("GAME OVER")
                            self.new_game()
                            break

            if self.score <= 10:
                self.matrix_len_bounds = [4, 5]
                self.sequence_len_bounds = [4, 4]
            elif self.score > 10 and self.score <= 20:
                self.matrix_len_bounds = [6, 8]
                self.sequence_len_bounds = [6, 7]
            else:
                self.matrix_len_bounds = [8, 10]
                self.sequence_len_bounds = [8, 9]

            if self.counter == self.code_matrix.get_seq_len():
                self.score += 1
                print(f"SCORE : {self.score}")
                self.new_game()

            pygame.display.update()

        pygame.quit()

main = Main()