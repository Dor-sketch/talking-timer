"""
A module for the timer functionality.
"""
import time


def chapter_timer(tuple_args):
    """
    A function to keep track of the time for each chapter.
    """
    # Unpack the arguments
    stop_flag, extra_essay, clock_ticking, remaining_time, five_min_warning, \
    screen, print_lock, synthesizer = tuple_args

    # Check if extra essay time is needed
    if extra_essay.is_set():
        remaining_time = 1800  # Reset time for extra essay
        extra_essay.clear()

    # First loop: Run until there are 5 minutes left
    while remaining_time > 300 and not stop_flag.is_set():
        clock_ticking.wait()
        update_timer_display(remaining_time, screen, print_lock)
        remaining_time -= 1
        time.sleep(1)

    # Trigger the 5-minute warning
    if not stop_flag.is_set():
        synthesizer.speak_text_async("5 minutes remaining!")

    # Second loop: Last 5 minutes countdown
    while remaining_time > 0 and not stop_flag.is_set():
        clock_ticking.wait()
        update_timer_display(remaining_time, screen, print_lock)
        remaining_time -= 1
        time.sleep(1)

    # Time is up - update signals
    clock_ticking.clear()
    stop_flag.set()


def update_timer_display(remaining_time, screen, print_lock):
    """
    Updates the timer display on the screen.
    """
    mins, secs = divmod(remaining_time, 60)
    timer_str = f"{mins:02d}:{secs:02d}"
    with print_lock:
        screen.move(4, 0)
        screen.clrtoeol()
        screen.addstr(4, 0, f"Time remaining: {timer_str}")
        screen.refresh()
