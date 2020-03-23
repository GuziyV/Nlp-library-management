import os
from flask import Flask, request, redirect, url_for, flash,jsonify
from semantic_analysis import getCommand
from werkzeug.utils import secure_filename
import speech_recognition as sr
import sys
sys.path.insert(1, './Services')
import GoodreadsService

GoodreadsService = GoodreadsService.GoodreadsService()
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
	resp = dict()
	resp['command'] = command
	resp['text'] = text
	return resp
	GoodreadsService.postToTransformService("AddBook", "add alice in wonderland")

if __name__ == '__main__':
    app.run(host = 'localhost')
