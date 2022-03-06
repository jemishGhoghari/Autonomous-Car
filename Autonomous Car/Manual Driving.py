from typing import SupportsIndex
from warnings import catch_warnings
import pygame
from pygame import Surface, font
import pygame.gfxdraw as gfx
import math
import random
# import time
import copy
from utils_dir import blit_rotate_center


pygame.init()

# Screen dimensions
screen_width = 1200 # in pixels 
screen_heigth = 600

# Screen Display
dimension = (screen_width, screen_heigth)
screen = pygame.display.set_mode(dimension)

# Clock Ticker
clock = pygame.time.Clock()

# Framerate
framerate = 60
# Ball size
ball_size = 10
# Load image
carImg = pygame.image.load('..\Autonomous Car\images\car.png')
# Colors
white = pygame.color.Color(255, 255, 255)
green = pygame.color.Color(0, 255, 0)
# Dimensions of the Image
rect_width = 59
rect_height = 128
# Controlling Flow of Programme
playing = True

class DubinCar:
    def __init__(self, rot_valocity, max_vel):
        self.position = [100, 100]
        self.velocity = 0
        self.angle = 0
        self.max_vel = max_vel
        self.rotational_vel = rot_valocity
        self.target = [random.randint(100, screen_width), random.randint(100, screen_heigth)]
        self.acceleration = 0.1

    # Function to find distance to the target from the car
    def distance_to_target(self):
        self.dx = self.target[0] - (self.position[0] + rect_width/2)
        self.dy = self.target[1] - (self.position[1] + rect_height/2)
        res = math.sqrt((self.dx)**2 + (self.dy)**2)
        return res

    # Function to reach at the destination and redefine new target
    def collect_target(self):
        if self.distance_to_target() < ball_size+60:
            self.target = [random.randint(10, screen_width), random.randint(10, screen_heigth)]
        
    def planning(self):
        angles = []
        distances = []

        for i in range(10):
            simulation = copy.deepcopy(self)
            rendom_number = random.uniform(-.5, .5)
            simulation.angle += rendom_number
            simulation.update()
            d = simulation.distance_to_target()
            # print(rendom_number, d)
            distances.append(d)
            angles.append(rendom_number)

        min_distance = 50000
        min_index = -1
        for i, d in enumerate(distances):
            if d < min_distance:    
                min_distance = d
                min_index = i
        best_angle = angles[min_index]
        return best_angle, min_distance
    
    # Function to rotate car at it's center point
    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotational_vel
        elif right:
            self.angle -= self.rotational_vel

    # Function to draw rotated car
    def draw(self, screen):
        blit_rotate_center(screen, carImg, (self.position[0], self.position[1]), self.angle)

    # Function to move car forward from the current position
    def move_forward(self):
        self.velocity = min(self.velocity + self.acceleration, self.max_vel)
        self.move()

    # Function to move car backward from the current position
    def move_backward(self):
        self.velocity = max(self.velocity - self.acceleration, -self.max_vel/2)
        self.move()

    # Function to move car
    def move(self):
        rad_angle = math.radians(self.angle)
        verticle = math.cos(rad_angle) * self.velocity
        horizontal = math.sin(rad_angle) * self.velocity

        self.position[1] -= verticle
        self.position[0] -= horizontal


def draw_car(win, player_car):
    player_car.draw(win)
    pygame.display.update()

car = DubinCar(5, 5)

while playing:
    # listening for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
    
    # get input from keyboard
    keys = pygame.key.get_pressed()

    # Keyboard Key event to move and turn the car
    if keys[pygame.K_RIGHT]:
        car.rotate(right=True)
    if keys[pygame.K_LEFT]:
        car.rotate(left=True)
    if keys[pygame.K_UP]:
        car.move_forward()
    if keys[pygame.K_DOWN]:
        car.move_backward()

    # filling window background color
    screen.fill(white)

    # Draw car
    draw_car(screen, car)

    # Functions to measure distance to target and collect target
    car.distance_to_target()
    car.collect_target()

    # Making a universal boundaries of the window
    if int(car.position[0]) >= screen_width + 50:
        car.position[0] = -50
        car.position[1] = random.randint(0, screen_heigth)
    if int(car.position[0]) < -50:
        car.position[0] = screen_width - 50
        car.position[1] = random.randint(0, screen_heigth)
    if int(car.position[1]) >= screen_heigth + 50:
        car.position[1] = -50
        car.position[0] = random.randint(0, screen_width)
    if int(car.position[1]) < -50:
        car.position[1] = screen_heigth + 50
        car.position[0] = random.randint(0, screen_width)

    # printing target ball on the screen
    gfx.filled_circle(screen, int(car.target[0]), int(car.target[1]), ball_size, green)

    # update display
    pygame.display.update()

    # control looping speed
    clock.tick(framerate)

pygame.quit()


    


    


