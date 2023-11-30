import pygame
import sys
import math
import numpy as np

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Define the screen dimensions
WIDTH, HEIGHT = 1080//2, 1920//2

# Create a class for the spinning ball
class SpinningBall(pygame.sprite.Sprite):
    def __init__(self, center, distance, radius, color, linear_speed, sound = pygame.mixer.Sound('sounds/sound3.mp3'), initial_angle=0):
        super().__init__()
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect(center=center)
        self.center = center
        self.radius = radius
        self.angle = initial_angle
        self.linear_speed = linear_speed
        self.distance = distance
        self.sound = sound

    def update(self):
        radian_angle = math.radians(self.angle)
        if self.rect.colliderect(line_rect):
#             self.linear_speed *= -1 
        
            self.sound.play()
        
        self.angle += self.linear_speed
        radian_angle = math.radians(self.angle)
        x = self.center[0] + self.distance * math.cos(radian_angle)
        y = self.center[1] + self.distance * math.sin(radian_angle)
        self.rect.center = (x, y)

def generate_gradient(start_color, end_color, num_steps):
    gradient_colors = [
        tuple(int(start + (end - start) * i / (num_steps - 1)) for start, end in zip(start_color, end_color))
        for i in range(num_steps)
    ]
    return gradient_colors

# Example usage:
start_color = (185, 43, 39)  # #659999
end_color = (21, 101, 192)  # #f4791f



# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("люблю Диану")

# Create a sprite group
all_sprites = pygame.sprite.Group()

center_point = (WIDTH // 2, HEIGHT // 2)


# Create the spinning balls
# ball1 = SpinningBall(center_point,10, 5, RED, 1)
# ball2 = SpinningBall(center_point,20, 5, GREEN, 1)
# ball3 = SpinningBall(center_point,30, 5, BLUE, 1)  # Negative speed for opposite rotation
range_distances = range(50, 260, 20)

num_steps = len(range_distances)

gradient_colors = generate_gradient(start_color, end_color, num_steps)

balls = [SpinningBall(center_point, distance, 7, color, 6.3 - distance/50, sound) for distance, color, sound in zip(range_distances,
                                                                                                                    gradient_colors,
                                                                                                                   [pygame.mixer.Sound(f'sounds/sound{i}.mp3') for i in range(num_steps)]
                                                                                                                   )]
all_sprites.add(balls)

line_rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, 1, HEIGHT // 2)
# Run the game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update the sprites
    all_sprites.update()

    # Draw on the screen
    screen.fill(BLACK)
    all_sprites.draw(screen)
    
    pygame.draw.line(screen, WHITE, center_point, (WIDTH // 2, HEIGHT))
    
    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)
