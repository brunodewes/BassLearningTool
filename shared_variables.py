# played_data = []
played_data = [{'time': 5647, 'note_name': 'A'}, {'time': 7411, 'note_name': 'E'}, {'time': 7588, 'note_name': 'F#'}, {'time': 7765, 'note_name': 'A'}, {'time': 7942, 'note_name': 'F#'}]
tab_data = []

tab_file = ""
music_file = ""

hits = 0
misses = 0


def reset_globals():
    global played_data, tab_data, tab_file, music_file, hits, misses

    played_data = []
    tab_data = []

    tab_file = ""
    music_file = ""

    hits = 0
    misses = 0
