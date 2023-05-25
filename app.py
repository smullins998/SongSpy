from flask import Flask, render_template, request, redirect
import os
from werkzeug.utils import secure_filename
import pytube
from pytube import YouTube
from pytube.exceptions import VideoUnavailable
from SVMFinal import extract_feature
import time
import ssl
import urllib.request
import dropbox
from dropbox.exceptions import AuthError
import tempfile

# Specify the access token for your Dropbox account


app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB
app.config['ALLOWED_EXTENSIONS'] = {'.wav', '.mp3', '.aif'}


ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
ssl._create_default_https_context = ssl._create_unverified_context



@app.route('/')
def main():
    return render_template('main.html')


@app.route('/upload', methods=['POST'])
def upload():
    if request.method =='POST':
        file = request.files['music-file']  # This is the file NAME in the HTML

        if file:
            filename = secure_filename(file.filename)
            extension = os.path.splitext(filename)[1].lower()
            if extension not in app.config['ALLOWED_EXTENSIONS']:
                message = 'Error: This is not an mp3, wav, or aif...'
            else:
                response = extract_feature(os.path.join('uploads', filename))

                message = ''
        else:
            message = 'Error: There was no file submitted...'

        return render_template('main.html', message=message, response=response)
    else:
        pass
    
    
@app.route('/youtube_upload', methods=['POST'])
def youtube_upload():   
    if request.method == 'POST':
        # try:
        youtube_link = request.form.get('youtube-link')  # Access the value of the 'youtube-link' input field
        if youtube_link:
        
            yt = pytube.YouTube(youtube_link)
            stream = yt.streams.filter(only_audio=True).first()
            filename = secure_filename(''.join(list(stream.default_filename)[0:-4]) + '.wav')
    
            # stream.download(filename=filename)

            audio_file = stream.download(filename=filename, output_path=None)
        
            access_token = 'sl.BfHiljRELAoeSBDcZs0p6ihhC7g4vrMj_zLKhM6qHecfay3kCmB4jeIRBff9dgjfIo7w3WjZ0q1jpRNWq9qOucLPZrQw_XE5RlKGpJQH4QvAsaO6wnSLMdjB9-aV6c1vlPGq3ck'
            secret = 'ubao0smd0wg6msn'
            reg_key = 'w4ex9ok8udpepwh'

            dbx = dropbox.Dropbox(access_token, app_key=reg_key, app_secret=secret)


            # Upload the file to Dropbox
            with open(audio_file, 'rb') as f:
                response = dbx.files_upload(f.read(), f'/{filename}')

            time.sleep(1)

            metadata, response = dbx.files_download( '/' + filename)
            data = response.content

            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_file.write(data)


            response = extract_feature(temp_file.name)
            
            dbx.files_delete_v2('/' + filename)
            
            try:
                os.remove(audio_file)  
            except:
                pass
        
           
         



        else:
            return render_template('main.html')

        return render_template('main.html', response=response)
        # except:
        #     response = 'There was an error...'   
        #     return render_template('main.html', response=response)
     
        
    

if __name__ == '__main__':
    app.run(port=8083, debug=True)

