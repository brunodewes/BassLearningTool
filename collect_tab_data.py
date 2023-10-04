import guitarpro

from map_tab_to_note import map_tab_to_note


def collect_tab_data(tab_file, bpm):
    song = guitarpro.parse(tab_file)
    tab_data = []

    for track in song.tracks:
        if len(track.strings) == 4:
            print(f"Track: {track.name}")
            for measure in track.measures:
                for voice in measure.voices:
                    for beat in voice.beats:
                        for note in beat.notes:
                            note_name = map_tab_to_note(note.string, note.value)
                            tab_data.append({
                                'time': int(beat.start*60/bpm),
                                # "duration": note.beat.duration,
                                # "string": note.string,
                                # "fret": note.value,
                                'note_name': note_name
                            })

    return tab_data
