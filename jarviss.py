import speech_recognition as sr   # Speech recognition library
import pyttsx3               # Text-to-speech library
import webbrowser            # Web browser control library
import music_Lib
from gtts import gTTS  # Google Text-to-Speech library
import pygame
import os
import requests
from google import genai

recognizer = sr.Recognizer
engine = pyttsx3.init()

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text, lang = 'hi')
    tts.save('text.mp3')

    # Initialize the mixer module
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load("text.mp3")  

    # Play the music
    pygame.mixer.music.play()

    # Keep the program running until the music finishes
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10) 

    pygame.mixer.music.unload()
    os.remove("text.mp3")

def processCommand(command):
    command = command.lower()
    if "open google" in command:
        webbrowser.open("https://www.google.com")
        speak("Opening Google.")
    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube.")
    elif "open spotify" in command:  # opens spotify app
        spotify_path = r"C:\Users\sk282\AppData\Local\Microsoft\WindowsApps\Spotify.exe"
        os.startfile(spotify_path)
    elif command.lower().startswith("play"):
        song = command.lower().split("play", 1)[1].strip()
        if song in music_Lib.music.keys():
            link = music_Lib.music[song]
            webbrowser.open(link)
            speak(f"Playing {song} on Youtube.")
        else:
            speak("Sorry, I couldn't find that song.")
    elif "news" in command.lower().strip():
     newsapi = 'd40e87a85ebe26926e120ab1041d64ac'
     try:
        r = requests.get(f"https://gnews.io/api/v4/top-headlines?country=in&category=general&apikey={newsapi}")

        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])

            if articles:
                for article in articles[:5]:  # Limit to top 5
                    print("Headline:", article['title'])
                    speak(article['title'])
            else:
                print("No news articles found.")
                speak("Sorry, I couldn't find any news headlines right now.")
        else:
            print("Failed to fetch news:", r.status_code)
            speak("Sorry, I couldn't connect to the news service.")
     except Exception as e:
        print("Error:", e)
        speak("An error occurred while fetching the news.")

    else:
     try:
        client = genai.Client(api_key="AIzaSyCMjgPmegK0pErXWZlndWr8joYOjiu6njo")

        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=f"{command}"
        )
        print(response.text)
        speak(response.text)
     except Exception as e:
        print("LLM API Error:", e)
        speak("Sorry, I couldn't process that request.")

         

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        r = sr.Recognizer()

        print('Recognizing...')
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout = 2, phrase_time_limit = 1)
                word = r.recognize_google(audio)
                if word.lower() == "jarvis":
                    speak("Yes, how can I help you?")
                    print("Listening for command...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    print(f"Command received: {command}")

                    processCommand(command)
         
        
        except Exception as e:
            print("Error: " + str(e))
            continue


import tkinter as tk
from tkinter import messagebox
import threading

def on_gui_command():
    user_command = command_entry.get()
    if user_command:
        try:
            processCommand(user_command)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process command: {e}")
    else:
        messagebox.showwarning("Input Needed", "Please enter a command.")

# GUI setup
def launch_gui():
    global command_entry
    root = tk.Tk()
    root.title("Jarvis GUI")
    root.geometry("400x200")

    tk.Label(root, text="Enter your command:").pack(pady=10)
    command_entry = tk.Entry(root, width=50)
    command_entry.pack(pady=5)

    tk.Button(root, text="Execute", command=on_gui_command).pack(pady=20)

    root.mainloop()

# Voice assistant loop
def start_voice_assistant():
    speak("Initializing Jarvis...")
    while True:
        r = sr.Recognizer()
        print('Recognizing...')
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
                word = r.recognize_google(audio)
                if word.lower() == "jarvis":
                    speak("Yes, how can I help you?")
                    print("Listening for command...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    print(f"Command received: {command}")
                    processCommand(command)
        except Exception as e:
            print("Error: " + str(e))
            continue

# Start both GUI and voice assistant in parallel
if __name__ == "__main__":
    threading.Thread(target=start_voice_assistant, daemon=True).start()
    launch_gui()
