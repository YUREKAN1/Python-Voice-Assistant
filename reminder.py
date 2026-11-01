
import threading
import time


class ReminderManager:

    def __init__(self, speak_callback):
        self.speak = speak_callback
        self.reminders = []
        self.lock = threading.Lock()

    def set_reminder(self, message, seconds):

        if seconds <= 0:
            self.speak("Reminder duration must be greater than zero.")
            return

        reminder = {
            "message": message,
            "seconds": seconds
        }

        with self.lock:
            self.reminders.append(reminder)

        thread = threading.Thread(
            target=self._trigger_reminder,
            args=(reminder,),
            daemon=True
        )

        thread.start()

        self.speak(
            f"Reminder set. I will remind you to {message} "
            f"in {seconds} seconds."
        )

    def _trigger_reminder(self, reminder):

        time.sleep(reminder["seconds"])

        with self.lock:
            if reminder in self.reminders:
                self.reminders.remove(reminder)

        self.speak(f"Reminder alert! {reminder['message']}")

    def get_reminders(self):

        with self.lock:
            return list(self.reminders)
