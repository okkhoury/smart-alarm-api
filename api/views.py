# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#import speech_recognition as sr
import io
import os
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

# Create your views here.

@csrf_exempt
def getResponse(request):
    # if post request came
    if request.method == 'POST':
        username = request.POST.get('username')
        response = {}

        response['value'] = convertAudioFileToText("test.FLAC")

        return JsonResponse(response, safe=False)


def convertAudioFileToText(filename):
	# Instantiates a client
	client = speech.speechClient();

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























































