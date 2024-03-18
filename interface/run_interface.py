import os
import threading

import pygame

import math

import shared_variables
from collect_gp_file_data import collect_tab_data, collect_song_info
from database.database_crud import get_precision_from_tab_id, update_database, get_id_list
from detect_leading_silence import trim
from feedback import give_feedback
from interface.display_buttons import display_start_screen, display_end_screen_buttons, display_record_history_button, \
    display_record_history
from interface.prompt_file import prompt_file
from interface.start_countdown import start_countdown
from tuner import run_tuner


def run_interface(width=1800, height=900, time_resolution=4, string_spacing=25, padding=30):
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    pygame.mixer.init()

    recording_thread = threading.Thread(target=run_tuner)
    feedback_thread = threading.Thread(target=give_feedback)

    info = pygame.display.Info()
    screen_width, screen_height = info.current_w * 0.95, info.current_h * 0.8
    window_width, window_height = screen_width, screen_height
    width, height = window_width, window_height
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Bass Learning Tool")
    pygame.display.update()

    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 36)
    white = (230, 230, 230)
    black = (43, 45, 48)
    light_blue = (135, 206, 235)

    width_limit = width - padding
    row_height = string_spacing * 5  # Decreased y size
    empty_row_height = string_spacing  # Height of the empty row
    total_row_height = row_height + empty_row_height
    scroll_y = 0

    line_x = padding
    line_y_start = 0
    y_accumulator = 0
    pixels_per_ms = 1 / time_resolution

    waiting = False
    wait_start_time = None
    wait_duration = 1000

    tab_button_rect, music_button_rect, start_button_rect = display_start_screen(screen, font, width, height)
    record_history_button_rect = display_record_history_button(screen, font, width)

    start_button_clicked = False
    running = False
    record_beaten = False

    running_start_screen = True
    running_record_history_screen = False
    while running_start_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if tab_button_rect.collidepoint(mouse_pos):
                    tab_file = prompt_file(button_type='tab')
                    shared_variables.tab_file = tab_file if tab_file != "" else shared_variables.tab_file
                elif music_button_rect.collidepoint(mouse_pos):
                    music_file = prompt_file(button_type='music')
                    shared_variables.music_file = music_file if music_file != "" else shared_variables.music_file
                elif record_history_button_rect.collidepoint(mouse_pos):
                    running_record_history_screen = True
                    running_start_screen = False
                elif start_button_rect.collidepoint(mouse_pos):
                    start_button_clicked = True
                    if shared_variables.tab_file.endswith((".gp3", ".gp4", ".gp5")) and shared_variables.music_file.endswith(("wav", "mp3")):
                        running_start_screen = False

        tab_button_rect, music_button_rect, start_button_rect = display_start_screen(screen, font, width, height)
        record_history_button_rect = display_record_history_button(screen, font, width)

        pygame.display.flip()

    tab_ids = get_id_list()
    selected_tab_id = None
    dropdown_visible = False
    while running_record_history_screen:
        screen.fill(black)

        back_to_start_button_rect = display_end_screen_buttons(screen, font, width, height)
        dropdown_button_rect, dropdown_list_rect = display_record_history(screen, font, selected_tab_id, dropdown_visible, width, height)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if dropdown_button_rect.collidepoint(mouse_pos):
                    dropdown_visible = not dropdown_visible
                elif dropdown_visible and dropdown_list_rect.collidepoint(mouse_pos):
                    selected_tab_id = tab_ids[(mouse_pos[1] - dropdown_list_rect.y) // 30][0]
                    dropdown_visible = False
                elif back_to_start_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    run_interface()

        pygame.display.flip()

    collect_tab_data(shared_variables.tab_file)
    tab_id = shared_variables.tab_data[-1]['time'] - shared_variables.tab_data[0]['time']
    song_info = collect_song_info(shared_variables.tab_file)
    if song_info['artist'] != "" and song_info['title'] != "":
        tab_name = f"{song_info['artist']} - {song_info['title']}"
    else:
        tab_name = os.path.basename(shared_variables.tab_file)

    # Create the rows (length based on the last note's time)
    num_surfaces = math.ceil((shared_variables.tab_data[-1]['time'] / time_resolution) / (width - padding * 2))
    rows = [pygame.Surface((width, total_row_height)) for _ in range(num_surfaces)]
    for row in rows:
        row.fill(white)

    # Trim the silence in the audio start and save it as a temporary WAV file
    trimmed_sound = trim(shared_variables.music_file)
    temp_wav_file = "../temp_audio.wav"
    trimmed_sound.export(temp_wav_file, format='wav')

    pygame.mixer.music.load(temp_wav_file)

    if start_button_clicked:
        start_countdown(screen, duration=3000)

        pygame.display.set_caption(f"{song_info['artist']} - {song_info['title']}")
        pygame.mixer.music.play()
        recording_thread.start()
        feedback_thread.start()

        running = True
        clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if rows:
            rows[0].fill(white)

        current_row = 0

        for note in shared_variables.tab_data:
            time = note['time']
            if time == 0:
                time = 1
            string = note['string']
            fret = note['fret']
            color = note['color']

            std_time = time / time_resolution
            std_time_width = std_time + padding * math.ceil(std_time / (width - padding * 2))

            x_position = std_time_width % width_limit if std_time_width % width_limit != 0 else width_limit

            row_width_limit = width_limit * (current_row + 1)

            if std_time_width > row_width_limit:
                current_row = math.ceil(std_time_width / width_limit) - 1
                rows[current_row].fill(white)

            y_position = (string_spacing * (string - 1)) + 5

            text = font.render(str(fret), True, color)
            rows[current_row].blit(text, (x_position, y_position))

        # Blit each row (and empty row) onto the main screen
        for i, row in enumerate(rows):
            row_y_position = i * total_row_height - scroll_y
            screen.blit(row, (0, row_y_position))

            # Draw a white rectangle to fill the gap between rows
            pygame.draw.rect(screen, white, (0, row_y_position + row_height, width, empty_row_height))

        # Draw lines for each string in all previous rows and the current row
        for row_offset in range(current_row + 1):
            for i in range(1, 5):
                y = i * string_spacing + (current_row - row_offset) * total_row_height
                pygame.draw.line(screen, black, (padding, y), (width - padding, y), 2)

        # Add string labels at the start of each row
        labels = ["G", "D", "A", "E"]
        for i, label in enumerate(labels):
            y = i * string_spacing
            for row_offset in range(current_row + 1):
                row_y_position = row_offset * total_row_height + 5
                screen.blit(font.render(label, True, black), (0, y + row_y_position))

        # Update the x-coordinate of the line based on the speed and time difference
        time_difference = clock.tick(60)
        line_x += pixels_per_ms * time_difference

        # Draw the rounded ends of the vertical line within the width limit
        line_x = min(line_x, width - padding)

        line_y_end = line_y_start + row_height
        line_thickness = 20

        # Draw the central
        pygame.draw.line(screen, light_blue, (line_x, line_y_start), (line_x, line_y_end), line_thickness)

        # Draw rounded ends
        radius = line_thickness / 2
        pygame.draw.circle(screen, light_blue, (line_x + 1, line_y_start), radius)
        pygame.draw.circle(screen, light_blue, (line_x + 1, line_y_end), radius)

        # Move the line to the next row when it reaches the end of the current row
        if line_x >= width - padding and y_accumulator < (len(rows) - 1) * total_row_height:
            line_x = padding
            line_y_start += total_row_height
            y_accumulator += total_row_height
            if line_y_start >= height:
                screen.fill(black)
                scroll_y += line_y_start
                line_y_start = 0

        if y_accumulator == (len(rows) - 1) * total_row_height and line_x >= width - padding:
            # Wait for music to finish
            if pygame.mixer.music.get_busy():
                pass
            else:
                if not waiting:
                    wait_start_time = pygame.time.get_ticks()
                    waiting = True
                else:
                    # Check if the waiting period has elapsed
                    if pygame.time.get_ticks() - wait_start_time >= wait_duration:
                        screen.fill(black)

                        # Create and display the report
                        finish_message = "Música concluída com sucesso!"
                        record_beaten_message = "Você atingiu um novo recorde!"
                        hits = shared_variables.hits
                        misses = shared_variables.misses
                        precision = f"{(hits / len(shared_variables.tab_data) * 100):.2f}"

                        # Update database if record beaten
                        if precision > get_precision_from_tab_id(tab_id):
                            update_database(tab_id, tab_name, precision)
                            record_beaten = True

                        if record_beaten:
                            report_text = (
                                f"{finish_message}\n\n"
                                f"{'=' * 40}\n"
                                f"{song_info['artist']} - {song_info['title']}\n"
                                f"{'=' * 40}\n\n"
                                f"{record_beaten_message}\n\n"
                                f"Acertos: {hits}\n"
                                f"Erros: {misses}\n"
                                f"Precisão: {precision}%"
                            )
                        else:
                            report_text = (
                                f"{finish_message}\n\n"
                                f"{'=' * 40}\n"
                                f"{song_info['artist']} - {song_info['title']}\n"
                                f"{'=' * 40}\n\n"
                                f"Acertos: {hits}\n"
                                f"Erros: {misses}\n"
                                f"Precisão: {precision}%\n"
                                f"Recorde Pessoal: {get_precision_from_tab_id(tab_id)}%"
                            )

                        report_font = pygame.font.Font(None, 48)
                        text_y = height * 0.1  # Initial y position for the text

                        for i, line in enumerate(report_text.split("\n")):
                            text_surface = report_font.render(line, True, white)
                            text_rect = text_surface.get_rect(right=(width - padding - 10),
                                                              centery=text_y + text_surface.get_height() // 2)
                            text_rect.centerx = width // 2  # Center horizontally
                            screen.blit(text_surface, text_rect)
                            text_y += text_surface.get_height() + 10  # Add spacing between lines

                            back_to_start_button_rect = display_end_screen_buttons(screen, font, width, height)

                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    mouse_pos = pygame.mouse.get_pos()
                                    if back_to_start_button_rect.collidepoint(mouse_pos):
                                        shared_variables.reset_globals()
                                        pygame.quit()
                                        run_interface()

        pygame.display.flip()

    pygame.quit()
