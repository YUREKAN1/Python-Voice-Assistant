# Python Voice Assistant

A Python-based voice assistant that recognizes spoken commands and responds using text-to-speech. It supports everyday tasks such as checking the time and date, searching the web, setting reminders, checking weather information, answering basic knowledge questions, and executing custom commands.

## Features

### Beginner Features
- **Speech Recognition:** Converts spoken commands into text using SpeechRecognition.
- **Voice Greeting:** Responds to greeting commands.
- **Time and Date:** Announces the current time and date.
- **Web Search:** Opens Google search results based on voice commands.
- **Text-to-Speech:** Uses pyttsx3 to provide spoken responses.
- **Error Handling:** Handles microphone, speech recognition, and network errors.

### Advanced Features
- **Intent Recognition:** Identifies the purpose of user commands using NLTK and regular expressions.
- **Reminders:** Sets timed reminders using Python threading.
- **Weather Updates:** Retrieves current weather information using the OpenWeatherMap API.
- **Knowledge Base:** Answers predefined questions using a local JSON knowledge base.
- **Custom Commands:** Supports configurable commands through `commands.json`.

### Email Integration
An SMTP email module has been developed, but email sending is currently paused and has not been verified as a working feature in the active assistant.

## Technologies Used

- Python 3
- SpeechRecognition
- PyAudio
- pyttsx3
- NLTK
- Requests
- Python-dotenv
- OpenWeatherMap API
- JSON
- Threading

## Project Structure

```text
Yurekan_1/
│
├── main.py
├── intent_recognition.py
├── reminder.py
├── weather.py
├── email_sender.py
├── knowledge_base.py
├── knowledge.json
├── custom_commands.py
├── commands.json
├── requirements.txt
├── README.md
├── .gitignore
└── .env
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd Yurekan_1
```

### 2. Create a virtual environment

```bash
python -m venv task1env
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
task1env\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Note:** PyAudio installation may require additional Windows-specific setup if pip cannot install it directly.

### 5. Configure the weather API

Create a `.env` file in the project root directory.

Add your OpenWeatherMap API key:

```env
OPENWEATHER_API_KEY=your_api_key_here
```

Replace the placeholder with your actual API key.

Keep `.env` private. Do not upload it to GitHub.

## Running the Assistant

Start the application using:

```bash
python main.py
```

The assistant will start listening for voice commands.

Examples:

| Voice command | Expected action |
|---|---|
| Hello | Greets the user |
| What is the time? | Announces current time |
| What is today's date? | Announces current date |
| Search for Python tutorials | Opens Google search |
| Remind me to study in 10 minutes | Sets a reminder |
| Weather in Chennai | Retrieves weather information |
| What is Python? | Answers from the knowledge base |
| Stop the assistant | Exits the application |

The exact supported command phrases depend on the intent patterns implemented in `intent_recognition.py`.

## Custom Commands

Custom commands are stored in `commands.json`.

You can extend the assistant by adding supported command configurations to this file.

The current custom command manager supports:
- Opening URLs.
- Searching the web.

Follow the structure of the existing entries in `commands.json` when adding commands.

## Knowledge Base

The assistant uses `knowledge.json` to store predefined questions and answers.

You can extend its knowledge by adding more question-answer entries to the JSON file.

The assistant uses text similarity matching to find relevant answers. If no sufficiently similar answer is found, it responds with a fallback message.

## Privacy and Data Handling

This project uses external services for some features.

- **Speech Recognition:** Audio is sent to Google's speech recognition service through the `recognize_google()` method. This project does not implement local-only speech recognition.
- **Weather:** The application sends weather requests to OpenWeatherMap using the configured API key and requested city.
- **Web Search:** Search queries are sent to Google through the user's browser.
- **Knowledge Base:** Questions and answers in `knowledge.json` are processed locally.
- **Custom Commands:** Configurations in `commands.json` are processed locally. Opening websites and searching the web involve external services.
- **Reminders:** Reminders are stored in application memory and are not designed to persist after the application closes.
- **Email:** Email functionality is currently paused. The SMTP module exists, but sending emails is not part of the active verified workflow.

The project does not intentionally save microphone recordings to disk.

## Limitations

- An active internet connection is required for Google speech recognition, web searches, and weather requests.
- Weather updates require a valid OpenWeatherMap API key.
- The knowledge base only answers questions represented by its stored entries.
- Reminders are temporary and are lost when the application exits.
- Speech recognition accuracy can vary depending on microphone quality, background noise, and pronunciation.
- Email sending has not been verified and is not currently active.

## Future Improvements

- Integrate a larger knowledge base or an external question-answering API.
- Improve natural language understanding.
- Add local speech recognition for better privacy.
- Improve reminder reliability and persistence.
- Complete and test email integration.
- Add more configurable custom commands.

## Author

**Yurekan M**

GitHub: https://github.com/YUREKAN1

Portfolio: https://yurekan-portfolio.vercel.app/
