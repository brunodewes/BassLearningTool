import pygame
import math


def start_countdown(screen, duration):
    font = pygame.font.Font(None, screen.get_height() // 3)
    countdown_start_time = pygame.time.get_ticks()
    countdown_running = True
    while countdown_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                countdown_running = False

        screen.fill((43, 45, 48))

        countdown_elapsed_time = pygame.time.get_ticks() - countdown_start_time
        countdown_remaining_time = max(duration - countdown_elapsed_time, 0)
        countdown_seconds = math.ceil(countdown_remaining_time / 1000)

        if countdown_seconds == 0:
            countdown_running = False
        else:
            countdown_text = font.render(str(countdown_seconds), True, (230, 230, 230))
            countdown_text_rect = countdown_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(countdown_text, countdown_text_rect)

        pygame.display.flip()
        pygame.time.delay(10)
    return
