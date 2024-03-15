import pygame


def display_start_screen(screen, font, width, height):
    screen.fill((43, 45, 48))  # Fill the screen with a dark color

    title_font = pygame.font.Font(None, 72)

    # Title text
    title_text = title_font.render("Bass Learning Tool", True, (230, 230, 230))
    title_rect = title_text.get_rect(center=(width // 2, height // 5))
    screen.blit(title_text, title_rect)

    # Button styling
    button_color = (53, 116, 240)  # Light blue color for buttons
    button_width = 300
    button_height = 60
    button_margin = 20

    # Tab button
    tab_button_rect = pygame.Rect((width - button_width) // 2, height // 2.5, button_width, button_height)
    tab_button_text = font.render("Selecionar tablatura", True, (255, 255, 255))
    draw_button(screen, tab_button_rect, button_color, tab_button_text)

    # Music button
    music_button_rect = pygame.Rect((width - button_width) // 2, height // 2.5 + button_height + button_margin,
                                    button_width, button_height)
    music_button_text = font.render("Selecionar áudio", True, (255, 255, 255))
    draw_button(screen, music_button_rect, button_color, music_button_text)

    # Start button
    start_button_rect = pygame.Rect((width - button_width) // 2, height // 2.5 + 2 * (button_height + button_margin),
                                    button_width, button_height)
    start_button_text = font.render("Iniciar", True, (255, 255, 255))
    draw_button(screen, start_button_rect, button_color, start_button_text)

    return tab_button_rect, music_button_rect, start_button_rect


def draw_button(screen, rect, color, text):
    pygame.draw.rect(screen, color, rect)
    screen.blit(text, text.get_rect(center=rect.center))
