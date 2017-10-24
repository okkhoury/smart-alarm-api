 # -*- coding: utf-8 -*-
from __future__ import unicode_literals

import io
import os

# from google.cloud import speech
# from google.cloud.speech import enums
# from google.cloud.speech import types

# from googleapiclient.discovery import build
# from oauth2client.client import GoogleCredentials

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage

from .forms import DocumentForm

import json
from watson_developer_cloud import SpeechToTextV1

import re

myUsername = '6d1d6655-b091-4232-bb3c-72f35b924f63'
myPassword = 'PiNCxqb5uTbe'

speech_to_text = SpeechToTextV1(username=myUsername, password = myPassword, x_watson_learning_opt_out=False)

# Create your views here.
def index(request):
	return render_to_response('googlef0490e45c8742bb2.html')


def handle_uploaded_file(f):
    with open('saved.flac', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

@csrf_exempt
def getResponse(request):
    # if post request came
	
	# credentials = GoogleCredentials.get_application_default()
	# service = build('compute', 'v1', credentials=credentials)

	# PROJECT = 'ardent-pact-149801'
	# ZONE = 'us-east1-a'
	# request = service.instances().list(project=PROJECT, zone=ZONE)
	# response = request.execute()
		
	if request.method == 'POST':

		form = DocumentForm(request.POST, request.FILES)

		response = {}

		if form.is_valid():

			file = request.FILES['file']

			handle_uploaded_file(file)

			#response['textFromFile'] = convertAudioFileToText("saved.flac");

			with io.open("saved.flac", 'rb') as audio_file:
				fileData = json.dumps(speech_to_text.recognize(audio_file, content_type='audio/flac', timestamps=True, word_confidence=True))

			
			data = re.sub(r'([^\s\w]|_)+', '', fileData.split("transcript")[1].split("timestamps")[0]).strip()

			for word in data.split(" "):
				if word == "Tony":
					response['transcript'] = "tony was here"
					return JsonResponse(response, safe=False)


			response['transcript'] = data
		
			return JsonResponse(response, safe=False)

		else:
			response['textFromFile'] = "failed"
			return JsonResponse(response, safe=False)
			

def convertAudioFileToText(filename):
	# Instantiates a client
	client = speech.SpeechClient();

	# The name of the audio file to transcribe
	file_name = os.path.join(
    os.path.dirname(__file__), filename)

    # Loads the audio into memory
	with io.open(file_name, 'rb') as audio_file:
	    content = audio_file.read()
	    audio = types.RecognitionAudio(content=content)


	config = types.RecognitionConfig(
	    encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
	    sample_rate_hertz=44100,
	    language_code='en-US')


	# Detects speech in the audio file
	response = client.recognize(config, audio)
	alternatives = response.results[0].alternatives

	textFromFile = ""

	for alternative in alternatives:
		textFromFile += 'Transcript: {}'.format(alternative.transcript)
	    #print('Transcript: {}'.format(alternative.transcript))

	return textFromFile;























































