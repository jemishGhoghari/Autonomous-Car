import pygame
import math 

def blit_rotate_center(screen, image, top_left, angle):
    # print(top_left)
    # print(top_left[0])
    # new_list = [top_left[0], top_left[1]]
     
    # new_list[0] += 64
    # new_list[1] += 29.5
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
    screen.blit(rotated_image, new_rect.topleft)