from ShazamAPI import Shazam
from pydub import AudioSegment
import time


def ShazamSong(file_path):
    audio = AudioSegment.from_file(file_path)
    start_time = 30000  
    end_time = len(audio)
    trimmed_audio = audio[start_time:end_time]

    mp3_file_content_to_recognize = trimmed_audio.export(format='mp3').read()
    shazam = Shazam(mp3_file_content_to_recognize)
    recognize_generator = shazam.recognizeSong()

    try:
        result = next(recognize_generator)
        artist = result[1]['track']['subtitle']
        return artist
    except (StopIteration, KeyError):
        return None