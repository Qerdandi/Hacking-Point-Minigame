from pygame.locals import *

# This class allows you to custom font size, margin and color of all the game 
# (except font that can be custom in main.py for each text components)

class Design:
    def __init__(self):
        self.color()

        self.matrix_margin = 20
        self.sequence_margin = 10
        
        self.score_font_size = 72
        self.win_rate_font_size = 36
        self.matrix_font_size = 25
        self.sequence_font_size = 24

        self.matrix_size = self.matrix_font_size + self.matrix_margin
        self.sequence_size = self.sequence_font_size + self.sequence_margin
    
    def color(self):
        self.score_text_color = Color(255, 255, 255)
        self.win_rate_text_color = Color(255, 255, 255)
        self.score_plane_color = Color(35, 30, 40)
        
        self.matrix_text_color = Color(200, 255, 0)
        self.matrix_plane_color = Color(35, 30, 40)

        self.sequence_text_color = Color(200, 255, 0)
        self.sequence_plane_color = Color(35, 30, 40)

        self.border_color = Color(200, 255, 0)

        self.button_text_color = Color(200, 255, 0)
        self.button_hitbox_color = Color(35, 30, 40)
        self.button_over_color = Color(0, 245, 255)