import os
from flask import Flask, request, redirect, url_for, flash,jsonify
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

	return r.recognize_google(audio_text)

if __name__ == '__main__':
    app.run(host = '0.0.0.0')