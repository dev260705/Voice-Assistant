import tkinter as tk
from tkinter import Entry, Label, Button, Text
from PIL import Image, ImageTk
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import threading  # For threading the speech and recognition functions

# Initialize the speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    display_text(f"Speaking: {audio}")
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Caran.....how may I help you")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        display_text("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        display_text("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        display_text(f"User said: {query}")
    except Exception as e:
        display_text("Say that again please...")
        return "None"
    return query

def executeQuery(query):
    if 'according to wikipedia' in query:
        speak('Searching Wikipedia...')
        query = query.replace("about", "")
        try:
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            display_text(results)
            speak(results)
        except Exception as e:
            display_text("Sorry, I couldn't find any results.")

    elif 'open youtube' in query:
        speak("What should I search on YouTube?")
        search_query = takeCommand().lower()
        webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
        speak(f"Searching for {search_query} on YouTube")

    elif 'google' in query:
        speak("What should I search on Google?")
        search_query = takeCommand().lower()
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
        speak(f"Searching for {search_query} on Google")

    elif 'open stackoverflow' in query:
        webbrowser.open("https://stackoverflow.com")

    elif 'play music' in query:
        speak("What music would you like to listen?")
        music_query = takeCommand().lower()
        if music_query != "None":
            webbrowser.open(f"https://open.spotify.com/search/{music_query}")
            speak(f"Playing {music_query}")

    elif 'the time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Sir, the time is {strTime}")

    elif 'open whatsapp' in query:
        webbrowser.open("https://web.whatsapp.com/")

    elif 'run code' in query:
        codePath = "D:\\python programming\\calculator.py"
        os.startfile(codePath)
        speak("I am opening the specified code")

    elif 'send email to dev' in query:
        try:
            speak("What should I say?")
            content = takeCommand()
            to = "recipient@example.com"
            sendEmail(to, content)
            speak("Email has been sent!")
        except Exception as e:
            display_text("Sorry, I am not able to send the email.")

    elif 'tell about yourself' in query:
        response = "Hey! How are you? I am Caran, your favorite voice assistant. I am ready to help you with your queries."
        speak(response)
        display_text(response)
    # Additional commands can be added here...

def display_text(text):
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, text)

def onVoiceCommand():
    query = takeCommand().lower()
    if query != "None":
        executeQuery(query)

def onSubmit():
    query = entry.get().lower()
    if query:
        entry.delete(0, tk.END)
        executeQuery(query)

def greet_after_start():
    root.after(1000, wishMe)

# Set up GUI
root = tk.Tk()
root.title("Caran Voice Assistant")
root.geometry("600x700")
root.configure(bg="black")

# Title
title = Label(root, text="Caran Voice Assistant", font=("Arial", 24), fg="sky blue", bg="black")
title.pack(pady=20)

# Load and place glowing effect image
try:
    glow_image = Image.open("C:\\Users\\devyu\\OneDrive\\Pictures\\Screenshots 1\\Screenshot 2024-11-17 140656.png")  # Replace with your image file path
    glow_image = glow_image.resize((200, 200), Image.LANCZOS)
    glow_photo = ImageTk.PhotoImage(glow_image)
    glow_label = Label(root, image=glow_photo, bg="black")
    glow_label.pack(pady=10)
except Exception as e:
    display_text(f"Error loading glow image: {e}")

# Load and place microphone icon
try:
    mic_image = Image.open("D:\\istockphoto-1405947165-612x612.jpg")  # Replace with your microphone icon path
    mic_image = mic_image.resize((50, 50), Image.LANCZOS)
    mic_photo = ImageTk.PhotoImage(mic_image)
    mic_button = Button(root, image=mic_photo, command=lambda: threading.Thread(target=onVoiceCommand).start(), bg="black", borderwidth=0)
    mic_button.pack(pady=10)
except Exception as e:
    display_text(f"Error loading microphone icon: {e}")

# Entry box for text command
entry = Entry(root, font=("Arial", 16), width=30)
entry.pack(pady=10)

# Submit button
submit_button = Button(root, text="Submit", command=onSubmit, font=("Arial", 14), bg="sky blue", fg="black")
submit_button.pack()

# Text box to display Wikipedia results or other responses
result_text = Text(root, font=("Arial", 14), wrap="word", width=60, height=10, bg="black", fg="white")
result_text.pack(pady=20)

# Start the greeting after the GUI loads
greet_after_start()

# Run GUI main loop
root.mainloop()
