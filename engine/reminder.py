import threading
import time
import datetime
import pyttsx3


reminders = []


def speak(message):
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()
    engine.stop()


def add_reminder(hour, minute, message):
    reminder = {
        "hour": hour,
        "minute": minute,
        "message": message
    }

    reminders.append(reminder)

    return f"Reminder set for {hour:02d}:{minute:02d}."


def reminder_checker():
    last_triggered = None

    while True:
        now = datetime.datetime.now()

        current_key = (
            now.year,
            now.month,
            now.day,
            now.hour,
            now.minute
        )

        for reminder in reminders.copy():

            if (
                now.hour == reminder["hour"]
                and now.minute == reminder["minute"]
                and last_triggered != current_key
            ):
                speak(
                    f"Reminder: {reminder['message']}"
                )

                reminders.remove(reminder)
                last_triggered = current_key

        time.sleep(10)


def start_reminder_checker():
    thread = threading.Thread(
        target=reminder_checker,
        daemon=True
    )

    thread.start()