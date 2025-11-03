import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia
import requests

# Initialize the speech engine
engine = pyttsx3.init()

def speak(text):
    """Converts text to speech"""
    engine.say(text)
    engine.runAndWait()

def greet_user():
    """Greets the user based on the current time"""
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning!")
    elif hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am your Voice Assistant. How can I help you today?")

def take_command():
    """Takes voice input from the user and returns text"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}")
    except Exception:
        speak("Sorry, I didn't catch that. Please repeat.")
        return "None"
    return query.lower()

def get_weather(city):
    """Fetches weather details using OpenWeatherMap API"""
    api_key = "YOUR_API_KEY"  # Replace with your OpenWeatherMap key
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    data = response.json()
    if data["cod"] == 200:
        main = data["main"]
        speak(f"The temperature in {city} is {main['temp']} degree Celsius with {data['weather'][0]['description']}.")
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
            webbrowser.open("https://youtube.com")
            speak("Opening YouTube")

        elif 'open google' in query:
            webbrowser.open("https://google.com")
            speak("Opening Google")

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M")
            speak(f"The time is {strTime}")

        elif 'weather' in query:
            speak("Please tell me the city name.")
            city = take_command()
            get_weather(city)

        elif 'exit' in query or 'quit' in query:
            speak("Goodbye! Have a nice day.")
            break

        else:
            speak("Sorry, I didn't understand that.")

if __name__ == "__main__":
    main()
