import threading

import pygame

from collect_gp_file_data import collect_tab_data
from compare_arrays import compare_data
from interface.run_interface import run_interface
import shared_variables


def main():
    pygame.init()
    pygame.mixer.init()

    interface_thread = threading.Thread(target=run_interface)
    interface_thread.start()

    note_index = 0
    is_check_time = False
    tolerance_ms = 350

    tab_data = []
    tab_data_collected = False

    while pygame.mixer.music.get_busy():
        if not tab_data_collected:
            tab_data = collect_tab_data(shared_variables.tab_file)
            tab_data_collected = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()  # Stop the music if the window is closed
                interface_thread.join()  # Wait for the interface thread to finish
                pygame.quit()  # Quit Pygame
                return

        if is_check_time and len(shared_variables.played_data) > 0:
            compare_result = compare_data(tab_data=tab_data[note_index], played_data=shared_variables.played_data,
                                          tolerance_ms=tolerance_ms)
            if compare_result == 1:
                shared_variables.hits += 1
                tab_data[note_index]['color'] = (0, 255, 0)
            else:
                shared_variables.misses += 1
                tab_data[note_index]['color'] = (255, 0, 0)

            is_check_time = False
            note_index += 1

        if note_index < len(tab_data):
            check_note = tab_data[note_index]

            if pygame.mixer.music.get_pos() - check_note['time'] >= tolerance_ms:
                is_check_time = True


if __name__ == "__main__":
    main()
