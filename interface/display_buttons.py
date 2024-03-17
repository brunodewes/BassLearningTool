import os

import pygame

import shared_variables
from database.database_crud import get_precision_from_tab_id, get_id_list, get_tab_name_from_id


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
    draw_button(screen, tab_button_rect, button_color, tab_button_text, shared_variables.tab_file)

    # Music button
    music_button_rect = pygame.Rect((width - button_width) // 2, height // 2.5 + button_height + button_margin,
                                    button_width, button_height)
    music_button_text = font.render("Selecionar áudio", True, (255, 255, 255))
    draw_button(screen, music_button_rect, button_color, music_button_text, shared_variables.music_file)

    # Start button
    start_button_rect = pygame.Rect((width - button_width) // 2, height // 2.5 + 2 * (button_height + button_margin),
                                    button_width, button_height)
    start_button_text = font.render("Iniciar", True, (255, 255, 255))
    draw_button(screen, start_button_rect, button_color, start_button_text)

    return tab_button_rect, music_button_rect, start_button_rect


def display_record_history_button(screen, font, width):
    button_color = (95, 171, 100)
    button_width = 250
    button_height = 60
    button_margin = 20

    # Record history button
    history_button_rect = pygame.Rect(width - button_width - button_margin, button_margin, button_width, button_height)
    record_button_text = font.render("Recordes Pessoais", True, (255, 255, 255))
    draw_button(screen, history_button_rect, button_color, record_button_text)

    return history_button_rect


def display_record_history(screen, font, selected_tab_id, dropdown_visible, width, height):
    white = (230, 230, 230)

    # Get a list of all tab IDs
    tab_ids = get_id_list()

    # Get name from tab_id
    tab_name = get_tab_name_from_id(selected_tab_id)

    personal_record_text_font = pygame.font.Font(None, 54)

    # Dropdown button styling
    dropdown_button_rect = pygame.Rect(50, 50, 200, 30)
    dropdown_button_color = white
    pygame.draw.rect(screen, dropdown_button_color, dropdown_button_rect, 2)
    dropdown_button_text = font.render("Selecionar faixa", True, white)
    dropdown_button_text_rect = dropdown_button_text.get_rect(center=dropdown_button_rect.center)
    screen.blit(dropdown_button_text, dropdown_button_text_rect)

    # Dropdown list styling
    dropdown_list_rect = pygame.Rect(50, 80, 200, len(tab_ids) * 30)
    black = (43, 45, 48)
    if dropdown_visible:
        pygame.draw.rect(screen, black, dropdown_list_rect)
        for i, tab_id in enumerate(tab_ids):
            tab_id = tab_id[0]
            text_surface = font.render(get_tab_name_from_id(tab_id), True, white)
            text_rect = text_surface.get_rect(x=dropdown_list_rect.x + 5, y=dropdown_list_rect.y + i * 30 + 5)
            screen.blit(text_surface, text_rect)

    # Display selected tab
    selected_tab_text = f"{tab_name}" if tab_name and not dropdown_visible else ""
    selected_tab_surface = personal_record_text_font.render(selected_tab_text, True, white)
    selected_tab_rect = selected_tab_surface.get_rect(centerx=width // 2, y=height/4)
    screen.blit(selected_tab_surface, selected_tab_rect)

    # Display precision record for the selected tab
    precision = get_precision_from_tab_id(selected_tab_id)
    precision_text = f"Recorde Pessoal: {precision}%" if precision and not dropdown_visible else ""
    precision_surface = personal_record_text_font.render(precision_text, True, white)
    precision_rect = precision_surface.get_rect(centerx=width // 2, y=height/4 + 100)
    screen.blit(precision_surface, precision_rect)

    return dropdown_button_rect, dropdown_list_rect


def display_end_screen_buttons(screen, font, width, height):
    # Button styling
    button_color = (53, 116, 240)  # Light blue color for buttons
    button_width = 300
    button_height = 60
    button_margin = 20

    # Back to start screen button
    back_button_rect = pygame.Rect((width - button_width) // 2, height // 2.5 + 3 * (button_height + button_margin),
                                   button_width, button_height)
    back_button_text = font.render("Voltar para o início", True, (255, 255, 255))
    draw_button(screen, back_button_rect, button_color, back_button_text)

    return back_button_rect


def draw_button(screen, rect, color, text, right_text=None):
    pygame.draw.rect(screen, color, rect)
    screen.blit(text, text.get_rect(center=rect.center))

    selected_file_font = pygame.font.Font(None, 18)

    if right_text is not None:
        file_name = os.path.basename(right_text)
        right_text_surf = selected_file_font.render(file_name, True, (230, 230, 230))
        right_text_rect = right_text_surf.get_rect(midleft=(rect.right + 10, rect.centery))
        screen.blit(right_text_surf, right_text_rect)
