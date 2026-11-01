from email_sender import send_email

success, message = send_email(
    "YOUR_OWN_GMAIL@gmail.com",
    "Voice Assistant Test",
    "This is a test email from my Python Voice Assistant."
)

print("Success:", success)
print("Message:", message)