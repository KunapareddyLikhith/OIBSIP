import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia
import requests

# Initialize the engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Choose voice (0 = male, 1 = female)
engine.setProperty('rate', 180)  # Speech speed

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def greet_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning!")
    elif hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am your voice assistant. How can I help you today?")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")
    except Exception:
        speak("Sorry, I didn't catch that. Could you please repeat?")
        return "None"
    return query.lower()

def get_weather(city):
    api_key = "2cb3ec42a06af93618ed87684f8fbba9"  # Replace this with your OpenWeatherMap key
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    data = response.json()

    if data["cod"] == 200:
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        speak(f"The temperature in {city} is {temp} degrees Celsius with {desc}.")
    else:
        speak("Sorry, I couldn't find that city.")

def main():
    greet_user()

    while True:
        query = take_command()

        if 'wikipedia' in query:
            speak("Searching Wikipedia...")
            results = wikipedia.summary(query.replace("wikipedia", ""), sentences=2)
            speak("According to Wikipedia")
            speak(results)

        elif 'open youtube' in query:
            speak("Opening YouTube")
            webbrowser.open("https://youtube.com")

        elif 'open google' in query:
            speak("Opening Google")
            webbrowser.open("https://google.com")

        elif 'time' in query:
            time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {time}")

        elif 'weather' in query:
            speak("Please tell me the city name.")
            city = take_command()
            get_weather(city)

        elif 'exit' in query or 'quit' in query or 'stop' in query:
            speak("Goodbye, have a great day!")
            break

        else:
            speak("Sorry, I didn't understand that command.")

if __name__ == "__main__":
    main()
