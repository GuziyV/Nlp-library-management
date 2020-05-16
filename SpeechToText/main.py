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

def fileToText(f):
	with open('file.mp3', 'wb') as f_vid:
		f_vid.write(f)

	subprocess.run(["ffmpeg.exe", "-i", "file.mp3", "file.wav", "-y"])

	file_audio = sr.WavFile('file.wav')

	r = sr.Recognizer()
	with file_audio as source:
		audio_text = r.record(source)

	return r.recognize_google(audio_text)

goodReadService = GoodreadsService()
app = Flask(__name__)
CORS(app)

@app.route('/getCommand', methods=['POST'])
def command():
	f = request.files['file'].read()

	text = fileToText(f)
	command = getCommand(text)

	return command

@app.route('/getText', methods=['POST'])
def getText():
	f = request.files['file'].read()

	return fileToText(f)

@app.route('/sendReview', methods=['POST'])
def sendReview():
	json = request.get_json()
	return goodReadService.addReview("Best book in my childhood", "Harry Potter")
	#return goodReadService.addReview(json["review"], json["book"])

@app.route('/addBook', methods=['POST'])
def addBook():
	json = request.get_json()
	return goodReadService.addBook(json["book"])
	#return goodReadService.addBook("Sherlock holmes")

@app.route('/removeBook', methods=['POST'])
def removeBook():
	json = request.get_json()
	return goodReadService.removeBook(json["book"])
	#return goodReadService.removeBook("Sherlock holmes")


if __name__ == '__main__':
    app.run(host = 'localhost')

