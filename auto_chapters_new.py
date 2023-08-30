
import requests
import pprint
import json

auth_key = '2f7d2ca034c5427e81a225a22e70c0ee'

upload_endpoint = 'https://api.assemblyai.com/v2/upload'
transcript_endpoint = 'https://api.assemblyai.com/v2/transcript'

headers_auth_only = {"authorization": auth_key}

headers = {
    "authorization": auth_key,
    "content-type": "application/json"
}

CHUNK_SIZE = 5_242_880 # 5 MB

def upload(filename):  # Added filename parameter here
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
            
        filename = transcript_id + '_chapters.json'
        with open(filename, 'w') as f:
            chapters = polling_response.json()['chapters']
            json.dump(chapters,f,indent=4)

        print('Transcript saved')
    

if __name__ == "__main__":
    filename = 'videoplayback.mp3'
    #url = upload(filename)  # Call the upload function with the filename argument
    url = 'https://cdn.assemblyai.com/upload/d685c33c-165f-4795-b1bd-056abc8fd79a'
    #transcript_id = transcribe(url,auto_chapters=True)
    transcript_id = '631qogdlg6-d74e-49db-9d69-aae224730c37'
    poll(transcript_id)
