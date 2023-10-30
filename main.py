import threading
from typing import Tuple, Any
import my_timer
from my_setup import SetupManager
import io_util

five_min: int = 300
twenty_min: int = 1200

class ThreadManager:
    """
    Manages multiple threads for the application.
    """
    def __init__(self, synthesizer=None, chapters: int = 8, extra_essay: bool = False):
        self.initialize_events()
        self.warning_time = five_min
        self.remaining_time = twenty_min
        self.synthesizer = synthesizer
        self.chapters = chapters
        if extra_essay:
            self.extra_essay.set()

    def get_timer_args(self) -> Tuple[Any, ...]:
        """
        Returns the arguments needed for the timer thread.
        """
        return self.stop_flag, self.extra_essay, self.clock_ticking, self.remaining_time, self.warning_time

    def get_output_args(self) -> Tuple[Any, ...]:
        """
        Returns the arguments needed for the output thread.
        """
        return self.stop_flag, self.exit_flag, self.output_event, self.synthesizer, self.clock_ticking, self.chapters

    def get_input_args(self) -> Tuple[Tuple[Any, ...],]:
        """
        Returns the arguments needed for the input thread.
        """
        return (self.stop_flag, self.exit_flag, self.output_event, self.clock_ticking),

    def initialize_events(self):
        """
        Initializes threading events.
        """
        self.stop_flag = threading.Event()
        self.clock_ticking = threading.Event()
        self.output_event = threading.Event()
        self.exit_flag = threading.Event()
        self.extra_essay = threading.Event()

    def run_threads(self, i: int):
        """
        Starts and joins the threads.
        """
        self.stop_flag.clear()
        self.clock_ticking.set()
        self.timer_thread = threading.Thread(target=my_timer.chapter_timer, args=(i + 1, self.get_timer_args()))
        self.output_thread = threading.Thread(target=io_util.output_util, args=(i, self.get_output_args()))
        self.input_thread = threading.Thread(target=io_util.input_util, args=self.get_input_args())

        self.timer_thread.start()
        self.output_thread.start()
        self.input_thread.start()
        self.join_threads()

    def join_threads(self):
        """
        Joins all threads.
        """
        self.timer_thread.join()
        self.output_thread.join()
        self.input_thread.join()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.join_threads()


if __name__ == "__main__":
    try:
        with SetupManager() as setup_manager:
            synthesizer, chapters, extra_essay = setup_manager.get_setup()
        with ThreadManager(synthesizer=synthesizer, chapters=chapters, extra_essay=extra_essay) as thread_manager:
            for i in range(thread_manager.chapters):
                thread_manager.run_threads(i)
            thread_manager.exit_flag.set()
    except KeyboardInterrupt:
        print("Quitting!")
        quit()