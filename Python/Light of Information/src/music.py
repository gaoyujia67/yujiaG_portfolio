#pip install librosa

import librosa
import time
from lighting import lighting 
import random

def load_audio(file_path):
    """
    Load the audio file in WAV format.

    Parameters:
        file_path (str): The path to the WAV audio file.

    Returns:
        tuple: A tuple containing the audio waveform and the sampling rate.
               If loading fails, returns (None, None).
    """
    try: 
        audio_file = librosa.load(file_path)
        y, sr = audio_file
        return y, sr
    except Exception as e:
        print(f"Failed to load audio file: {e}")
        return None, None
    

def get_beat_times(y, sr):
    """
    Extract beat times from the audio.

    Parameters:
        y (ndarray): Audio time series.
        sr (int): Sampling rate of y.

    Returns:
        ndarray: Array containing beat timings in seconds.
                If extraction fails, returns None.
    """
    try:
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)
        return beat_times
    except Exception as e:
        print(f"Failed to get beat times: {e}")
        return None


def music_color(beat_times):
    """
    Adjusts lighting patterns based on beat times.

    Parameters:
        beat_times (ndarray): Array containing beat timings in seconds.
    """
    try:
        lit = lighting()
    except ImportError:
        print("Error: Failed to load the lighting class.")
        exit()

    pattern = [100, 100, 100, 100]
    for i in range(0, len(beat_times)-4, 2):
        fade = True if i%4==0 else False
        if fade==True:
            pattern_now=[int(x/1.1**5) for x in pattern]
        lit.general_pattern(pattern_now)
        # time.sleep(beat_times[i+3]-beat_times[i])
        lit.breath(fade, beat_times[i+2]-beat_times[i])
        pattern=[max(min(x+int(random.uniform(-100, 100)),255),0) for x in pattern]

    lit.shut_off()


if __name__ == "__main__":
    lit = lighting()
    file_path = 'sample-file-3.wav'
    y, sr = load_audio(file_path)
    try:
        beat_times = get_beat_times(y, sr)
        music_color(beat_times)
    except KeyboardInterrupt:
        lit.shut_off()