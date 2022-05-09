import time
import csv
from pynput import keyboard 
from pynput.keyboard import Key
import statistics

keyPresses=dict()
keyReleases=dict()
downUpTime=dict()
holdTime=list()
downDownTime=list()
upDownTime=list()
columns_name = ["session","H.time", "DD.time", "UD.time", "H.avg", "DD.avg", "UD.avg", "H.med", "DD.med", "UD.med"]
session_counter = 0
time_last_key_pressed = None
time_key_pressed = None
time_key_released = None
max_time_limit_between_presses = 15000

def on_key_release(key): #what to do on key-release
    global time_key_released
    time_key_released = time_in_millis()
    if key in keyPresses:
        time_taken = round(time_in_millis() - keyPresses[key], 2) #rounding the long decimal float
        downUpTime[key] = time_taken
        holdTime.append(time_taken)
        print("H time for key: ", key, "is: ", time_taken, " miliseconds")
    if key == Key.f9:
        return False #stop detecting more key-releases
    

def on_key_press(key): #what to do on key-press
    global time_key_pressed
    global time_last_key_pressed

    if key == Key.f10:
        global session_counter
        session_counter += 1
        summarise()

    time_key_pressed = time_in_millis()
    if time_last_key_pressed is not None:
        dd_time =  time_key_pressed - time_last_key_pressed
        if dd_time >= max_time_limit_between_presses:
            pass
        else:
            print("DD time",dd_time, "miliseconds")
            downDownTime.append(dd_time)

    keyPresses[key] = time_key_pressed
    if time_key_released is not None:
        ud_time = time_in_millis() - time_key_released
        if ud_time >= max_time_limit_between_presses:
            pass
        else:
            print("UD time: ", ud_time, " miliseconds")
            upDownTime.append(ud_time)

    if key == Key.f9:
        return False #stop detecting more key-presses
    time_last_key_pressed = time_key_pressed

def average(lst: list) -> float:
    return sum(lst) / len(lst)

def summarise():
    data_rows = zip([[session_counter],
     holdTime, downDownTime, upDownTime, # raw data
    [average(holdTime)], [average(downDownTime)], [average(upDownTime)], # average
    [statistics.median(holdTime)], [statistics.median(downDownTime)], [statistics.median(upDownTime)]]) # median value
    with open('summary_session_' + str(session_counter) + '.csv', 'w') as f: 
        write = csv.writer(f) 
        write.writerow(columns_name) 
        for row in data_rows:
            for item in row:
                write.writerow(item)
    keyPresses.clear()
    keyReleases.clear()
    downUpTime.clear()
    holdTime.clear()
    downDownTime.clear()
    upDownTime.clear()
    global time_last_key_pressed
    global time_key_pressed
    global time_key_released
    time_last_key_pressed = None
    time_key_pressed = None
    time_key_released = None      

def time_in_millis() -> int:
    return round(time.time() * 1000)

with keyboard.Listener(
        on_press=on_key_press,
        on_release=on_key_release) as listener:
    listener.join()

# with keyboard.Listener(on_press = on_key_press) as press_listener: #setting code for listening key-press
#     press_listener.join()

# with keyboard.Listener(on_release = on_key_release) as release_listener: #setting code for listening key-release
#     release_listener.join()