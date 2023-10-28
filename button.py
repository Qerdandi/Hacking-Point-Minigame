import pygame
from pygame.locals import *
from design import *

class Button:
    def __init__(self, text, plane_size, matrix_len, l, c):
        self.l = l
        self.c = c
        self.code = text
        self.pressed = False
        self.already_click = False
        
        self.ds = Design()
        
        size = self.ds.matrix_size
        pos_x = size*self.c + (plane_size[0] - matrix_len*size)//2
        pos_y = size*self.l + (plane_size[1] - matrix_len*size)//2 + 2*self.ds.score_font_size + self.ds.matrix_size//2
        self.hitbox = pygame.Rect((pos_x, pos_y), (size, size))

        self.font = pygame.font.SysFont('calibri', self.ds.matrix_font_size, True, False) # configure the font of the text
        self.text = self.font.render(text, True, self.ds.button_text_color) # create a text with font properties and string text
     
    def draw(self, screen):
        pygame.draw.rect(screen, self.ds.button_hitbox_color, self.hitbox) # draw a rectangle (button background) on the screen 
        screen.blit(self.text, self.text.get_rect(center = self.hitbox.center)) # add the text button on the screen positioning at the center of the button

    def draw_click(self, screen):
        pygame.draw.rect(screen, self.ds.button_over_color, self.hitbox, 2) # the 2 allows to put the color an a 2 size board instead of the background
        screen.blit(self.text, self.text.get_rect(center = self.hitbox.center))

    def get_pos(self): return [self.l, self.c]
        
    def check_click(self):
        mouse_pos = pygame.mouse.get_pos() # get mouse coordinates
        if self.hitbox.collidepoint(mouse_pos): # look if the mouse is in contact with button hitbox (the rectangle)
            if pygame.mouse.get_pressed()[0]: # look if the left [0] mouse button is pressed
                self.pressed = True
            elif self.pressed == True:
                print("CLICK !!!")
                self.pressed = False

        return self.pressed

    def mouse_over_button(self):
        mouse_pos = pygame.mouse.get_pos() # get mouse coordinates
        if self.hitbox.collidepoint(mouse_pos): # look if the mouse is in contact with button hitbox (the rectangle)
            return True
        return False

    def is_already_click(self): return self.already_click

    def put_it_already_click(self, true_or_false):
        self.already_click = true_or_false
