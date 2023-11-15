import threading
import pygame

from collect_gp_file_data import collect_tab_data, collect_song_info
from compare_arrays import compare_data
from detect_leading_silence import trim
from interface import generate_tab_interface
from tuner import run_tuner
from shared_variables import played_data


def play_music(mp3_file):
    pygame.mixer.init()

    # Trim the audio and save it as a temporary WAV file
    trimmed_sound = trim(mp3_file)
    temp_wav_file = "temp_audio.wav"
    trimmed_sound.export(temp_wav_file, format='wav')

    pygame.mixer.music.load(temp_wav_file)
    pygame.mixer.music.play()


def record_notes():
    run_tuner()


def main():
    mp3_file = "songs/soul-to-squeeze.mp3"
    # mp3_file = "songs/20secondstest.mp3"
    tab_file = "tabs/soul_to_squeeze.gp4"
    tab_data = collect_tab_data(tab_file)
    # tab_data = [{'time': 0, 'string': 1, 'fret': 1, 'note_name': 'A'}, {'time': 7792, 'string': 2, 'fret': 2, 'note_name': 'E'}, {'time': 7962, 'string': 2, 'fret': 3, 'note_name': 'F#'}, {'time': 8131, 'string': 1, 'fret': 4, 'note_name': 'A'}, {'time': 8301, 'string': 2, 'fret': 5, 'note_name': 'F#'}, {'time': 8699, 'string': 1, 'fret': 24, 'note_name': 'A'}, {'time': 8700, 'string': 1, 'fret': 24, 'note_name': 'B'}, {'time': 8849, 'string': 2, 'fret': 14, 'note_name': 'B'}, {'time': 9040, 'string': 1, 'fret': 9, 'note_name': 'B'}]
    # tab_data = [{'time': 6098, 'string': 1, 'fret': 1, 'note_name': 'A'}, {'time': 7792, 'string': 2, 'fret': 2, 'note_name': 'E'}, {'time': 7962, 'string': 2, 'fret': 3, 'note_name': 'F#'}, {'time': 8131, 'string': 1, 'fret': 4, 'note_name': 'A'}, {'time': 8301, 'string': 2, 'fret': 5, 'note_name': 'F#'}, {'time': 8470, 'string': 1, 'fret': 6, 'note_name': 'A'}, {'time': 8640, 'string': 1, 'fret': 7, 'note_name': 'B'}, {'time': 8840, 'string': 2, 'fret': 8, 'note_name': 'B'}]
    song_info = collect_song_info(tab_file)
    # for note in tab_data:
    #     print(note)

    # Create the interface in a separate thread
    interface_thread = threading.Thread(target=generate_tab_interface, args=(tab_data, song_info))
    interface_thread.start()

    note_index = 0
    is_check_time = False
    tolerance_ms = 100

    hits = 0
    misses = 0

    recording_thread = threading.Thread(target=record_notes)
    play_music(mp3_file)
    recording_thread.start()

    while pygame.mixer.music.get_busy():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()  # Stop the music if the window is closed
                interface_thread.join()  # Wait for the interface thread to finish
                pygame.quit()  # Quit Pygame
                return

        if is_check_time and len(played_data) > 0:
            compare_result = compare_data(tab_data=tab_data[note_index], played_data=played_data,
                                          tolerance_ms=tolerance_ms)
            if compare_result == 1:
                hits += 1
            else:
                misses += 1

            print(f"Hits: {hits}, Misses: {misses}")

            is_check_time = False
            note_index += 1

        if note_index < len(tab_data):
            check_note = tab_data[note_index]

            if pygame.mixer.music.get_pos() - check_note['time'] >= tolerance_ms:
                is_check_time = True

    recording_thread.join()  # Wait for the recording thread to finish
    interface_thread.join()  # Wait for the interface thread to finish


if __name__ == "__main__":
    main()
