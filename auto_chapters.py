import requests
import json
import pprint
import  sys
from api_secrets import API_KEY_ASSEMBLYAI


upload_endpoint = 'https://api.assemblyai.com/v2/upload'
transcript_endpoint = 'https://api.assemblyai.com/v2/transcript'


headers_auth_only = {"authorization": API_KEY_ASSEMBLYAI}

headers = {
    "authorization": API_KEY_ASSEMBLYAI,
    "content-type":"application/json"
    }

CHUNK_SIZE = 5_242_880

def upload(filename):
    def read_file(filename):
        with open(filename, 'rb') as f:
            while True:
                data = f.read(CHUNK_SIZE)
                if not data:
                    break
                yield data

    upload_response = requests.post(upload_endpoint,
                                    headers=headers_auth_only, 
                                    data=read_file(filename))
    pprint.pprint(upload_response.json())
    return upload_response.json()['upload_url'] 


def transcribe(audio_url,auto_chapters=False):
    transcript_request = {
        'audio_url': audio_url,
        'auto_chapters': 'True' if auto_chapters else 'False'
    } 

    transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=headers)
    pprint.pprint(transcript_response.json())
    return transcript_response.json()['id']


        
def poll(transcript_id):
    polling_endpoint = transcript_endpoint + '/' + transcript_id
    polling_response = requests.get(polling_endpoint, headers=headers)
    
    if polling_response.json()['status'] == 'completed':
        filename = transcript_id + '.txt'
        with open(filename, 'w') as f:
            f.write(polling_response.json()['text'])
        

        text_filename = transcript_id + '_chapters.json'
        with open(text_filename, 'w') as f:
            chapters = polling_response.json()['chapters']
            json.dump(chapters,f,indent=4)

        print('Transcript saved')

                



# if __name__ == "__main__":
    filename = 'wildfires.wildfires.mp3'
    # audio_url = upload(filename)
    # audio_url = 'https://cdn.assemblyai.com/upload/5c0fe6dc-e180-4767-ac4b-6d88b0c2d00d'

    # transcript_id = transcribe(audio_url,auto_chapters=True)
    transcript_id = '6qwc36jlzt-4ade-4880-80d0-a16f82c6e283'
    poll(transcript_id)