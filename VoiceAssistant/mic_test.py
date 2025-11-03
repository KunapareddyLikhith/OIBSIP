import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print("🎤 Say something...")
    audio = r.listen(source)

try:
    print("Recognizing...")
    text = r.recognize_google(audio)
    print("✅ You said:", text)
except sr.UnknownValueError:
    print("❌ Could not understand audio")
except sr.RequestError as e:
    print("❌ Could not request results; {0}".format(e))
