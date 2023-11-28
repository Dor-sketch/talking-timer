import time

# Define a function to run the chapter timer loop
def chapter_timer(chapter_num, tuple_args):
    # Unpack the arguments
    stop_flag, extra_essay, clock_ticking, remaining_time, five_min_warning, screen, print_lock = tuple_args
    # global delay_per_second

    if (extra_essay.is_set()):
        remaining_time = 1800
        extra_essay.clear()

    while remaining_time > 0 and not stop_flag.is_set():
        clock_ticking.wait()
        mins, secs = divmod(remaining_time, 60)
        timer_str = f"{mins:02d}:{secs:02d}"

        with print_lock:
            # Clear the line where the timer is displayed
            screen.move(4, 0)  # Adjust the position as needed
            screen.clrtoeol()
            # Display the timer
            # Adjust the position as needed
            screen.addstr(4, 0, f"Time remaining: {timer_str}")
            screen.refresh()

        remaining_time -= 1
        time.sleep(1)
