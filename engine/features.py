


import json
import os
import re
from shlex import quote
import sqlite3
import struct
import subprocess
import time
import webbrowser

from playsound  import playsound
import eel
import pyaudio
import pyautogui
from engine.command import speak
from engine.config import ASSISTANT_NAME, LLM_KEY

# playing assistant sound function
import  pywhatkit as kit
import pvporcupine

from engine.helper import extract_yt_term, markdown_to_text, remove_words


conn = sqlite3.connect("jarvis.db")
cursor = conn.cursor()


@eel.expose
def playAssistantSound():
    music_dir="www\\assets\\audio\\www_assets_audio_start_sound.mp3"
    playsound(music_dir)

def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()

    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")

       
def PlayYoutube(query):
   # search_term = extract_yt_term(query)
    search_term = query.replace("play", "").replace("on youtube", "").strip()

    kit.playonyt(search_term)
    
def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

# find contacts
# def findContact(query):
    
#     words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
#     vquery = remove_words(query, words_to_remove)

#     try:
#         query = query.strip().lower()
#         cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
#         results = cursor.fetchall()
#         print(results[0][0])
#         mobile_number_str = str(results[0][0])

#         if not mobile_number_str.startswith('+92'):
#             mobile_number_str = '+92' + mobile_number_str

#         return mobile_number_str, query
#     except:
#         speak('not exist in contacts')
#         return 0, 0

def findContact(query):
    import re

    try:
        # Remove command words and keep the contact name
        query = query.strip().lower()

        words_to_remove = [
            ASSISTANT_NAME, "send", "message", "to",
            "make", "a", "phone", "call", "whatsapp",
            "video", "please"
        ]

        contact_name = query

        for word in words_to_remove:
            contact_name = re.sub(
                r'\b' + re.escape(word) + r'\b',
                ' ',
                contact_name,
                flags=re.IGNORECASE
            )

        contact_name = " ".join(contact_name.split())

        print("DEBUG CONTACT NAME:", repr(contact_name))

        cursor.execute(
            "SELECT name, mobile_no FROM contacts WHERE LOWER(name) LIKE ?",
            ('%' + contact_name + '%',)
        )

        results = cursor.fetchall()

        if not results:
            print("DEBUG: Contact not found in database")
            speak("Contact not found in database")
            return 0, 0

        name = results[0][0]
        mobile_number = str(results[0][1]).strip()

        if not mobile_number.startswith("+"):
            if mobile_number.startswith("0"):
                mobile_number = "+92" + mobile_number[1:]
            else:
                mobile_number = "+92" + mobile_number

        print("DEBUG FOUND CONTACT:", name)
        print("DEBUG CONTACT NUMBER:", mobile_number)

        return mobile_number, name

    except Exception as e:
        print("CONTACT SEARCH ERROR:", e)
        speak("There was an error finding the contact")
        return 0, 0


















# def whatsApp(mobile_no, message, flag, name):
#     import subprocess, time, pyautogui
#     from urllib.parse import quote

#     if flag == 'message':
#         target_tab = 12
#         jarvis_message = "message sent successfully to " + name

#     elif flag == 'call':
#         target_tab = 7
#         message = ''
#         jarvis_message = "calling " + name

#     else:
#         target_tab = 6
#         message = ''
#         jarvis_message = "starting video call with " + name

#     encoded_message = quote(message)
#     whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"
#     full_command = f'start "" "{whatsapp_url}"'

#     subprocess.run(full_command, shell=True)
#     time.sleep(5)

#     if flag == 'video':
#         time.sleep(3)
#         pyautogui.click(x=1750, y=80)  # adjust these coords
#         speak("Video call started")
#         return

#     pyautogui.hotkey('ctrl', 'f')
#     for i in range(1, target_tab):
#         pyautogui.hotkey('tab')
#     pyautogui.hotkey('enter')
#     speak(jarvis_message)

def whatsApp(mobile_no, message, flag, name):
    import subprocess
    import time
    import webbrowser
    from urllib.parse import quote

    mobile_no = str(mobile_no).strip()
    mobile_no = mobile_no.replace("+", "").replace(" ", "")

    if not mobile_no.isdigit():
        speak("The contact phone number is invalid.")
        return

    if flag == "message":
        encoded_message = quote(str(message))
        whatsapp_url = (
            f"https://web.whatsapp.com/send"
            f"?phone={mobile_no}&text={encoded_message}"
        )

    elif flag in ("call", "video"):
        whatsapp_url = (
            f"https://web.whatsapp.com/send?phone={mobile_no}"
        )

    else:
        speak("Sorry, this WhatsApp command is not supported.")
        return

    try:
        # WhatsApp Web ko default browser mein open karo
        webbrowser.open(whatsapp_url)

        # Page load hone ke liye waqt do
        time.sleep(10)

        if flag == "message":
            speak(
                f"WhatsApp chat with {name} is open. "
                "Please check the message and send it."
            )

        elif flag == "call":
            speak(
                f"WhatsApp chat with {name} is open. "
                "Please start the voice call using WhatsApp."
            )

        elif flag == "video":
            speak(
                f"WhatsApp chat with {name} is open. "
                "Please start the video call using WhatsApp."
            )

    except Exception as e:
        print("WhatsApp Error:", e)
        speak("Sorry, WhatsApp could not be opened.")






    
