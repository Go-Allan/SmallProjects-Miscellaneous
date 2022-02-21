''' Morse Code Translator:
    Translates inputted phrases into morse code.
    I want to be able to implement the following:
        -choose whether audio or visual translation
        -replay audio translation
        -enter morse code in ./- or also by tapping patterns
        -implement numbers and punctuation
        -idk something else...
        -make an actual interface?
        -speed of playback?
        -generate a random text phase and play it as audio then
         see if the user can translate it to text appropriately
        -make the speed scalable for mode 1
'''

# import sound library and define relevant constants
import winsound
import time
from pynput import keyboard

freq = 1000 # frequency of tone
dot_dur = 110  # dot duration (standard 100)
dash_dur = 375  # dash duration (standard 300)
no_sound = 37
space_dur = 0.075 # default 0.1
sleep_time = 1.0 # default 0.5

# Dot, Dash, and Wait Functions


def dot():
    winsound.Beep(freq, dot_dur)


def dash():
    winsound.Beep(freq, dash_dur)


def space():
    time.sleep(space_dur)


def wait():
    time.sleep(sleep_time)

# Mode Selection


def mode_selection():
    mode = input("\nSELECT MODE:\nText -> Morse: 0\nMorse -> to Text: 1"
                 "\nMorse Tapping Pattern Keyboard Input: 2\nQuit: Q\nEnter Here: ")
    n = "1"

    while n not in "0":
        if mode in "0":
            mode_0()
        elif mode in "1":
            mode_1()
        elif mode in "2":
            mode_2()
        elif mode in "Qq":
            exit()
        else:
            print("\nError: Invalid Entry\n")
            mode = input("SELECT MODE:\nText -> Morse: 0\nMorse -> to Text: 1"
                         "\nMorse Tapping Pattern Keyboard Input: 2\nEnter Here: ")

# Functions


def audio(store):
    for letter in store:
        if letter in ".":
            thing = dot(), space()
        elif letter in "-":
            thing = dash(),
        elif letter in " ":
            thing = wait(), space()
        else:
            print("error")
        time.sleep(0.05)
        output = thing
    return output


def translate_to_morse(phrase):  # this is defining a function named translate which takes one parameter called phrase
    store = ""
    for letter in phrase:
        if letter in "Aa":
            translation = ".-"
        elif letter in "Bb":
            translation = "-..."
        elif letter in "Cc":
            translation = "-.-."
        elif letter in "Dd":
            translation = "-.."
        elif letter in "Ee":
            translation = "."
        elif letter in "Ff":
            translation = "..-."
        elif letter in "Gg":
            translation = "--."
        elif letter in "Hh":
            translation = "...."
        elif letter in "Ii":
            translation = ".."
        elif letter in "Jj":
            translation = ".---"
        elif letter in "Kk":
            translation = "-.-"
        elif letter in "Ll":
            translation = ".-.."
        elif letter in "Mm":
            translation = "--"
        elif letter in "Nn":
            translation = "-."
        elif letter in "Oo":
            translation = "---"
        elif letter in "Pp":
            translation = ".--."
        elif letter in "Qq":
            translation = "--.-"
        elif letter in "Rr":
            translation = ".-."
        elif letter in "Ss":
            translation = "..."
        elif letter in "Tt":
            translation = "-"
        elif letter in "Uu":
            translation = "..-"
        elif letter in "Vv":
            translation = "...-"
        elif letter in "Ww":
            translation = ".--"
        elif letter in "Xx":
            translation = "-..-"
        elif letter in "Yy":
            translation = "-.--"
        elif letter in "Zz":
            translation = "--.."
        else:
            translation = " "

        store = store + translation + " "
    print(store)
    return store


