
import os
import smtplib

from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()


def send_email(recipient, subject, body):
    """Send an email using Gmail SMTP."""

    sender = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")

    if not sender or not password:
        return False, "Email credentials are missing from the .env file."

    if not recipient or "@" not in recipient:
        return False, "Invalid recipient email address."

    try:
        message = EmailMessage()

        message["From"] = sender
        message["To"] = recipient
        message["Subject"] = subject

        message.set_content(body)

        with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()

            server.login(sender, password)

            server.send_message(message)

        return True, "Email sent successfully."

    except smtplib.SMTPAuthenticationError:
        return False, "Gmail authentication failed. Check your app password."

    except smtplib.SMTPRecipientsRefused:
        return False, "Gmail rejected the recipient address."

    except (smtplib.SMTPException, OSError) as error:
        print("Email delivery error:", error)
        return False, "Unable to send the email. Please check your connection and Gmail settings."