# chat bot 

# Settings Modal 



# Assistant name
@eel.expose
def assistantName():
    name = ASSISTANT_NAME
    return name


@eel.expose
def personalInfo():
    try:
        cursor.execute("SELECT * FROM info")
        results = cursor.fetchall()
        jsonArr = json.dumps(results[0])
        eel.getData(jsonArr)
        return 1    
    except:
        print("no data")


@eel.expose
def updatePersonalInfo(name, designation, mobileno, email, city):
    cursor.execute("SELECT COUNT(*) FROM info")
    count = cursor.fetchone()[0]

    if count > 0:
        # Update existing record
        cursor.execute(
            '''UPDATE info 
               SET name=?, designation=?, mobileno=?, email=?, city=?''',
            (name, designation, mobileno, email, city)
        )
    else:
        # Insert new record if no data exists
        cursor.execute(
            '''INSERT INTO info (name, designation, mobileno, email, city) 
               VALUES (?, ?, ?, ?, ?)''',
            (name, designation, mobileno, email, city)
        )

    conn.commit()
    personalInfo()
    return 1



@eel.expose
def displaySysCommand():
    cursor.execute("SELECT * FROM sys_command")
    results = cursor.fetchall()
    jsonArr = json.dumps(results)
    eel.displaySysCommand(jsonArr)
    return 1


@eel.expose
def deleteSysCommand(id):
    cursor.execute("DELETE FROM sys_command WHERE id = ?", (id,))
    conn.commit()


@eel.expose
def addSysCommand(key, value):
    cursor.execute(
        '''INSERT INTO sys_command VALUES (?, ?, ?)''', (None,key, value))
    conn.commit()


@eel.expose
def displayWebCommand():
    cursor.execute("SELECT * FROM web_command")
    results = cursor.fetchall()
    jsonArr = json.dumps(results)
    eel.displayWebCommand(jsonArr)
    return 1


@eel.expose
def addWebCommand(key, value):
    cursor.execute(
        '''INSERT INTO web_command VALUES (?, ?, ?)''', (None, key, value))
    conn.commit()


@eel.expose
def deleteWebCommand(id):
    cursor.execute("DELETE FROM web_command WHERE Id = ?", (id,))
    conn.commit()


@eel.expose
def displayPhoneBookCommand():
    cursor.execute("SELECT * FROM contacts")
    results = cursor.fetchall()
    jsonArr = json.dumps(results)
    eel.displayPhoneBookCommand(jsonArr)
    return 1


@eel.expose
def deletePhoneBookCommand(id):
    cursor.execute("DELETE FROM contacts WHERE Id = ?", (id,))
    conn.commit()


@eel.expose
def InsertContacts(Name, MobileNo, Email, City):
    cursor.execute(
        '''INSERT INTO contacts VALUES (?, ?, ?, ?, ?)''', (None,Name, MobileNo, Email, City))
    conn.commit()





#from google import genai

#def geminai(query):
 #   try:
  #      query = query.replace(ASSISTANT_NAME, "")
   #     query = query.replace("search", "")
    #    client = genai.Client(api_key= LLM_KEY)
     #   model=genai.GenerativeModel("gemini-2.0-flash")
      #  respose= model.generate_content(query)
       # filter_text = markdown_to_text(respose.text)
        #speak(filter_text)
    #except Exception as e:
      #  print("Error:",e)

from groq import Groq

def geminai(query):
    try:
        query = query.replace(ASSISTANT_NAME, "")
        query = query.replace("search", "")
    
        client = Groq(api_key=LLM_KEY)

    


        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": "You are Jarvis, an intelligent AI desktop assistant. Reply naturally and helpfully."
                },
                {
                    "role": "user",
                    "content": query
                }
            ],
            temperature=0.7,
            max_tokens=1024
        )

        answer = response.choices[0].message.content

        filter_text = markdown_to_text(answer)

        print(filter_text)

        speak(filter_text)

    except Exception as e:
        print("Groq Error:", e)