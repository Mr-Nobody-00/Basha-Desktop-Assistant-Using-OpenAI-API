import speech_recognition as sr
import os
import webbrowser
import datetime
import win32com.client 
speaker = win32com.client.Dispatch("SAPI.SpVoice")  # Only For Windows User
import datetime
import random
import numpy as np
import pandas as pd
import joblib
import subprocess
import nltk
from fuzzywuzzy import process


chatStr = ""

def say(text):
    speaker.speak(text) # For Mac Just give os.system(f"say {text}")

# Voice Recognition
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.8
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language= "en-in")
            print(f"User Said: {query}")
            return query
        except Exception as e:
            return "Some Error Occured Boss Sorry from Baaasha"


# Preprocess: Normalize text (lowercase, remove punctuation)
def preprocess_text(text):
    text = text.lower()
    text = "".join([char for char in text if char.isalnum() or char.isspace()])
    return text

# Function to find the closest matching command
def get_best_match(command_text):
    command_text = preprocess_text(command_text)
    command_list = df["Command"].tolist()
    
    best_match, score = process.extractOne(command_text, command_list)
    if score > 80:
        return best_match
    return None

# Function to predict and execute command
def process_command(command_text):
    best_match = get_best_match(command_text)
    if not best_match:
        print("Sorry, I couldn't recognize that command.")
        return

    X_test = vectorizer.transform([best_match])
    predicted_action = model.predict(X_test)[0]

    # Get execution path
    action_path = df.loc[df["Action"] == predicted_action, "Path"].values[0]

    print(f"Executing: {predicted_action} ({action_path})")

    try:
        subprocess.run(action_path, shell=True)
    except Exception as e:
        print(f"Error executing command: {e}")


if __name__ =='__main__':
    say("Hey I am Baaasha A i ")
    # Load trained model and vectorizer
    model = joblib.load("model.pkl")
    vectorizer = joblib.load("vectorizer.pkl")
    df = pd.read_csv("processed_commands.csv")
    while True:
        print("Listening...")
        query = takecommand()
        print(query)
        process_command(query)

        sites = [["youtube","https://Youtube.com"], ["movie","https://1tamilmv.bike"], ["github","https://github.com"], ["chat","https://chatgpt.com/"], ]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} boss")
                webbrowser.open(site[1])
        if "the time".lower() in query.lower():
            hr = strfTime = datetime.datetime.now().strftime("%H")
            min = strfTime = datetime.datetime.now().strftime("%M")
            sec = strfTime = datetime.datetime.now().strftime("%S")
            say(f"Boss the time is {hr} {min}")

        elif "open spotify".lower() in query.lower():
            path = os.system("where spotify")
            os.system("start C:/Users/harim/AppData/Local/Microsoft/WindowsApps/Spotify.exe")

        elif "Quit".lower() in query.lower():
            exit()

        # say(query)