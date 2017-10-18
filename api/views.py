# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import io
import os

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

from googleapiclient.discovery import build
from oauth2client.client import GoogleCredentials


from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
	return render_to_response('googlef0490e45c8742bb2.html')

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
		filename = request.POST.get('filename')
		response = {}
		response['textFromFile'] = "test hello" # convertAudioFileToText("test.flac");
		
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























