def translate_to_text(string):  # this is defining a function named translate which takes one parameter called phrase
    store = ""
    x = string.split(" ")  # Break the entered string into individual words

    for word in x:
        if word == ".-":
            text = "a"
        elif word == "-...":
            text = "b"
        elif word == "-.-.":
            text = "c"
        elif word == "-..":
            text = "d"
        elif word == ".":
            text = "e"
        elif word == "..-.":
            text = "f"
        elif word == "--.":
            text = "g"
        elif word == "....":
            text = "h"
        elif word == "..":
            text = "i"
        elif word == ".---":
            text = "j"
        elif word == "-.-":
            text = "k"
        elif word == ".-..":
            text = "l"
        elif word == "--":
            text = "m"
        elif word == "-.":
            text = "n"
        elif word == "---":
            text = "o"
        elif word == ".--.":
            text = "p"
        elif word == "--.-":
            text = "q"
        elif word == ".-.":
            text = "r"
        elif word == "...":
            text = "s"
        elif word == "-":
            text = "t"
        elif word == "..-":
            text = "u"
        elif word == "...-":
            text = "v"
        elif word == ".--":
            text = "w"
        elif word == "-..-":
            text = "x"
        elif word == "-.--":
            text = "y"
        elif word == "--..":
            text = "z"
        elif word == "":
            text = " "
        else:
            text = "???"


        store = store + text

    print("Translation: " + store)

#        print(x)
# ----------------------------------------------------------------------------------------------------------------------

# Main Loop Mode 0


def mode_0():
    i = "1"

    while i in "1":
        n = "1"
        input_phrase = input("\nPlease enter a phrase: ")
        while n not in "0":
            audio(translate_to_morse(input_phrase))
            n = input("Press 1 to play same phrase again,\nelse press 0 to continue:")

        i = input("\nAnother Phrase? (Yes: 1, Mode Select: 2, Quit Program: 0): ")
    # Checks common to all three modes:
        while i not in "012":
            i = input("Error: Please enter 0, 1, or 2: ")

    else:
        if i in "0":
            exit()
        else:  # if this line runs, i == 2 so continue to choose mode below
            mode_selection()

# Main Loop Mode 1


def mode_1():
    i = "1"

    while i in "1":
        to_translate = input("\nPlease enter morse code using '.' and '-' with"
                             "\na single space between letters and two spaces"
                             "\nbetween words below:\n")
        translate_to_text(to_translate)

        i = input("\nAnother Phrase? (Yes: 1, Mode Select: 2, Quit Program: 0): ")
    # Checks common to all three modes
        while i not in "012":
            i = input("Error: Please enter 0, 1, or 2: ")

    else:
        if i in "0":
            exit()
        else:  # if this line runs, i == 2 so continue to choose mode below
            mode_selection()

# Main Loop Mode 2


def mode_2():
    n = "1"

    print("Please tap a phrase in morse code on any key:\n")
    print("(input ends after a pause of 5 seconds of no key press")

    while n in "1":

        def callb(key):  # what to do on key-release

            ti1 = str(time.time() - t)[0:5]  # converting float to str, slicing the float
#            start = time.time()
            print("\nThe key", key, " is pressed for", ti1, 'seconds')
#            int(ti1)
#            if (ti1 < 0.150) and (ti1 > 0.050):
#                pattern = pattern + "."
#            elif (ti1 > 0.280) and (ti1 < 0.450):
#                pattern = pattern + "-"
            return False #and start  # stop detecting more key-releases

        def callb1(key):  # what to do on key-press
#            end = time.time()
#            pause = str(end-start)
#            print("The time between key pressess was", pause)
            return False  # stop detecting more key-presses

        with keyboard.Listener(on_press=callb1) as listener1:  # setting code for listening key-press
            listener1.join()

        t = time.time()  # reading time in sec

        with keyboard.Listener(on_release=callb) as listener:  # setting code for listening key-release
            listener.join()

        # convert key press to either dot or dash or space and then store in pattern
        # translate the phrase to english text
        # if there is a gap of five seconds or greater ask if user wishes to
        # enter another phrase or go to mode selection
        # figure out how to measure the time between key release and the next key press in order to
        # determine gaps between letters and words

    mode_selection()

# Program Actually Starts Running Here:


print("\nWELCOME!")
mode_selection()
