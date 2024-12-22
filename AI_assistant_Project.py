import speech_recognition as sr
import pyttsx3
import webbrowser
import requests
import random
from bs4 import BeautifulSoup

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 0.9)  # Volume level

# Function to change the assistant's voice
def change_voice(gender="female"):
    voices = engine.getProperty('voices')
    if gender == "female":
        engine.setProperty('voice', voices[1].id)  # Female voice
    else:
        engine.setProperty('voice', voices[0].id)  # Male voice

# Function to make the assistant speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to voice commands
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for background noise
        try:
            audio = recognizer.listen(source, timeout=5)
            print("Processing your command...")
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Could you repeat?")
            return None
        except sr.RequestError:
            speak("Sorry, I'm having trouble connecting to the speech recognition service.")
            return None

# Function to process commands
def process_command(command):
    if command is None:
        return

    if "hello" in command:
        speak("Hello! How can I assist you today?")

    elif "your name" in command:
        speak("My Model name is Lenovo, and intel(R) core i7, I am your AI assistant. How can I help you?")

    elif "time" in command:
        from datetime import datetime
        now = datetime.now().strftime("%H:%M:%S")
        speak(f"The current time is {now}.")

    elif "open" in command:
        if "google" in command:
            speak("Opening Google.")
            webbrowser.open("https://www.google.com")
        elif "youtube" in command:
            speak("Opening YouTube.")
            webbrowser.open("https://www.youtube.com")
        elif "facebook" in command:
            speak("Opening Facebook.")
            webbrowser.open("https://www.facebook.com")
        else:
            speak("Please specify a website to open.")

    elif "play" in command and "youtube" in command:
        query = command.replace("play", "").replace("on youtube", "").strip()
        speak(f"Searching YouTube for {query}.")
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

    elif "give me a story" in command:
        speak("Let me find a random story for you.")
        try:
            story = get_random_story()
            speak(story)
        except Exception as e:
            speak("Sorry, I couldn't fetch a story at the moment.")

    elif "change voice to male" in command:
        change_voice("male")
        speak("Voice changed to male.")

    elif "change voice to female" in command:
        change_voice("female")
        speak("Voice changed to female.")

    elif "exit" in command or "quit" in command:
        speak("Goodbye! Have a great day.")
        exit()

    else:
        speak("I'm sorry, I can't handle that command right now. Try something else.")

# Function to get a random story from the web
def get_random_story():
    url = "https://www.shortkidstories.com/story-category/random/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find story title and content
    story_title = soup.find("h1").text
    story_content = soup.find("div", class_="entry-content").text.strip()

    return f"Here is a story titled '{story_title}': {story_content}"

# Main loop
if __name__ == "__main__":
    change_voice("female")  # Set default voice to female
    speak("Hello, I am your AI assistant. How can I help you?")
    while True:
        command = listen()
        if command:
            process_command(command)
