from flask import Flask, render_template, request, redirect
import os
from werkzeug.utils import secure_filename
import yt_dlp
from SVMFinal import extract_feature
import time
import ssl
import urllib.request
import tempfile
import io
import pickle
import json


with open('mlp_model.pkl', 'rb') as file:
    model = pickle.load(file)
        
with open('SVM-scaler', 'rb') as file:
    scaler = pickle.load(file)
    
with open('SVM-key', 'r') as file:
    SVM_key = json.load(file)


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
            
            file.save(filename)
                
            extension = os.path.splitext(filename)[1].lower()
            if extension not in app.config['ALLOWED_EXTENSIONS']:
                message = 'Error: This is not an mp3, wav, or aif...'
                response = ''
            else:
                response = extract_feature(filename, model=model, scaler=scaler, SVM_key=SVM_key)

                message = ''
                
            os.remove(filename)
        else:
            message = 'Error: There was no file submitted...'
            response = ''

        return render_template('main.html', message=message, response=response)
    else:
        pass
    
    
@app.route('/youtube_upload', methods=['POST'])
def youtube_upload():   
    if request.method == 'POST':
        # try:
        youtube_link = request.form.get('youtube-link')  # Access the value of the 'youtube-link' input field
        if youtube_link:
        
            # yt = pytube.YouTube(youtube_link)
            # stream = yt.streams.filter(only_audio=True).first()
            # filename = secure_filename(''.join(list(stream.default_filename)[0:-4]) + '.wav')
           
            # stream.download(filename=filename)
            


            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(youtube_link, download=True)
                filename = ydl.prepare_filename(info_dict) 
                filename = filename[0:-4] + 'mp3'
                
                                        
                                        
            response = extract_feature(filename, model=model, scaler=scaler, SVM_key=SVM_key)
            
            try:
                os.remove(filename)  
            except:
                pass

        else:
            return render_template('main.html')

        return render_template('main.html', response=response)

if __name__ == '__main__':
    app.run(port=8083, debug=True)

