from engine.chat_history import save_current_message
import re
from engine.reminder import add_reminder
import pyttsx3
import speech_recognition as sr
import eel
import time

from engine.system_control import control_system


# Speak function
def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    #engine.say(text)
    # Jarvis ka reply database mein save karo
    save_current_message("assistant", text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        eel.DisplayMessage('listening...')

        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=10, phrase_time_limit=6)

    try:
        print("Recognizing...")
        eel.DisplayMessage('Recognizing...')
        query = r.recognize_google(audio, language='en-PK')
        print(f"User said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)

    except Exception as e:
        print("Error:", e)
        return None

    return query.lower()



    

@eel.expose
def allCommands(message=1):

    try:
        # ============================
        # GET QUERY
        # ============================
        if message == 1:
            query = takecommand()
        else:
            query = message

        if not query or query.strip() == "":
            return

       # print("🟢 QUERY:", query)
       # eel.senderText(query)

        print("🟢 QUERY:", query)

        # User ka message database mein save karo
        save_current_message("user", query)

        eel.senderText(query)


        # ============================
        # SYSTEM CONTROL
        # ============================
        result = control_system(query)
        if result:
            speak(result)
            return


                # ============================
        # REMINDER
        # ============================

        if "remind me at" in query:

            try:
                match = re.search(
                    r"remind me at (\d{1,2})(?::(\d{2}))?\s*(am|pm)?\s+to\s+(.+)",
                    query,
                    re.IGNORECASE
                )

                if not match:
                    speak("Please say the reminder like: Remind me at 5 PM to call Ayaan.")
                    return

                hour = int(match.group(1))
                minute = int(match.group(2) or 0)
                am_pm = match.group(3)
                reminder_message = match.group(4).strip()

                if am_pm:
                    am_pm = am_pm.lower()

                    if am_pm == "pm" and hour != 12:
                        hour += 12

                    elif am_pm == "am" and hour == 12:
                        hour = 0

                if hour > 23 or minute > 59:
                    speak("Invalid reminder time.")
                    return

                result = add_reminder(
                    hour,
                    minute,
                    reminder_message
                )

                speak(result)
                return

            except Exception as e:
                print("❌ REMINDER ERROR:", e)
                speak("Unable to set reminder.")
                return






        # ============================
        # COMMAND ROUTING
        # ============================

        query = str(query).strip().lower()
        print("DEBUG QUERY:", repr(query))

        if "open" in query:
            from engine.features import openCommand
            openCommand(query)

        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)

        elif "send message" in query or "phone call" in query or "video call" in query:
            print("DEBUG: WhatsApp command detected")
            from engine.features import findContact, whatsApp

            contact_no, name = findContact(query)
            if contact_no == 0:
                speak("Contact not found")
                return

            if "send message" in query:
                speak("What message to send?")
                msg = takecommand()
                whatsApp(contact_no, msg, 'message', name)

            elif "phone call" in query:
                whatsApp(contact_no, '', 'call', name)

            else:
                whatsApp(contact_no, '', 'video', name)

        else:
            # ============================
            # 🔥 FALLBACK TO GEMINI
            # ============================
            from engine.features import geminai
            geminai(query)

    except Exception as e:
        print("❌ ERROR OCCURRED:", e)
        speak("Sorry, something went wrong.")

    eel.ShowHood()
   