import os
from flask import Flask, request, redirect, url_for, flash,jsonify
from semantic_analysis import getCommand
from werkzeug.utils import secure_filename
import speech_recognition as sr


app = Flask(__name__)


@app.route('/getText', methods=['POST'])
def getText():
	f = request.files['file']
	file_audio = sr.AudioFile(f)

	r = sr.Recognizer()
	with file_audio as source:
		audio_text = r.record(source)

	text = r.recognize_google(audio_text)
	command = getCommand(text);
	return command

if __name__ == '__main__':
    app.run(host = 'localhost')
