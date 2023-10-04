import numpy as np
import pyaudio
import wave
import librosa

# Constants for audio recording
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5  # Adjust as needed
OUTPUT_FILENAME = "recorded_audio.wav"


def record_audio():
    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=1024)

    print("Recording...")
    frames = []

    # Start recording
    for _ in range(0, int(RATE / 1024 * RECORD_SECONDS)):
        data = stream.read(1024)
        frames.append(data)

    # Stop recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded audio to a WAV file
    with wave.open(OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print("Recording finished.")


def analyze_recorded_audio():
    # Load the recorded audio
    y, sr = librosa.load(OUTPUT_FILENAME)

    # Extract pitch and note information
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)

    # Determine the number of frames
    num_frames = pitches.shape[1]

    # Initialize a list to store detected notes
    detected_notes = []

    for frame in range(num_frames):
        # Find the most prominent pitch for each frame
        pitch_index = magnitudes[:, frame].argmax()
        frequency = pitches[pitch_index, frame]

        # Check if the frequency is valid (not infinity or too large)
        if not np.isinf(frequency) and frequency < 1e9:
            # Convert frequency to note name (you may need to fine-tune this)
            note_name = librosa.hz_to_note(frequency)

            detected_notes.append({
                'time_seconds': frame * (1024 / RATE),
                'frequency': frequency,
                'note_name': note_name
            })

    return detected_notes


if __name__ == "__main__":
    record_audio()  # Start recording

    # Analyze the recorded audio
    detected_notes = analyze_recorded_audio()

    # Print all detected notes
    for note in detected_notes:
        print(f"Time: {note['time_seconds']:.2f}s, Note: {note['note_name']} (Frequency: {note['frequency']} Hz)")
