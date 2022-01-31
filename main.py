import database.display_util as display
import database.db as db
import utilities.timer as timer
import fileOperations.read as reader
import threading
import fileOperations.takeQuiz as takeQuiz
from pynput import keyboard

current = set()
# The key combination to check
COMBINATIONS = [
    {keyboard.Key.alt, keyboard.Key.ctrl,keyboard.KeyCode(char='e')}
]

def on_press(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            db.exportMarksToCsv()

def on_release(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.remove(key)

def hotkeys_export():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

export_thread = threading.Thread(target=hotkeys_export)
export_thread.start()

display.main_account_screen()


'''
tesing account:

username : JS123456
password : password123

username : JS123123
password : zaq1zaq1

'''

