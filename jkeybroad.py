import pyautogui
import speech_recognition as sr

# Function to type text
def type_text(text):
    pyautogui.typewrite(text)

# Function to simulate pressing a key
def press_key(key):
    pyautogui.press(key)

# Function to simulate a key combination (e.g., Ctrl+C)
def press_key_combination(key1, key2):
    pyautogui.hotkey(key1, key2)

def listen_for_commands():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)
        return command
    except sr.UnknownValueError:
        print("Could not understand audio.")
    except sr.RequestError as e:
        print("Error occurred while accessing the Google Speech Recognition service: {0}".format(e))

    return None

# Modes
TYPE_MODE = "type mode"
KEY_MODE = "key mode"
current_mode = TYPE_MODE  # Start with type mode by default

# Example usage
print("Welcome to the Voice Command Keyboard Automation!")
print("Available modes: 'type mode' and 'key mode'")
print("Say 'change mode' to switch between the modes.")
print("Say 'quit' to exit the program.")
print()

while True:
    command = listen_for_commands()

    if command is not None:
        if command == "change mode":
            if current_mode == TYPE_MODE:
                current_mode = KEY_MODE
                print("Switched to key mode.")
            else:
                current_mode = TYPE_MODE
                print("Switched to type mode.")
        elif command == "quit":
            print("Exiting...")
            break
        else:
            if current_mode == TYPE_MODE:
                type_text(command)
            elif current_mode == KEY_MODE:
                # Check for key combinations like Ctrl+R, Shift+A, etc.
                if "+" in command:
                    keys = command.split("+")
                    if len(keys) == 2 and keys[0] in pyautogui.KEYBOARD_KEYS and keys[1] in pyautogui.KEYBOARD_KEYS:
                        press_key_combination(keys[0], keys[1])
                    else:
                        print("Invalid key combination. Please say a valid key combination.")
                elif command in pyautogui.KEYBOARD_KEYS:
                    press_key(command)
                else:
                    print(f"Invalid key: {command}. Please say a valid key or key combination.")
