
import re
import nltk
from nltk.tokenize import word_tokenize

# Download tokenizer data once if required
try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab", quiet=True)


def detect_intent(command):

    command = command.lower().strip()

    # Tokenization
    words = word_tokenize(command)

    # Greeting intent
    if any(word in words for word in ["hello", "hi", "hey"]):
        return "greeting", None

    # Time intent
    if any(word in words for word in ["time", "clock"]):
        return "time", None

    # Date intent
    if any(word in words for word in ["date", "today"]):
        return "date", None

    # Search intent
    search_patterns = [
        r"search(?:\s+for)?\s+(.+)",
        r"look\s+up\s+(.+)",
        r"find\s+information\s+about\s+(.+)",
        r"google\s+(.+)",
        r"find\s+(.+?)\s+online"
    ]

    for pattern in search_patterns:
        match = re.search(pattern, command)

        if match:
            return "search", match.group(1).strip()

    # Exit intent
    if any(word in words for word in [
        "exit", "quit", "goodbye", "stop"
    ]):
        return "exit", None
    
    
    # Reminder intent
    reminder_patterns = [
        r"remind me to (.+?) in (\d+)\s*(seconds?|minutes?|hours?)",
        r"set a reminder to (.+?) in (\d+)\s*(seconds?|minutes?|hours?)",
        r"remind me (.+?) after (\d+)\s*(seconds?|minutes?|hours?)"
    ]

    for pattern in reminder_patterns:
        match = re.search(pattern, command)

        if match:
            message = match.group(1).strip()
            amount = int(match.group(2))
            unit = match.group(3)

            if unit.startswith("minute"):
                amount *= 60
            elif unit.startswith("hour"):
                amount *= 3600

            return "reminder", {
                "message": message,
                "seconds": amount
            }
    
    # Weather intent
    weather_patterns = [
        r"weather (?:in|at) (.+)",
        r"(?:what is|what's|tell me) (?:the )?weather (?:in|at) (.+)",
        r"temperature (?:in|at) (.+)",
        r"how is the weather (?:in|at) (.+)"
    ]

    for pattern in weather_patterns:
        match = re.search(pattern, command)

        if match:
            return "weather", match.group(1).strip()
    
    # Weather intent
    weather_patterns = [
        r"\bweather\b.*?\b(?:in|at)\s+(.+)",
        r"\btemperature\b.*?\b(?:in|at)\s+(.+)",
        r"\b(?:in|at)\s+(.+?)\s+weather\b",
    ]

    for pattern in weather_patterns:
        match = re.search(pattern, command)

        if match:
            city = match.group(1).strip()
            return "weather", city
    
    
    
    # Flexible Email Intent Recognition

    email_pattern = (
        r"\bemail\s+to\s+(.+?)\s+"
        r"(?:saying|that says|that|with message|message is)\s+"
        r"(.+)"
    )

    match = re.search(email_pattern, command, re.IGNORECASE)

    if match:
        recipient = match.group(1).strip()
        body = match.group(2).strip()

        # Convert spoken email symbols
        recipient = re.sub(r"\s+at\s+", "@", recipient)
        recipient = re.sub(r"\s+dot\s+", ".", recipient)

        # Remove spaces within the email address
        recipient = re.sub(r"\s+", "", recipient)

        recipient = recipient.strip(".,!?")

        # Validate email address
        email_validation = (
            r"^[A-Za-z0-9._%+-]+@"
            r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        )

        if re.fullmatch(email_validation, recipient):
            return "email", {
                "recipient": recipient,
                "body": body
            }

        return "email_invalid", None
    
    # General knowledge question intent

    knowledge_patterns = [
        r"^(what|who|where|when|why|how)\b",
        r"^(explain|define|describe)\b",
        r"^tell me about\b",
        r"^can you explain\b"
    ]

    for pattern in knowledge_patterns:
        if re.search(pattern, command):
            return "knowledge", command

    return "unknown", None
