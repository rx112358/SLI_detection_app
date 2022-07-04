from flask import Flask
from flask import request
from flask import render_template
from flask import url_for
from flask import jsonify

import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

import sklearn
import tensorflow as tf
import keras
import numpy as np
import sys
import math
import librosa
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

from keras.models import load_model

TARGET_SR = 8000
AUDIO_LENGTH = 3000

app = Flask(__name__)

UPLOAD_FOLDER = '/home/vivo/Desktop/clg_prj/SLI_detection_app/audio/upload/' 
ALLOWED_EXTENSIONS = {'wav'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template('index.ejs')

def read_audio_from_filename(filename, target_sr):
    audio, _ = librosa.load(filename, sr=target_sr, mono=True)
    audio = audio.reshape(-1, 1)
    return audio

def transform_audio(wav_filename):

    #print(wav_filename)

    audio_buf = read_audio_from_filename(wav_filename, target_sr=TARGET_SR)
    # normalize mean 0, variance 1
    audio_buf = (audio_buf - np.mean(audio_buf)) / np.std(audio_buf)
    original_length = len(audio_buf)
    print(wav_filename, original_length, np.round(np.mean(audio_buf), 4), np.std(audio_buf))
    if original_length < AUDIO_LENGTH:
        audio_buf = np.concatenate((audio_buf, np.zeros(shape=(AUDIO_LENGTH - original_length, 1))))
        print('PAD New length =', len(audio_buf))
    elif original_length > AUDIO_LENGTH:
        audio_buf = audio_buf[0:AUDIO_LENGTH]
        print('CUT New length =', len(audio_buf))

    output_folder ='/home/vivo/Desktop/clg_prj/SLI_detection_app/audio/output/'
    x = str(str(wav_filename.split('/')[-1]).split('.')[0])+'.pkl'
    p = str(output_folder+'/'+x)
    output_filename = p
    #print(p)

    out = { 'audio': audio_buf,
            'sr': TARGET_SR}
    
    
    with open(output_filename, 'wb') as w:
        pickle.dump(out, w)

def load_into(_filename, _x):
    with open(_filename, 'rb') as f:
        print(_filename)
        audio_element = pickle.load(f)
        _x.append(audio_element['audio'])
        return np.array(_x)


@app.route("/model/prediction", methods=['POST'])
def get_prediction():
    if request.method == 'POST':

        if 'file' not in request.files:
            app.logger.debug('No file part')
            #return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            app.logger.debug('No selected file')
            #return redirect(request.url)
        if file :
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            try:
                wav_filename = filename
                upload_folder ='/home/vivo/Desktop/clg_prj/SLI_detection_app/audio/upload/' 
                try:
                    model=load_model('soundnet_lstm.h5')
                    output_folder ='/home/vivo/Desktop/clg_prj/SLI_detection_app/audio/output/'
                    transform_audio(upload_folder+wav_filename)
                    x=[]
                    pickle_file_name = str(str(wav_filename.split('/')[-1]).split('.')[0])+'.pkl'
                    X=load_into(output_folder+pickle_file_name , x)
                    print(X.shape)
                    model=load_model('soundnet_lstm.h5')
                    y_pred=1 if (model.predict(X)>=0.5).astype(int) else 0
                    print(y_pred,filename)
                    #return "success"
                    return jsonify({"file_name":filename, "model_prediction":y_pred})
                except:
                    app.logger.error('Model not found')
                finally:
                    app.logger.debug('Model has succesfully run')

            except FileNotFound:
                app.logger.error('Audio file not found')
        