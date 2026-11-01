
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
from urllib.parse import quote_plus

from intent_recognition import detect_intent
from reminder import ReminderManager
from weather import get_weather
from knowledge_base import KnowledgeBase
from custom_commands import CustomCommandManager


# Initialize text-to-speech
engine = pyttsx3.init()
engine.setProperty("rate", 170)


# Initialize speech recognition
recognizer = sr.Recognizer()


def speak(message):
    """Speak a response and display it in the terminal."""
    print("Assistant:", message)
    engine.say(message)
    engine.runAndWait()


# Initialize assistant modules
reminder_manager = ReminderManager(speak)
knowledge_base = KnowledgeBase()
custom_manager = CustomCommandManager()


def listen():
    """Capture voice input and convert it into text."""

    try:
        with sr.Microphone() as source:
            print("\nListening...")

            recognizer.adjust_for_ambient_noise(
                source, duration=0.5
            )

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=10
            )

        command = recognizer.recognize_google(audio)
        command = command.lower().strip()

        print("You:", command)
        return command

    except sr.WaitTimeoutError:
        speak("I did not hear anything. Please try again.")

    except sr.UnknownValueError:
        speak("Sorry, I could not understand. Please repeat.")

    except sr.RequestError:
        speak(
            "Speech recognition is unavailable. "
            "Check your internet connection."
        )

    except OSError as error:
        print("Microphone error:", error)
        speak("I could not access the microphone.")

    except Exception as error:
        print("Unexpected error:", error)
        speak("Something went wrong while listening.")

    return ""


def handle_command(command):
    """Identify and execute a supported voice command."""

    if not command:
        return True

    # Check custom commands first
    custom_command = custom_manager.find_command(command)

    if custom_command:
        success, message = custom_manager.execute(custom_command)
        speak(message)
        return True

    # Identify the user's intent
    intent, entity = detect_intent(command)

    print("DEBUG INTENT:", intent)
    print("DEBUG ENTITY:", entity)

    # Greeting
    if intent == "greeting":
        speak("Hello! How can I help you?")

    # Current time
    elif intent == "time":
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")

    # Current date
    elif intent == "date":
        current_date = datetime.datetime.now().strftime(
            "%A, %d %B %Y"
        )
        speak(f"Today's date is {current_date}")

    # Web search
    elif intent == "search":
        if entity:
            url = (
                "https://www.google.com/search?q="
                + quote_plus(entity)
            )

            speak(f"Searching for {entity}")
            webbrowser.open(url)

        else:
            speak("Please tell me what you want to search for.")

    # Reminders
    elif intent == "reminder":
        reminder_manager.set_reminder(
            entity["message"],
            entity["seconds"]
        )

    # Weather
    elif intent == "weather":
        weather_data, error = get_weather(entity)

        if error:
            speak(error)

        else:
            message = (
                f"The weather in {weather_data['city']} is "
                f"{weather_data['condition']}. "
                f"Temperature is {weather_data['temperature']} "
                f"degrees Celsius. "
                f"It feels like {weather_data['feels_like']} degrees. "
                f"Humidity is {weather_data['humidity']} percent. "
                f"Wind speed is {weather_data['wind_speed']} "
                f"meters per second."
            )

            speak(message)

    # General knowledge questions
    elif intent == "knowledge":
        answer = knowledge_base.get_answer(entity)

        if answer:
            speak(answer)

        else:
            speak(
                "Sorry, I don't have an answer for that question yet. "
                "You can try asking something else."
            )

    # Exit assistant
    elif intent == "exit":
        speak("Goodbye! Have a great day.")
        return False

    # Unknown command
    else:
        speak(
            "Sorry, I couldn't identify your intention. "
            "Please try again."
        )

    return True


def main():
    """Main execution loop of the voice assistant."""

    speak("Voice assistant started. Say hello to begin.")

    try:
        while True:
            command = listen()

            if not handle_command(command):
                break

    except KeyboardInterrupt:
        speak("Voice assistant stopped.")

    finally:
        engine.stop()


if __name__ == "__main__":
    main()
