import os
import webbrowser
import subprocess
import pyttsx3
import speech_recognition as sr
import time



def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 175)
    engine.setProperty('voice', 'com.apple.speech.synthesis.voice.samantha')
    print("Babu:", text)
    try:
        engine.say(text)
        engine.runAndWait()
        time.sleep(0.2)  # tiny pause to avoid blocking next listen
    except Exception as e:
        print("Speech error:", e)

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.9)
        print("🎧 Listening...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        speak("Network issue. Please check your internet.")
        return ""

def open_application(app_name):
    try:
        apps = {
            "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "vs code": r"C:\Users\Dell\AppData\Local\Programs\Microsoft VS Code\Code.exe"
        }

        if app_name in apps:
            subprocess.Popen(apps[app_name])
            speak(f"Opening {app_name}")
        else:
            subprocess.Popen(f"start {app_name}", shell=True)
            speak(f"Trying to open {app_name}")
    except Exception as e:
        speak(f"Sorry, I couldn’t open {app_name}. Error: {e}")

import google.generativeai as genai
import os

# Add this at the top with other imports
genai.configure(api_key="AIzaSyCOivo8EfipN5YIC5IpFpDOhbbqFDYFNBU")
model = genai.GenerativeModel('gemini-2.5-flash')

# Add this function anywhere before main()
def get_ai_response(user_message):
    """Get AI response from Gemini"""
    try:
        response = model.generate_content(user_message)
        ai_reply = response.text
        return ai_reply
    
    except Exception as e:
        print(f"AI Error: {e}")
        return "Sorry, I'm having trouble thinking right now."
        
def process_command(command):
    if "open" in command:
        app_name = command.replace("open", "").strip()
        open_application(app_name)

    elif "search" in command:
        query = command.replace("search", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")
        speak(f"Searching for {query}")

    elif "youtube" in command:
        query = command.replace("youtube", "").strip()
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
        speak(f"Showing results for {query} on YouTube")

    elif any(x in command for x in ["exit", "quit", "stop"]):
        speak("Goodbye Dhanesh!")
        exit()

    else:
        speak("Sorry, I didn’t understand that command.")

def main():
    speak("Hey Dhanesh, I'm always listening. Say 'Babu' to wake me up.")
    
    while True:
        command = listen()
        print(f"RAW COMMAND: {command}")

        if command and command.lower().strip().startswith("babu"):
            print("DEBUG: Wake word detected!")
            #REMOVE BABU AND PRINT THE COMMAND
            command = command.replace("babu", "").strip()

            
            print(f"DEBUG: User said: '{command}'")

            if command:
                # Exit check
                if any(word in command.lower() for word in ["exit", "quit", "goodbye", "stop"]):
                    speak("Goodbye Dhanesh!")
                    break

                # Check if it matches a known command
                if any(keyword in command.lower() for keyword in ["open", "search", "youtube"]):
                    process_command(command)
                else:
                    # Default to AI response
                    ai_response = get_ai_response(command+"SUMMARIZE IN 10 WORDS")
                    print(f"AI Response: {ai_response}")
                    speak(ai_response)
            else:
                speak("I didn't hear anything. Please try again.")
        
        time.sleep(0.3)

if __name__ == "__main__":
    main()
