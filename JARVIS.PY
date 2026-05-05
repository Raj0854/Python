import os
import datetime
import webbrowser
import speech_recognition as sr
import pyttsx3
import time
import pyjokes
import threading
import json

MEMORY_FILE = "memory.json"


def load_memory():
    try:
        with open(MEMORY_FILE, "r") as file:
            return json.load(file)
    except:
        return {"owner": "", "likes": []}


def save_memory(memory):
    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file)


memory = load_memory()
if "data" not in memory:
    memory["data"] = {}
# Small delay
time.sleep(1)


# wake word
def listen_for_wake_word():
    print("\n🟡 Waiting for wake word...")

    command = take_command()

    if command == "":
        return "none"

    if "bye" in command or "stop" in command:
        return "bye sir!"

    if "jarvis" in command:
        speak("Yes sir?")
        return "wake"

    return "none"

# 🔊 Speak
def speak(text):
    def run():
        print("Jarvis:", text)
        engine = pyttsx3.init("sapi5")
        voices = engine.getProperty("voices")
        engine.setProperty("voice", voices[0].id)
        engine.setProperty("rate", 170)
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
        speak("Sorry, I didn't catch that. Please say that again.")
        return ""

    except Exception as e:
        print("Error:", e)
        return ""

# Faster listen for wake word
def listen_fast():
    r = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("...idle...")
            audio = r.listen(source, timeout=2, phrase_time_limit=2)

        command = r.recognize_google(audio)
        print("Heard:", command)
        return command.lower()

    except:
        return ""

# ⚠️ Confirmation
def confirm_action(action):
    speak(f"Do you want me to {action}? Say yes or no.")

    for _ in range(3):
        response = take_command()

        if response == "":
            continue

        print("Confirmation heard:", response)

        if any(
            word in response
            for word in ["yes", "yeah", "yup", "sure", "do it", "go ahead"]
        ):
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
    separators = [" and ", " then ", ",", "for"]
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
    if "my name is" in command or "i am" in command or "raj" in command:
        name = command.split("my name is")[-1].strip()

        if memory["owner"] == "":
            memory["owner"] = name
            save_memory(memory)
            speak(f"Nice to meet you {name}, welcome to Jarvis!")

        else:
            if name == memory["owner"]:
                speak(f"Welcome back {name} sir! i am your Jarvis")
            else:
                speak("Access denied")

        return
    elif "remember" in command:
        if not memory["owner"]:
            speak("Tell me your name first")
            return

        try:
            # Example: remember my city is pune
            content = command.replace("remember", "").strip()

            if "is" in content:
                key, value = content.split("is", 1)

                key = key.replace("my", "").strip()
                value = value.strip()

                memory["data"][key] = value
                save_memory(memory)

                speak(f"I will remember that your {key} is {value}")
            else:
                speak("Please say it like: remember my something is something")

        except:
            speak("I could not understand what to remember")
    elif "what is my" in command or "who is my" in command:
        key = (
            command.replace("what is my" or "who is my", "")
            .replace("who is my", "")
            .strip()
        )

        if key in memory["data"]:
            value = memory["data"][key]
            speak(f"Your {key} is {value}")
        else:
            speak(f"I don't know your {key} yet")

    elif "what is my name" in command or "who am i" in command:
        if memory["owner"]:
            speak(f"Your name is {memory['owner']}")
        else:
            speak(
                "I don't know your name yet, please tell me by saying 'my name is ...'"
            )

    elif "my fullname" in command or "what is my full name" in command:
        if memory["fullname"]:
            speak(f"Your full name is {memory['fullname']}, and i'm your Jarvis")
        else:
            speak("I don't know your full name yet, please tell me ")

    elif "what do i like" in command or "what are my likes" in command:
        if memory["likes"]:
            likes_text = ", ".join(memory["likes"])
            speak(f"You like {likes_text}")
        else:
            speak("I don't know what you like yet")

    elif "what do i dislike" in command or "what are my dislikes" in command:
        if memory["dislikes"]:
            dislikes_text = ", ".join(memory["dislikes"])
            speak(f"You dislike {dislikes_text}")
        else:
            speak("I don't know what you dislike yet")

    elif "i dislike" in command:
        if not memory["owner"]:
            speak("Tell me your name first")
            return

        dislike = command.split("i dislike")[-1].strip()

        if dislike and dislike not in memory["dislikes"]:
            memory["dislikes"].append(dislike)
            save_memory(memory)
            speak(f"Got it {memory['owner']}, you dislike {dislike}")
        else:
            speak("I already know that")

    elif "i like" in command:
        if not memory["owner"]:
            speak("Tell me your name first")
            return

        like = command.split("i like")[-1].strip()

        if like and like not in memory["likes"]:
            memory["likes"].append(like)
            save_memory(memory)
            speak(f"Got it {memory['owner']}, you like {like}")
        else:
            speak("I already know that")

    elif "what are my recent files" in command or "what are my recent file" in command:
        if memory["recent_files"]:
            files_text = ", ".join(memory["recent_files"])
            speak(f"Your recent files are {files_text}")
        else:
            speak("I don't know about your recent files yet")

    elif "add recent file" in command:
        if not memory["owner"]:
            speak("Tell me your name first")
            return

        file = command.split("add recent file")[-1].strip()

        if file and file not in memory["recent_files"]:
            memory["recent_files"].append(file)
            save_memory(memory)
            speak(f"Got it {memory['owner']}, added {file} to recent files")
        else:
            speak("I already know that or invalid file name")

    elif "time" in command:
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

    elif "bye" in command or "stop" in command:
        speak("okay bye sir, take care see you soon!")
        exit()
    elif "good" in command or "very good" in command or "nice" in command:
        speak("thank you sir, i'm trying to improve myself!")
    elif "idiot" in command or "stupid" in command or "not this" in command:
        speak("i'm sorry sir, i am working to improve myself!")
    elif "who made you" in command or "who created you" in command:
        speak("I was created by Raj Gupta, a passionate coder and tech enthusiast.")
    elif (
        "what can you do" in command
        or "what things can you do" in command
        or "tell me about yourself" in command
    ):
        speak(
            "i'm jarvis, your personal assistant. I can perform various tasks such as opening applications, searching the web, telling jokes, and remembering information about you. Just ask me to do something!"
        )

    elif "Thank you" in command or "thanks" in command:
        speak("My pleasure sir, I'm here to assist you anytime!")
    else:
        speak("I did not understand that command")


# 🔥 Smart search
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
    speak("System is online. Say Jarvis to activate.")

    active_mode = False

    while True:

        # 💤 IDLE MODE (only wake word)
        while not active_mode:
            command = listen_fast()

            if command == "":
                continue

            if "exit" in command:
                speak("Shutting down")
                return

            if "jarvis" in command:
                speak("Activated")
                active_mode = True
                break


        # 🎯 ACTIVE MODE (normal assistant)
        while active_mode:
            command = take_command()
            command = clean_command(command)

            if command == "":
                continue

            print("Command:", command)

            # 🔴 Exit completely
            if "exit" in command:
                speak("Shutting down")
                return

            # 💤 Go back to idle
            if "stop listening" in command:
                speak("Going idle")
                active_mode = False
                break

            # 🔍 Smart search
            if smart_search(command):
                continue

            # 🔀 Multi-command
            commands = split_commands(command)

            for cmd in commands:
                handle_command(cmd)
# Run
jarvis()
