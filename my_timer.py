import time

# Define a function to run the chapter timer loop
def chapter_timer(chapter_num, stop_flag, extra_essay, clock_ticking, remaining_time=1200, five_min_warning=300):
    # global delay_per_second
    
    if (extra_essay.is_set()):
        remaining_time = 1800
        extra_essay.clear()
    
    start_time = time.time()  # Get the current time
    saved_remaining_time = remaining_time
    estimated_end_time = start_time + remaining_time  # Calculate the estimated end time
    # timeout = max(0, min((1-delay_per_second), 1)) 
    timeout = 1 - 0.00333

    # with open("output.txt", "a") as f:
    #     print(f"Chapter {chapter_num} ", file=f) 

    while remaining_time > five_min_warning and not stop_flag.is_set():
        clock_ticking.wait()
        mins, secs = divmod(remaining_time, 60)  
        timer_str = f"{mins:02d}:{secs:02d} " 
        print(f"Time remaining: {timer_str}", end="\r") 
        remaining_time -= 1  # Decrement the remaining time by 1 second
        time.sleep(timeout)  # Wait for the timeout value

    # if stop_flag.is_set() == False:
    #     synthesizer.speak_text_async("Five minutes remaining!")

    while remaining_time > 0 and not stop_flag.is_set():
        clock_ticking.wait()
        mins, secs = divmod(remaining_time, 60)  
        timer_str = f"{mins:02d}:{secs:02d} " 
        print(f"Time remaining: {timer_str}", end="\r") 
        remaining_time -= 1  # Decrement the remaining time by 1 second
        time.sleep(timeout)  # Wait for the timeout value

    if (remaining_time == 0):
        stop_flag.set()
        output_event.set()
        # with open("output.txt", "a") as f:
        #     delay = time.time() - estimated_end_time    # Calculate the delay
        #     print(f"Chapter {chapter_num} delay was: {delay}\n", file=f)
        # delay = delay / float(saved_remaining_time) 
        # delay_per_second = (delay_per_second + delay) / 2.00000
