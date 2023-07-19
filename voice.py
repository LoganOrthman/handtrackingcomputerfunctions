import speech_recognition as sr
import pyttsx3
import pyautogui

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
recognizer = sr.Recognizer()

def execute_command(command):
    if "Open Brave" in command:
        pyautogui.hotkey('win')
        pyautogui.typewrite('brave')
        pyautogui.hotkey('enter')
        print("Opening Brave browser...")
        # Add any additional actions you want to perform after opening Brave
    else:
        print("Command not recognized.")

def cmd():
    while True:
        with sr.Microphone() as source:
            print('Clearing')
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Ask me anything")
            recorded_audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(recorded_audio)
            print("Heard:", command)
            execute_command(command)
        except sr.UnknownValueError:
            print("Sorry, I could not understand what you said.")
        except sr.RequestError as e:
            print("Sorry, an error occurred. {0}".format(e))

cmd()
