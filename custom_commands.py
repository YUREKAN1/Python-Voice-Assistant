
import json
import webbrowser

from pathlib import Path
from urllib.parse import quote_plus, urlsplit


class CustomCommandManager:

    def __init__(self, file_path="commands.json"):
        self.file_path = Path(file_path)
        self.commands = []
        self.load_commands()

    def load_commands(self):
        """Load custom commands from JSON."""

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            commands = data.get("commands", [])

            if not isinstance(commands, list):
                raise ValueError("Commands must be a list.")

            self.commands = commands

        except FileNotFoundError:
            print("commands.json not found.")
            self.commands = []

        except (json.JSONDecodeError, ValueError) as error:
            print("Invalid command configuration:", error)
            self.commands = []

    def normalize(self, text):
        return " ".join(text.lower().strip().split())

    def find_command(self, spoken_text):
        """Find an exact matching custom phrase."""

        spoken_text = self.normalize(spoken_text)

        for command in self.commands:
            for phrase in command.get("phrases", []):

                if self.normalize(phrase) == spoken_text:
                    return command

        return None

    def valid_url(self, url):
        """Allow only valid HTTPS URLs."""

        try:
            parsed = urlsplit(url)

            return (
                parsed.scheme == "https"
                and bool(parsed.hostname)
                and parsed.username is None
                and parsed.password is None
            )

        except ValueError:
            return False

    def execute(self, command):
        """Execute a matched custom command."""

        action = command.get("action")
        value = command.get("value")

        if action == "open_url":

            if not isinstance(value, str) or not self.valid_url(value):
                return False, "Invalid or unsafe URL."

            opened = webbrowser.open(value)

            if opened:
                return True, "Opening your requested website."

            return False, "Unable to open the website."

        elif action == "search_web":

            if not isinstance(value, str) or not value.strip():
                return False, "Invalid search query."

            url = "https://www.google.com/search?q=" + quote_plus(value)
            opened = webbrowser.open(url)

            if opened:
                return True, f"Searching for {value}."

            return False, "Unable to open the search page."

        return False, "Unsupported custom command action."
