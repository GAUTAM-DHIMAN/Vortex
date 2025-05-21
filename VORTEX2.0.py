import pyttsx3
import speech_recognition as sr
import pywhatkit as kit
import wikipedia
import webbrowser
import datetime
import requests
from bs4 import BeautifulSoup
import os
import cv
import numpy as np
from tensorflow.keras.models import load_model

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User  said: {query}\n")
            return query.lower()

        except sr.UnknownValueError:
            print("Sorry, I did not understand. Please try again.")
            return "None"
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return "None"

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning Sir")
    elif 12 <= hour < 18:
        speak("Good Afternoon Sir")
    else:
        speak("Good Evening Sir")
    speak("I am J.A.R.V.I.S. How can I assist you today?")

def open_website(website):
    webbrowser.open(website)
    speak(f"Opening {website}")

def search_wikipedia(query):
    speak('Searching Wikipedia...')
    results = wikipedia.summary(query, sentences=2)
    speak("According to Wikipedia")
    print(results)
    speak(results)

def send_message(contact, message):
    kit.sendwhatmsg(contact, message, datetime.datetime.now().hour, datetime.datetime.now().minute + 2)
    speak(f"Message sent to {contact}")

def get_weather(city):
    api_key = "your_api_key"  # Replace with your OpenWeatherMap API key
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    data = response.json()
    if data["cod"] != "404":
        main = data["main"]
        weather_desc = data["weather"][0]["description"]
        temp = main["temp"]
        speak(f"The temperature in {city} is {temp} degrees Celsius with {weather_desc}.")
    else:
        speak("City not found.")

def recognize_image():
    model = load_model('path_to_your_model.h5')  # Update with your model path
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(gray, (28, 28))  # Example for a digit recognition model
        img = img.reshape(1, 28, 28, 1) / 255.0  # Normalize and reshape

        predictions = model.predict(img)
        digit = np.argmax(predictions)

        cv2.putText(frame, f'Predicted: {digit}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow('Image Recognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break