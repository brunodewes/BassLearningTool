import tkinter
import tkinter.filedialog


def prompt_file(button_type):
    """Create a Tk file dialog and cleanup when finished"""
    top = tkinter.Tk()
    top.withdraw()  # hide window
    initial_dir = "tabs" if button_type == 'tab' else "songs"
    if button_type == 'tab':
        filetypes = [("*.gp3;*.gp4;*.gp5", "*.gp3;*.gp4;*.gp5")]
    elif button_type == 'music':
        filetypes = [("*.mp3;*.wav", "*.mp3;*.wav")]
    else:
        filetypes = None
    file_name = tkinter.filedialog.askopenfilename(parent=top, filetypes=filetypes, initialdir=initial_dir)
    top.destroy()
    return file_name
