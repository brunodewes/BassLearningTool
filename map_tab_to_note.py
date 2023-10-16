def map_tab_to_note(string, fret):
    # Define the MIDI note numbers for the open strings of a standard-tuned guitar
    string_midi_notes = [15, 10, 5, 0]  # E1, A1, D2, G2

    # Calculate the MIDI note number for the given string and fret
    note_midi_number = string_midi_notes[string - 1] + fret

    # Convert the MIDI note number to a note name
    note_name = get_note_name_from_midi(note_midi_number)

    return note_name


def get_note_name_from_midi(midi_note_number):
    note_names = ['E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#']
    note_name = note_names[midi_note_number % 12]
    octave = (midi_note_number // 12) + 1  # Add 1 to start from octave 1
    return f"{note_name}"
