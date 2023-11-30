import pygame
import sys
import math
import random

pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

sounds = {'1' : pygame.mixer.Sound(r'sounds/water_drop1.mp3'),
          '2' : pygame.mixer.Sound(r'sounds/water_drop2.mp3')
         }


WIDTH, HEIGHT = 1080//2, 1920//2

ball_rate = 10/9
VELOCITY = 15
class FallingSplittingBall(pygame.sprite.Sprite):
    def __init__(self, center, radius,
                 color = (random.randint(1,255), random.randint(1,255), random.randint(1,255)),
                 speed = [0,-15]):
        super().__init__()
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (random.randint(0,255), random.randint(1,50), random.randint(1,50)), (radius, radius), radius)
        self.rect = self.image.get_rect(center=center)
        self.radius = radius
        self.center = list(center)
        self.speed = speed  
        self.flag = False 

    def update(self):
        global all_sprites
        self.center[0] += self.speed[0]
        self.center[1] += self.speed[1]
        self.speed[1] += 0.1  # Gravity effect
        if self.center[1] + self.radius >= HEIGHT and self.radius >=3:
            x_speed = random.uniform(0,VELOCITY)
            y_speed = math.sqrt(VELOCITY**2 - x_speed**2)
            ball1 = FallingSplittingBall((self.center[0] - self.radius//4*3, self.center[1]),
                                         self.radius//ball_rate, speed = [-1 * x_speed, -1 * y_speed])
            
            x_speed2 = random.uniform(0,VELOCITY)
            y_speed2 = math.sqrt(VELOCITY**2 - x_speed**2)
            ball2 = FallingSplittingBall((self.center[0] + self.radius//4*3, self.center[1]),
                                         self.radius//ball_rate, speed = [x_speed2, -1 * y_speed2])
            ball3 = FallingSplittingBall((self.center[0] + self.radius//4*3, self.center[1]),
                                         self.radius//ball_rate, speed = [x_speed2//2, -1 * y_speed2])
            all_sprites.add(ball1, ball2, ball3)
            self.kill()
            sounds[str(random.randint(1,2))].play()
        
        elif self.center[1] + self.radius >= HEIGHT and self.radius < 3:
            x_speed = random.uniform(0,VELOCITY)
            y_speed = math.sqrt(VELOCITY**2 - x_speed**2)
            ball1 = FallingSplittingBall((self.center[0] - self.radius//2, self.center[1]),
                                         self.radius, speed = [-1 * x_speed, -1 * y_speed])
            
            x_speed2 = random.uniform(0,VELOCITY)
            y_speed2 = math.sqrt(VELOCITY**2 - x_speed**2)
            ball2 = FallingSplittingBall((self.center[0] + self.radius//2, self.center[1]),
                                         self.radius, speed = [x_speed2, -1 * y_speed2])
            all_sprites.add(ball1, ball2)
            self.kill()
            sounds[str(random.randint(1,2))].play()
        
        if self.center[0] + self.radius >= WIDTH or self.center[0] - self.radius <= 0:
            self.speed[0] *= -1
            
        
        if self.center[1] - self.radius <= 0:
            self.speed[1] *= -1
        self.rect.center = tuple(map(round, self.center))
            

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Falling and Splitting Balls")

all_sprites = pygame.sprite.Group()

initial_ball = FallingSplittingBall((WIDTH // 2, HEIGHT//4*3), color = (255, 0, 0), radius = 50)
all_sprites.add(initial_ball)

clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    all_sprites.update()
    

    screen.fill(BLACK)
    all_sprites.draw(screen)

    pygame.display.flip()

    clock.tick(60)