import guitarpro

import shared_variables
from map_tab_to_note import map_tab_to_note


def collect_song_info(tab_file):
    song = guitarpro.parse(tab_file)
    song_info = {
        'title': song.title,
        'artist': song.artist
    }

    return song_info


def collect_tab_data(tab_file):
    song = guitarpro.parse(tab_file)

    for track in song.tracks:
        if not track.isPercussionTrack:
            if len(track.strings) == 4:
                for measure in track.measures:
                    for voice in measure.voices:
                        for beat in voice.beats:
                            for note in beat.notes:
                                if note.type not in (guitarpro.NoteType.dead, guitarpro.NoteType.tie):
                                    note_name = map_tab_to_note(note.string, note.value)
                                    shared_variables.tab_data.append({
                                        'time': (((beat.start/960)-1) * (60/song.tempo) * 1000),
                                        'string': note.string,
                                        'fret': note.value,
                                        'note_name': note_name,
                                        'color': (43, 45, 48)
                                    })
    # print(shared_variables.tab_data)
