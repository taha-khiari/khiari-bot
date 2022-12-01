from googletrans import Translator
import speech_recognition as sr
r = sr.Recognizer()
mic=sr.Microphone()

with mic as source:
 while True:
    audio = r.listen(source)
    text=r.recognize_google(audio)
    print(text)

