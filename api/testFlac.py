import json
from os.path import join, dirname
from watson_developer_cloud import SpeechToTextV1

speech_to_text = SpeechToTextV1(
    username='6d1d6655-b091-4232-bb3c-72f35b924f63',
    password='PiNCxqb5uTbe',
    x_watson_learning_opt_out=False
)

#print(json.dumps(speech_to_text.models(), indent=2))

#print(json.dumps(speech_to_text.get_model('en-US_BroadbandModel'), indent=2))

with open(join(dirname(__file__), 'test2.flac'),
          'rb') as audio_file:
    print(json.dumps(speech_to_text.recognize(
        audio_file, content_type='audio/flac'), indent=2))
		
		# timestamps=True,
        # word_confidence=True),
        # indent=2))