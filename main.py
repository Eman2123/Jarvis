

# import os
# import eel
# from engine.reminder import start_reminder_checker
# from engine.features import *
# from engine.command import *
# from engine.login import (
#     create_user_table,
#     update_users_table,
#     login_user,
#     register_user,
#     check_email,
#     update_password
# )

# create_user_table()
# update_users_table()

# start_reminder_checker()

# eel.init("www")


# @eel.expose

# def userLogin(email, password):

#     if login_user(email, password):
#         return True

#     return False

# @eel.expose
# def userRegister(firstName, lastName, email, phone, password):

#     return register_user(
#         firstName,
#         lastName,
#         phone,
#         email,
#         password
#     )

# @eel.expose
# def checkEmail(email):

#     return check_email(email)

# @eel.expose
# def updatePassword(email, password):

#     return update_password(email, password)


# @eel.expose
# def init():
#     print("===== INIT CALLED =====")

#     try:
#         time.sleep(2)

#         print("Hide Loader")
#         eel.hideLoader()()

#         print("Hide Start")
#         eel.hideStart()()

#         print("Show Hood")
#         eel.ShowHood()()

#         print("INIT DONE")

#     except Exception as e:
#         print("INIT ERROR:", e)



# playAssistantSound()

# os.system('start msedge.exe --app="http://localhost:8000/login.html"')

# eel.start(
#     'login.html',
#     mode=None,
#     host='localhost',
#     port=8000,
#     block=True
# )
 




import os
import time
import threading
import eel
import json

from engine.chat_history import (
    create_chat_history_table,
    create_conversation,
    save_chat_message,
    get_all_conversations,
    get_conversation_messages,
    set_current_conversation
)


from engine.reminder import start_reminder_checker
from engine.features import *
from engine.command import *
from engine.login import (
    create_user_table,
    update_users_table,
    login_user,
    register_user,
    check_email,
    update_password
)

from engine.paths import resource_path, init_db

eel.init(resource_path("www"))


@eel.expose
def userLogin(email, password):
    return bool(login_user(email, password))


@eel.expose
def userRegister(firstName, lastName, email, phone, password):
    return register_user(firstName, lastName, phone, email, password)


@eel.expose
def checkEmail(email):
    return check_email(email)


@eel.expose
def updatePassword(email, password):
    return update_password(email, password)

# ================= CHAT HISTORY =================

current_conversation_id = None


@eel.expose
def newChat():
    global current_conversation_id

    current_conversation_id = create_conversation()
    set_current_conversation(current_conversation_id)

    return current_conversation_id


@eel.expose
def saveChatMessage(role, message):
    global current_conversation_id

    if not current_conversation_id:
        current_conversation_id = create_conversation()

    return save_chat_message(
        current_conversation_id,
        role,
        message
    )


@eel.expose
def getChatHistory():
    return json.dumps(
        get_all_conversations(),
        ensure_ascii=False
    )


@eel.expose
def loadChat(conversation_id):
    global current_conversation_id

    try:
        conversation_id = int(conversation_id)

        conversations = get_all_conversations()

        if not any(
            int(chat["id"]) == conversation_id
            for chat in conversations
        ):
            return json.dumps([])

        current_conversation_id = conversation_id
        set_current_conversation(conversation_id)

        messages = get_conversation_messages(
            conversation_id
        )

        return json.dumps(
            messages,
            ensure_ascii=False
        )

    except (TypeError, ValueError):
        return json.dumps([])





@eel.expose
def init():
    print("===== INIT CALLED =====")
    try:
        time.sleep(2)
        eel.hideLoader()()
        eel.hideStart()()
        eel.ShowHood()()
        print("INIT DONE")
    except Exception as e:
        print("INIT ERROR:", e)


#def open_browser():
 #   time.sleep(2)   # server ko tayyar hone ka time
  #  os.system('start msedge.exe --app="http://localhost:8000/login.html"')

import socket

def open_browser():
    # server tayyar hone tak intezar (max 30 sec)
    for _ in range(60):
        try:
            with socket.create_connection(("localhost", 8000), timeout=0.5):
                break
        except OSError:
            time.sleep(0.5)
    time.sleep(1)
    os.system('start msedge.exe --app="http://localhost:8000/login.html"')



#def start():
 #   create_user_table()
  #  update_users_table()
   # start_reminder_checker()
   # playAssistantSound()

   # threading.Thread(target=open_browser, daemon=True).start()

    #eel.start(
     #   'login.html',
      #  mode=None,
       # host='localhost',
       # port=8000,
       # block=True
    #)

    #eel.start(
    #'login.html',
    #mode=None,
    #host='localhost',
    #port=8000,
    #block=True,
    #shutdown_delay=15
#)

def start():
    init_db()
    create_user_table()
    update_users_table()

    # Chat History database table create karo
    create_chat_history_table()

    start_reminder_checker()
    playAssistantSound()

    threading.Thread(
        target=open_browser,
        daemon=True
    ).start()

    eel.start(
        'login.html',
        mode=None,
        host='localhost',
        port=8000,
        block=True,
        shutdown_delay=15
    )




if __name__ == '__main__':
    start()

