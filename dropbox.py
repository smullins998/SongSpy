import dropbox
from werkzeug.utils import secure_filename
import pytube
from pydub import AudioSegment
import io
import numpy as np

access_token = 'sl.BfZyFuFwWbQLig6JXIkC3_LNM4A9RW8UIKnO1Y4Ri4n7kgth_I8M4voAoZ5CZFI3YSLHqy1E7MepWwVjhPIHMjabcrLyYXvW-bTKvJXGenXg-CRNQWkapcoc7HEffcnbqj04-aE'


def Dropbox(youtube_link):
    yt = pytube.YouTube(youtube_link)
    stream = yt.streams.filter(only_audio=True).first()
    filename = secure_filename(''.join(list(stream.default_filename)[0:-4]) + '.wav')
    buff = io.BytesIO()

    stream.stream_to_buffer(buff)

    dbx.files_upload(buff.getvalue(), filename)

    dbx = dropbox.Dropbox(access_token)
    _, response = dbx.files_download('/' + filename)
    audio_data = response.content

    audio_io = io.BytesIO(audio_data)

    audio = AudioSegment.from_file(io.BytesIO(audio_data), format="mp4")
    samples = np.array(audio.get_array_of_samples())
    y = samples.astype(float)

    return y