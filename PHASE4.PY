import os
import datetime
import webbrowser

import speech_recognition as sr
import pyttsx3
import time
import pyjokes
import threading

# Small delay
time.sleep(1)

# 🔊 Speak
def speak(text):
    def run():
        print("Jarvis:", text)
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        engine.setProperty('rate', 170)
        engine.say(text)
        engine.runAndWait()
        engine.stop()

    t = threading.Thread(target=run)
    t.start()
    t.join()

# 🎤 Listen
def take_command():
    r = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("\nListening...")
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=5, phrase_time_limit=6)

        command = r.recognize_google(audio)
        print("You:", command)
        return command.lower()

    except sr.WaitTimeoutError:
        print("Timeout: No speech detected")
        return ""

    except sr.UnknownValueError:
        speak("please say that again")
        return ""

    except Exception as e:
        print("Error:", e)
        return ""

# ⚠️ Confirmation
def confirm_action(action):
    speak(f"Do you want me to {action}? Say yes or no.")

    for _ in range(3):
        response = take_command()

        if response == "":
            continue

        print("Confirmation heard:", response)

        if any(word in response for word in ["yes", "yeah", "yup", "sure", "do it", "go ahead"]):
            return True
        elif any(word in response for word in ["no", "nope", "cancel", "stop"]):
            return False
        else:
            speak("Please say yes or no")

    return False

# 🧠 Clean command
def clean_command(command):
    fillers = ["please", "can you", "could you", "jarvis", "for me"]
    for word in fillers:
        command = command.replace(word, "")
    return command.strip()
# 🔥 Split multi-command
def split_commands(command):
    separators = [" and ", " then ", ","]
    parts = [command]

    for sep in separators:
        new_parts = []
        for p in parts:
            if sep in p:
                new_parts.extend(p.split(sep))
            else:
                new_parts.append(p)
        parts = new_parts

    return [p.strip() for p in parts if p.strip()]

# 🧠 Handle command (YOUR ORIGINAL LOGIC)
def handle_command(command):
    print("Processing:", command)

    if "time" in command:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {current_time}")

    elif "how are you" in command or "how r u" in command:
        speak("mai mast hu, aap kaise ho?")

    elif "who are you" in command or "hu r u" in command:
        speak("I am your personal assistant Jarvis")

    elif "youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "github" in command:
        speak("Opening GitHub")
        webbrowser.open("https://www.github.com")

    elif "notepad" in command:
        speak("Opening Notepad")
        os.system("notepad")

    elif "calculator" in command:
        speak("Opening Calculator")
        os.system("calc")

    elif "vs" in command or "visual studio" in command:
        speak("Opening Visual Studio Code")
        os.system("code")

    elif "music" in command or "song" in command:
        music_path = "C:\\Users\\RAJ GUPTA\\Music"
        try:
            songs = os.listdir(music_path)
            if songs:
                speak("Playing music")
                os.startfile(os.path.join(music_path, songs[0]))
            else:
                speak("No music found")
        except:
            speak("Music folder not found")

    elif "joke" in command or "funny" in command:
        speak(pyjokes.get_joke())

    # elif "search" in command:
    #     query = command.replace("search", "").strip()

    #     if not query:
    #         speak("What should I search?")
    #         query = take_command()

    #     if query:
    #         speak(f"Searching for {query}")
    #         webbrowser.open(f"https://www.google.com/search?q={query}")

    elif "image" in command or "picture" in command:
        query = command.replace("image", "").replace("picture", "").strip()

        if not query:
            speak("What image should I search for?")
            query = take_command()

        if query:
            speak(f"Searching for images of {query}")
            webbrowser.open(f"https://www.google.com/search?tbm=isch&q={query}")
        else:
            speak("I didn't catch the image search query")

    elif "folder" in command:
        speak("Opening your folder")
        os.startfile("C:\\Users\\RAJ GUPTA\\Desktop")

    elif "shutdown" in command:
        if confirm_action("shutdown the system"):
            speak("Shutting down")
            os.system("shutdown /s /t 1")

    elif "restart" in command:
        if confirm_action("restart the system"):
            speak("Restarting")
            os.system("shutdown /r /t 1")

    elif "exit" in command or "stop" in command:
        speak("Thik hai sir, bye!")
        exit()

    else:
        speak("I did not understand that command")

def smart_search(command):
    if "search" not in command:
        return False

    # Detect platform
    if "youtube" in command:
        platform = "youtube"
    elif "image" in command or "picture" in command:
        platform = "images"
    else:
        platform = "google"

    # Extract query
    query = command.replace("search", "")
    query = query.replace("on youtube", "").replace("on google", "")
    query = query.replace("youtube", "").replace("google", "")
    query = query.replace("image", "").replace("picture", "")
    query = query.strip()

    if not query:
        speak("What should I search?")
        query = take_command()

    if not query:
        speak("I didn't catch that")
        return True

    speak(f"Searching for {query}")

    if platform == "youtube":
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

    elif platform == "images":
        webbrowser.open(f"https://www.google.com/search?tbm=isch&q={query}")

    else:
        webbrowser.open(f"https://www.google.com/search?q={query}")

    return True
# 🤖 MAIN
def jarvis():
    speak("Hello sir, How can I help you?")

    while True:
        command = take_command()
        command = clean_command(command)

        if command == "":
            continue

        print("Processed:", command)

        # 🔥 FIRST check smart search
        if smart_search(command):
            continue

        commands = split_commands(command)

        for cmd in commands:
            handle_command(cmd)
# Run
jarvis()
