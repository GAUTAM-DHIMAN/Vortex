import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning Sir")
    elif 12 <= hour < 18:
        speak("Good Afternoon Sir")
    else:
        speak("Good Evening Sir")
    speak("I am Vortex. How may I help you?")

def takeCommand():
    # It takes microphone input from the user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
            return query.lower()

        except sr.UnknownValueError:
            print("Sorry, I did not understand. Please try again.")
            return "None"
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return "None"

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('officialsharma1122@gmail.com', 'Dhiman@123')
    server.sendmail('officialsharma@gmail.com', to, content)
    server.close()

if __name__ == "__main__":
    wishMe()

    while True:
    
        
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=4)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("https://www.youtube.com")
            speak("Sir, opening youtube")

       
        elif 'open google' in query:
            webbrowser.open("google.com")
            
        elif 'play song on youtube' in query:
            speak("What should I play?")
            song = takeCommand().lower()
            webbrowser.open(f"https://www.youtube.com/results?search_query={song}")
            speak(f"Sir, playing {song} on youtube")  
            
            
        elif 'play music' in query:
            music_dir = 'D:\\song'
            songs = os.listdir(music_dir)
            print(songs)    
            os.startfile(os.path.join(music_dir, songs[0]))
            
            
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'open microsoft word' in query:
            codePath = "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE"
            os.startfile(codePath)

        elif 'email to Gautam' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "gautamdhimanamb@gmail.com"    
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry my friend Gautam . I am not able to send this email")
