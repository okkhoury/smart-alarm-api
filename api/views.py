# Copyright 2017 IBM Watson

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


 # -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import re

from watson_developer_cloud import SpeechToTextV1

from django.shortcuts import render
from django.shortcuts import redirect

from .forms import DocumentForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

### Variables for the alarm visual ####

# Display the time for which an alarm is set.
global AlarmOnOffVisual
AlarmTimeVisual = 0;

# Display if a snooze is currently set.
global SnoozeVisual
SnoozeVisual = "OFF"

# Display whether there is currently an alarm set.
global AlarmOnOffVisual
AlarmOnOffVisual = "NO ALARM SET"

myUsername = '7558b471-8543-4ac4-861f-fee723bc59ba'
myPassword = '1h2YhFU1HpW2'



# Key words that trigger either on, off, or snooze commands.
onWords = ["on", "set", "make", "create"]
offWords = ["off", "stop", "shut"]
snoozeWords = ["snooze"]

# Used to parse the user text and format numbers. Ex thirty five -> 35.
units = [
        "oh", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen", "twenty"
      ]

tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty"]

speech_to_text = SpeechToTextV1(username=myUsername, password = myPassword, x_watson_learning_opt_out=False)

# Write the data recieved from a post request into a local wav file called saved.wav
def handle_uploaded_file(f):
    with open('saved.wav', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

# Handles the logic for determing the function a user is trying to execute.
# Reads in user audio file, converts audio to text, parses text, looks for keywords and
# sends the user's command back to the MyRio in the post request response.
@csrf_exempt
def getResponse(request):
		
	if request.method == 'POST':

		form = DocumentForm(request.POST, request.FILES)

		response = {}

		print("outside")

		if form.is_valid():

			print("here")

			file = request.FILES['file']

			handle_uploaded_file(file)

			with open("saved.wav", 'rb') as audio_file:
				fileData = json.dumps(speech_to_text.recognize(audio_file, content_type='audio/wav', timestamps=True, word_confidence=True))
			
			data = re.sub(r'([^\s\w]|_)+', '', fileData.split("transcript")[1].split("timestamps")[0]).strip().lower()

			for word in data.split(" "):

				if word in onWords:
					response['command'] = "on"

					time = getTimeFromWords(data.split(" "))
					response['time'] = time 

					# Update the visual to indicate that an alarm is on
					global AlarmOnOffVisual
					AlarmOnOffVisual = "ALARM SET"

					# update visual with new alarm time
					global AlarmTimeVisual
					AlarmTimeVisual = time

					# Turn snooze off if it was on
					global SnoozeVisual
					SnoozeVisual = "OFF"

					return JsonResponse(response, safe=False)

				elif word in offWords:
					response['command'] = "off"

					# Update the visual to indicate that an alarm is on
					global AlarmOnOffVisual
					AlarmOnOffVisual = "NO ALARM SET"

					# update visual with new alarm time
					global AlarmTimeVisual
					AlarmTimeVisual = None

					# Turn snooze off if it was on
					global SnoozeVisual
					SnoozeVisual = "OFF"


					return JsonResponse(response, safe=False)

				elif word in snoozeWords:
					response['command'] = "snooze"

					# Turn snooze off if it was on
					global SnoozeVisual
					SnoozeVisual = "ON"
					
					return JsonResponse(response, safe=False)

			response['command'] = data
		
			return JsonResponse(response, safe=False)

		else:
			response['textFromFile'] = "failed"
			return JsonResponse(response, safe=False)


@csrf_exempt
def showHomePage(request):	
	global AlarmTimeVisual
	print(AlarmTimeVisual)
	return render(request, 'home.html', {'AlarmTimeVisual': AlarmTimeVisual, 'AlarmOnOffVisual': AlarmOnOffVisual, 'SnoozeVisual': SnoozeVisual})


def getTimeFromWords(data):

	time = 0;
	mag = 1;

	hour = ""
	minutes = 0
	timeOfDay = "am"

	hourFound = False

	for word in data:
		if word == "pm":
				timeOfDay = "pm"

		if word in units:
			if hourFound == False:
				hour = str(units.index(word))
				hourFound = True 
			else:
				minutes += units.index(word)

	if minutes < 10:
		minutes = "0" + str(minutes);

	return hour + ":" + str(minutes) + " " + timeOfDay







			
