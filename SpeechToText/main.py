import os
from flask import Flask, request, redirect, url_for, flash,jsonify
from semantic_analysis import getCommand
from werkzeug.utils import secure_filename
import speech_recognition as sr
import sys
sys.path.insert(1, './Services')
from Services.GoodreadsService import GoodreadsService
from flask_cors import CORS
import base64
import wavio
import soundfile as sf 
from pydub import AudioSegment
import subprocess

goodReadService = GoodreadsService()
app = Flask(__name__)
CORS(app)

@app.route('/sendFile', methods=['POST'])
def sendFile():
	f = request.files['file'].read()
	with open('file.mp3', 'wb') as f_vid:
 		f_vid.write(f)

	subprocess.run(["ffmpeg.exe", "-i", "file.mp3", "file.wav", "-y"])

	file_audio = sr.WavFile('file.wav')

	r = sr.Recognizer()
	with file_audio as source:
		audio_text = r.record(source)

	text = r.recognize_google(audio_text)
	command = getCommand(text)

	if (command == "AddComment"):
    		return {
				'text': text,
				'command': command,
			};

	return goodReadService.postToTransformService(command, text)

@app.route('/sendReview', methods=['POST'])
def getText():
	json = request.get_json();
	return goodReadService.addReview(json["review"], json["saidText"])

if __name__ == '__main__':
    app.run(host = 'localhost')
