"""
A module to handle input and output to the screen.
"""
import atexit
import threading
import curses
import time

print_lock = threading.Lock()
screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)
last_input_time = time.time()

def cleanup_lock():
    """
    Clean-up function for the print lock.
    """
    global print_lock
    print_lock = None


def cleanup_curses():
    """
    Clean-up function for curses.
    """
    screen.keypad(False)
    curses.nocbreak()
    curses.echo()
    curses.endwin()


# Register clean-up functions to be executed when program exits
atexit.register(cleanup_lock)
atexit.register(cleanup_curses)


def wait_for_key(stop_flag=None, timeout=50) -> str:
    """
    A function to wait for user input.

    :param stop_flag: A threading.Event object to stop the function.
    :param timeout: The timeout value for the screen.getch() function.
    """
    global last_input_time
    screen.timeout(timeout)  # Set the timeout value
    while True:
        if stop_flag is not None and stop_flag.is_set():
            return -1  # Return -1 to indicate that the function was stopped
        char = screen.getch()
        if char == -1:
            # No input detected
            current_time = time.time()
            if current_time - last_input_time > 60:
                time.sleep(10)
                last_input_time = current_time
            if current_time - last_input_time > 30:  # Wait for 5 seconds of no input
                time.sleep(5)  # Add a delay of 1 second
                last_input_time = current_time
            else:
                time.sleep(1)  # Add a delay of 0.1 seconds
        else:
            last_input_time = time.time()
            return chr(char)



def output_util(current_chapter, tuple_args) -> None:
    """
    A function to handle output to the screen.

    :param current_chapter: The current chapter number.
    :param tuple_args: A tuple of arguments.
    """
    stop_flag, exit_flag, output_event, synthesizer, clock_ticking, chapters = tuple_args
    with print_lock:
        screen.clear()  # Clear the screen

        # Example of adding text to the screen
        screen.addstr(0, 0, "TEST STARTED")
        screen.addstr(
            1, 0, "Press 'P' to pause, 'R' to resume, 'N' for next chapter, 'Q' to quit.")
        screen.addstr(2, 0, f"Current Chapter: {current_chapter + 1}")
        chapter_str = ""
        for temp in range(chapters):
            if temp == current_chapter:
                chapter_str += "[*] "
            else:
                chapter_str += "[ ] "

        screen.addstr(3, 0, chapter_str)  # Adjust 3, 0 to the desired position

        screen.refresh()  # Refresh the screen to update the display

    while True and not exit_flag.is_set():
        output_event.wait()
        if exit_flag.is_set():
            synthesizer.speak_text_async("Quitting!")
            # Clean up the curses screen
            curses.nocbreak()
            screen.keypad(False)
            curses.echo()
            curses.endwin()
            break
        elif stop_flag.is_set():
            synthesizer.speak_text_async("Time is up! Please turn pages!")
            break
        elif clock_ticking.is_set() is False:
            # Put other threads to sleep until the pause flag is cleared
            synthesizer.speak_text_async("Paused!")
            clock_ticking.wait()
            synthesizer.speak_text_async("Resumed!")



def input_util(tuple_args) -> None:
    """
    A function to handle input from the user.

    :param tuple_args: A tuple of arguments.
    """

    stop_flag, exit_flag, output_event, clock_ticking = tuple_args
    while True and not stop_flag.is_set():
        key = wait_for_key(stop_flag=stop_flag)
        output_event.set()
        if key == ("n"):  # Check if the user has pressed the "n" key
            stop_flag.set()  # Set the stop flag to stop the chapter timer thread
            break
        elif key == ("q"):  # Check if the user has pressed the "q" key to quit the program
            stop_flag.set()  # Set the stop flag to stop the chapter timer thread
            exit_flag.set()
            quit()
        elif key == ("p"):  # Check if the user has pressed the "p" key to pause the timer
            clock_ticking.clear()  # Set the pause event to pause the timer
            while wait_for_key() == -1:  # Wait for the user to press a key
                pass
            clock_ticking.set()  # Clear the pause event to resume the timer
