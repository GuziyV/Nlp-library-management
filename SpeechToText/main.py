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

goodReadService = GoodreadsService()
app = Flask(__name__)
CORS(app)

@app.route('/sendFile', methods=['POST'])
def sendFile():
	f = request.files['file'].read()
	#with open('file.wav', 'wb') as f_vid:
 	#	f_vid.write(f)

	file_audio = sr.AudioFile('file.wav')

	r = sr.Recognizer()
	with file_audio as source:
		audio_text = r.record(source)

	text = "comment Alice in wonderland"#r.recognize_google(audio_text)
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
