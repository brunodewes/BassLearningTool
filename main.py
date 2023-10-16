import threading
import pygame

from collect_tab_data import collect_tab_data
from compare_arrays import compare_data
from detect_leading_silence import trim
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
    mp3_file = "songs/soul-to-squeeze15sec.mp3"
    tab_file = "tabs/soul_to_squeeze.gp4"
    bpm = 85
    tab_data = collect_tab_data(tab_file, bpm)
    # print(tab_data)

    note_index = 0
    is_check_time = False
    tolerance_ms = 100

    hits = 0
    misses = 0

    recording_thread = threading.Thread(target=record_notes)
    play_music(mp3_file)
    recording_thread.start()

    while pygame.mixer.music.get_busy():
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


if __name__ == "__main__":
    main()
