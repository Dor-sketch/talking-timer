import time
import curses
import threading

print_lock = threading.Lock() # Create a lock for synchronizing access to the standard output stream
screen = curses.initscr() # Initialize the curses screen
curses.resizeterm(0, 0) # Turn on automatic window resizing
curses.noecho() # turn off auto echoing of keypress on to screen
curses.cbreak() # turn off input buffering (so keypresses are passed to the app without waiting for enter to be pressed)
screen.keypad(True) # enable special Key values such as curses.KEY_LEFT etc - allow arrow keys to be processed
last_input_time = time.time()

def wait_for_key(stop_flag=None, timeout=50):
    global last_input_time
    screen.timeout(timeout)  # Set the timeout value
    while True:
        if stop_flag is not None and stop_flag.is_set():
            return -1  # Return -1 to indicate that the function was stopped
        char = screen.getch()
        if char == -1:
            # No input detected
            current_time = time.time()
            if current_time - last_input_time > 5:  # Wait for 5 seconds of no input
                time.sleep(1)  # Add a delay of 1 second
                last_input_time = current_time
            else:
                time.sleep(0.1)  # Add a delay of 0.1 seconds
        else:
            last_input_time = time.time()
            return chr(char)

# Define a function to handle output
def output_util(current_chapter, tuple_args):
    stop_flag, exit_flag, output_event, synthesizer, clock_ticking, chapters = tuple_args
    with print_lock:
        print("\033[2J\033[H")         # Clear the screen before printing
        test_str = "TEST STARTED"
        num_equals = (curses.COLS - len(test_str)) // 2
        equals_str = "=" * num_equals
        print(f"\033[F{equals_str}{test_str}{equals_str}")
        print("\033[F")
        print("Press \"P\" to pause the timer, and \"R\" to resume the timer.")
        print("\033[F")
        print("Press \"N\" to skip to next chapter.")
        print("\033[F")
        print("Press \"Q\" to quit the program.")
        print("\033[F")
        print("\nCurrent location: ", end="")
        for temp in range(chapters):
            if temp == current_chapter:
                print("[*]", end="")
            else:
                print("[ ]", end="")
        print("\n")
        print(f"\033[F\nChapter {current_chapter+1}")
        print("\033[F\n\n")

    while True and not exit_flag.is_set():
        output_event.wait()
        if (exit_flag.is_set()):
            synthesizer.speak_text_async("Quitting!")
            # Clean up the curses screen
            curses.nocbreak()
            screen.keypad(False)
            curses.echo()
            curses.endwin()
            break
        elif (stop_flag.is_set()):
            synthesizer.speak_text_async("Time is up! Please turn pages!")
            break
        elif clock_ticking.is_set() == False:
        # Put other threads to sleep until the pause flag is cleared
            synthesizer.speak_text_async("Paused!")
            clock_ticking.wait()
            synthesizer.speak_text_async("Resumed!")

# Define a function to handle user input
def input_util(tuple_args):
    stop_flag, exit_flag, output_event, clock_ticking = tuple_args
    while True and not stop_flag.is_set():
        key = wait_for_key(stop_flag=stop_flag)
        output_event.set()
        if (key == ("n")):  # Check if the user has pressed the "n" key
            stop_flag.set()  # Set the stop flag to stop the chapter timer thread
            break
        elif (key == ("q")):  # Check if the user has pressed the "q" key to quit the program
            stop_flag.set()  # Set the stop flag to stop the chapter timer thread
            exit_flag.set()
            quit()
        elif (key == ("p")):  # Check if the user has pressed the "p" key to pause the timer
            clock_ticking.clear()  # Set the pause event to pause the timer
            while wait_for_key() == -1:  # Wait for the user to press a key
                pass
            clock_ticking.set()  # Clear the pause event to resume the timer
