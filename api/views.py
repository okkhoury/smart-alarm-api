# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import io
import os

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/owenkhoury/Desktop/SmartAlarm-ca9757e1814f.json"

@csrf_exempt
def getResponse(request):
    # if post request came
    if request.method == 'POST':
        filename = request.POST.get('filename')
        response = {}

        response['textFromFile'] = convertAudioFileToText("test.flac");

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























































