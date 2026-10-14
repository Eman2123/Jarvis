import os
import psutil
import datetime
import subprocess
import time
import threading
from playsound import playsound

from pycaw.pycaw import AudioUtilities







#battery_alarm_triggered = False     # Prevents repeating alarm
#custom_alarm_triggered = False      # Single alarm system


#def auto_battery_alarm():
 #   global battery_alarm_triggered

  #  while True:
   #     battery = psutil.sensors_battery()
#    if battery:
 #           percent = battery.percent
  #          plugged = battery.power_plugged

            # LOW BATTERY ALARM (only once)
   #         if percent <= 20 and not plugged and not battery_alarm_triggered:
    #            battery_alarm_triggered = True
     #           playsound("low_battery_alarm.mp3")     # Put your alarm file here
      #          print("🔴 Low battery alarm triggered!")

            # Reset alarm if charge goes above 40%
       #     if percent > 40:
        #        battery_alarm_triggered = False

       # time.sleep(15)   # check every 15 seconds


#def single_custom_alarm(alarm_time):
 #   global custom_alarm_triggered
#
 #   while True:
  #      now = datetime.datetime.now().strftime("%H:%M")

   #     if now == alarm_time and not custom_alarm_triggered:
    #        custom_alarm_triggered = True
     #       playsound("alarm.mp3")
 #           print("⏰ Alarm ringing!")
#
  #      time.sleep(1)

def control_system(query):
    query = query.lower()

    # Shutdown
    if "shutdown" in query:
        os.system("shutdown /s /t 1")
        return "Shutting down your laptop"

    # Restart
    elif "restart" in query:
        os.system("shutdown /r /t 1")
        return "Restarting your laptop"

    # Sleep
    elif "sleep" in query:
        os.system("rundll32.exe powrprof.dll,SetSuspendState Sleep")
        return "Putting laptop to sleep"

    # Lock
    elif "lock" in query:
        os.system("rundll32.exe user32.dll,LockWorkStation")
        return "Locking your laptop"

        # Volume Up
    elif "volume up" in query:
        devices = AudioUtilities.GetSpeakers()
        volume = devices.EndpointVolume

        current_volume = volume.GetMasterVolumeLevelScalar()
        new_volume = min(1.0, current_volume + 0.10)
        volume.SetMasterVolumeLevelScalar(new_volume, None)

        return "Increasing volume"

    # Volume Down
    elif "volume down" in query:
        devices = AudioUtilities.GetSpeakers()
        volume = devices.EndpointVolume

        current_volume = volume.GetMasterVolumeLevelScalar()
        new_volume = max(0.0, current_volume - 0.10)
        volume.SetMasterVolumeLevelScalar(new_volume, None)

        return "Decreasing volume"
       
          


    # Brightness
    elif "brightness" in query:
        import screen_brightness_control as sbc
        try:
            value = int([x for x in query.split() if x.isdigit()][0])
            sbc.set_brightness(value)
            return f"Brightness set to {value}%"
        except:
            return "Unable to set brightness"

    # Battery Status
    elif "battery" in query:
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            charging = "Charging" if battery.power_plugged else "Not Charging"
            return f"Battery is {percent} percent, {charging}."
        return "Battery information not available."

    # Battery Alarm
    elif "battery alarm" in query or "battery alert" in query:
        battery = psutil.sensors_battery()
        if battery.percent <= 20:
            return "Warning! Battery is below 20 percent."
        elif battery.percent == 100:
            return "Battery is fully charged."
        return "Battery level is normal."

    # Uptime
    elif "uptime" in query or "running time" in query:
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        now = datetime.datetime.now()
        uptime = now - boot_time
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        return f"Laptop running for {uptime.days} days, {hours} hours and {minutes} minutes."

    # Current Time
    elif "time" in query or "clock" in query:
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {now}."


        # WiFi Off
    elif "wifi off" in query or "wifi disable" in query:
        os.system('powershell -Command "Start-Process netsh -ArgumentList \'interface set interface Wi-Fi admin=disabled\' -Verb RunAs"')
        return "Turning WiFi off."

        # WiFi On
    elif "wifi on" in query or "wifi enable" in query:
       os.system('powershell -Command "Start-Process netsh -ArgumentList \'interface set interface Wi-Fi admin=enabled\' -Verb RunAs"')
       return "Turning WiFi on."


       # Bluetooth On
    elif "bluetooth on" in query or "bluetooth enable" in query:
      os.system('powershell -Command "Start-Process powershell -ArgumentList \'-Command Start-Service bthserv\' -Verb RunAs"')
      return "Turning Bluetooth on."
    


     # Bluetooth Off
    elif "bluetooth off" in query or "bluetooth disable" in query:
     os.system('powershell -Command "Start-Process powershell -ArgumentList \'-Command Stop-Service bthserv\' -Verb RunAs"')
     return "Turning Bluetooth off."

    

    # CPU Usage
    #elif "cpu usage" in query:
   #     return f"CPU is at {psutil.cpu_percent()} percent."

    # RAM Usage
    elif "ram" in query or "memory" in query:
        ram = psutil.virtual_memory()
        return f"RAM used: {ram.percent} percent."

    

    

    # Internet Status
    elif "internet" in query or "network" in query:
        try:
            subprocess.check_output("ping google.com -n 1")
            return "Internet is connected."
        except:
            return "No internet connection."

    # System Report
    #elif "system report" in query or "full report" in query:
     #cpu = psutil.cpu_percent()
    #ram = psutil.virtual_memory().percent

   # battery = psutil.sensors_battery()

   # if battery is not None:
    #    battery_percent = battery.percent
     #   battery_status = f"{battery_percent} percent"
   # else:
    #    battery_status = "Not available"

   # return f"System status: CPU {cpu} percent, RAM {ram} percent, Battery {battery_status}."


    