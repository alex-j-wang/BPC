import numpy as np
import pygame
import os
import sys

from logic import *

# Initialize Pygame
pygame.init()
tick = 0

# Set up the screen
SCREEN_WIDTH, SCREEN_HEIGHT = CIT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('TPCIT Test')

fade_surface = pygame.Surface(CIT)
fade_surface.fill((0, 0, 0))

def fade_out(fade_surface, duration):
    for alpha in range(0, 256, 32):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(duration // 8)

def fade_in(fade_surface, duration):
    for alpha in range(255, -1, -32):
        fade_surface.set_alpha(alpha)
        draw_board(game)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(duration // 8)

def draw_board(game):
    screen.fill((255, 255, 255))
    for checkpointrect in game.checkpointrects:
        pygame.draw.rect(screen, (0, 255, 0), checkpointrect)
    for coin in game.coins:
        pygame.draw.circle(screen, (255, 215, 0), coin, COINSIZE * game.ratio)
    for enemy in game.enemies:
        pygame.draw.circle(screen, (0, 0, 255), enemy.pos, ENEMYSIZE * game.ratio)
    if game.draw:
        for wallrect in game.wallrects:
            pygame.draw.rect(screen, (0, 0, 0), wallrect)
    pygame.draw.rect(screen, (255, 0, 0), game.player.rect)

def end_game():
    font = pygame.font.Font(None, 36)  # Use default font and size 36
    text = font.render("[Answer]", True, (0, 255, 0))
    text_rect = text.get_rect(center=(CIT[0] // 2, CIT[1] // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(500)

# Set up the game
game = Game()

# Main game loop
running = True
win = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    game.player_tick(keys[pygame.K_DOWN] - keys[pygame.K_UP], keys[pygame.K_RIGHT] - keys[pygame.K_LEFT])

    if all(game.reached) and not game.savedcoins:
        fade_out(fade_surface, 250)
        game.level += 1
        if not os.path.exists(os.path.join(levels_dir, f'L{game.level}.txt')):
            running = False
            win = True
            break
        game.load_level()
        draw_board(game)
        fade_in(fade_surface, 250)

    # Move the enemies
    game.enemy_tick()

    # Remove coins
    game.coin_tick()

    # Draw the board
    draw_board(game)
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(TPS)
    tick += 1

# Clean up
if win:
    end_game()
pygame.quit()
sys.exit()
