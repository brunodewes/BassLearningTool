import pygame

from compare_arrays import compare_data
import shared_variables


def give_feedback():
    note_index = 0
    is_check_time = False
    tolerance_ms = 350

    while pygame.mixer.music.get_busy():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()  # Stop the music if the window is closed
                pygame.quit()  # Quit Pygame
                return

        if is_check_time and len(shared_variables.played_data) > 0:
            compare_result = compare_data(tab_data=shared_variables.tab_data[note_index], played_data=shared_variables.played_data,
                                          tolerance_ms=tolerance_ms)
            if compare_result == 1:
                shared_variables.hits += 1
                shared_variables.tab_data[note_index]['color'] = (0, 255, 0)
            else:
                shared_variables.misses += 1
                shared_variables.tab_data[note_index]['color'] = (255, 0, 0)

            is_check_time = False
            note_index += 1

        if note_index < len(shared_variables.tab_data):
            check_note = shared_variables.tab_data[note_index]

            if pygame.mixer.music.get_pos() - check_note['time'] >= tolerance_ms:
                is_check_time = True
