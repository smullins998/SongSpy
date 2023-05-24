from ShazamAPI import Shazam
from pydub import AudioSegment


def ShazamSong(file_path):
    audio_file_path = file_path
    audio = AudioSegment.from_file(audio_file_path)
    start_time = 30000  
    end_time = len(audio)  
    trimmed_audio = audio[start_time:end_time]
    trimmed_audio.export(file_path)
    
    
    audio_file_path = file_path
    mp3_file_content_to_recognize = open(audio_file_path, 'rb').read()
    shazam = Shazam(mp3_file_content_to_recognize)
    recognize_generator = shazam.recognizeSong()

    try:
        result = next(recognize_generator)
        artist = result[1]['track']['subtitle']
        return artist
    except (StopIteration, KeyError):
        return None
    
