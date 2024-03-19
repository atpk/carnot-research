#!/usr/bin/env python
# coding: utf-8

# In[5]:


import speech_recognition as sr
from openai import OpenAI
import json
import requests
import time
from elevenlabs import generate
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
from io import BytesIO

# Set up OpenAI API key
API_KEY = "X"
client = OpenAI(api_key=API_KEY)

def generate_text(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful voice assistant"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=50
    )

    # Extract the generated text from the response
    generated_text = response.choices[0].message.content
    print("Generated Text:", generated_text)
    return generated_text

def record_and_recognize():
    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Listening...")

        # Adjust ambient noise for better recognition
        recognizer.adjust_for_ambient_noise(source)

        # Record the audio
        audio_data = recognizer.listen(source)

        print("Processing...")

        try:
            # Recognize speech using Google Speech Recognition
            text = recognizer.recognize_google(audio_data)
            print("You said:", text)
            return text
        except sr.UnknownValueError:
            print("Sorry, could not understand audio.")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

def generate_audio(text):
    url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"
    headers = {
        "accept": "audio/mpeg",
        "xi-api-key": "X",
        "Content-Type": "application/json"
    }
    params = {"optimize_streaming_latency": 0}

    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8,
            "style": 0.0,
            "use_speaker_boost": True
        }
    }

    response = requests.post(url, headers=headers, params=params, data=json.dumps(data))

    if response.status_code == 200:
        print("Audio generated successfully")
        return response.content
    else:
        print(f"Error: {response.status_code}")
        print(response.text)            


if __name__ == "__main__":
    
    while True:
        # record speech and convert to text in real time
        input_text = record_and_recognize()

        # Generate new text using OpenAI API
        generated_text = generate_text(input_text)

        # Synthesize the generated text using Eleven Labs API
        audio_data = generate_audio(generated_text)

        # Load the audio data directly from a BytesIO buffer
        audio = AudioSegment.from_file(BytesIO(audio_data))

        # Play the audio
        play(audio)

        # Add a delay of 1 second before recording speech again
        time.sleep(1)

