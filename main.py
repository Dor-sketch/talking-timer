import threading
import my_timer
import my_setup
import io_util

stop_flag = threading.Event()
clock_ticking = threading.Event()
output_event = threading.Event()
exit_flag = threading.Event()
extra_essay = threading.Event()
print_lock = threading.Lock() # Create a lock for synchronizing access to the standard output stream

# Define the main function
if __name__ == "__main__":
    my_setup.synthesizer = my_setup.speak_text()
    chapters = my_setup.get_chapters(extra_essay)  # Get the number of chapters from the user
    for i in range(chapters):
        # Start the chapter timer loop in a separate thread
        stop_flag.clear()  # Clear the stop flag to start the chapter timer thread
        output_event.clear()
        timer_thread = threading.Thread(target=my_timer.chapter_timer, args=(i+1,stop_flag, extra_essay, clock_ticking))
        output_thread = threading.Thread(target=io_util.output_util, args=(stop_flag, exit_flag, output_event, my_setup.synthesizer, clock_ticking, i, chapters))
        input_thread = threading.Thread(target=io_util.input_util, args=(stop_flag, exit_flag,output_event, clock_ticking))
        clock_ticking.set()
        timer_thread.start()
        output_thread.start()
        input_thread.start()
        # Wait for the chapter timer thread to finish
        timer_thread.join()
        output_thread.join()
        input_thread.join()
        if exit_flag.is_set():
            break
quit()
