import os
import librosa
import numpy as np
import pandas as pd
import warnings
import openai

from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle 
import json
from Shazam import ShazamSong
from API_Keys import openai_key
from io import BytesIO


openai.api_key = openai_key
warnings.filterwarnings('ignore')


def extract_feature(file_path):

    final_json = {
                'MFCCs': [],
                'Spec_Con': [] }

    n_mfcc = 40

    y, sr = librosa.load(file_path, sr=None)

    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)

    sc = librosa.feature.spectral_contrast(y=y, sr=sr)  

    final_json['MFCCs'].append(mfccs)
    final_json['Spec_Con'].append(sc)
      

    mfcc_df_mean = pd.DataFrame(np.mean(final_json['MFCCs'][0], axis=1)).transpose()
    mfcc_df_var = pd.DataFrame(np.var(final_json['MFCCs'][0], axis=1)).transpose()

    sc_df = pd.DataFrame([np.mean(inner_array, axis=1) for inner_array in final_json['Spec_Con']])
    mfcc_df = mfcc_df_mean.merge(mfcc_df_var, how='left', left_index=True, right_index=True)
    mfcc_df = mfcc_df.merge(sc_df, how='left', left_index=True, right_index=True)
    new_column_names = ['Column' + str(i+1) for i in range(len(mfcc_df.columns))]
    mfcc_df.columns = new_column_names

    
    with open('SVM-model', 'rb') as file:
        model = pickle.load(file)
        
    with open('SVM-scaler', 'rb') as file:
        scaler = pickle.load(file)

    mfcc_df_scaled = scaler.transform(mfcc_df)

    y_pred = model.predict(mfcc_df_scaled)
    y_proba = model.predict_proba(mfcc_df_scaled)
    
    max_proba = round(y_proba.max() * 100, 2)

    with open('SVM-key', 'r') as file:
        SVM_key = json.load(file)
        
    keys = [key for key, value in SVM_key.items() if value == y_pred[0]]
    
    if keys is None:
        keys = ''

    else:
        pass    
   
    Shazam_Artist = ShazamSong(file_path)
    
    if Shazam_Artist is None:
        Shazam_Artist = 'None'
    else:
        pass
    
    
    if max_proba >= 50 and (Shazam_Artist != 'None' and ''.join(keys) in Shazam_Artist):
        response = openai.Completion.create(
        engine='text-davinci-003',  # Use the ADA model
        prompt='A user just uploaded an audio file to my web app. Tell them the song is by {} and it is not fake and not artificially generated. Make it casual and brief.'.format(Shazam_Artist, Shazam_Artist),  # Specify your prompt or instructions
        max_tokens=50  # Set the desired length of the generated paragraph
    )
        paragraph = response.choices[0].text.strip()  # Get the generated paragraph
        return paragraph
    
    if max_proba >= 50 and (''.join(keys) not in Shazam_Artist or Shazam_Artist == 'None'):
        response = openai.Completion.create(
            engine='text-davinci-003',  # Use the ADA model
            prompt='A user just uploaded an audio file to my web app. Tell them the song is by {} and that it is fake, and artificially generated. Make it casual and brief.'.format(keys[0], keys[0]),  # Specify your prompt or instructions
            max_tokens=50  # Set the desired length of the generated paragraph
        )
        paragraph = response.choices[0].text.strip()  # Get the generated paragraph
        return paragraph
 
    if max_proba < 50 and Shazam_Artist != 'None':
        return "Hmm... It sounds like a {} song, but we're not sure. It's possible it has a featured artist in it...".format(Shazam_Artist)
    else:
        return "Hmm... We're not sure we can identify that song. It's possible it has a featured artist in it..."

