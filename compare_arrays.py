def compare_data(tab_data, played_data, tolerance_ms):
    tab_note_time = tab_data['time']
    tab_note_name = tab_data['note_name']

    for played_note in played_data:
        played_note_time = played_note['time']
        played_note_name = played_note['note_name']

        if abs(played_note_time - tab_note_time) <= tolerance_ms and played_note_name == tab_note_name:
            # print(f"tab time: {tab_note_time} | played time: {played_note_time} | tab note: {tab_note_name} | played note: {played_note_name}")
            return 1

    return 0
