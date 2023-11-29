"""
This is the main file for the application. It manages the threads and the
timer.
"""
import threading
import configparser
from typing import Tuple, Any
from io_util import output_util
from io_util import input_util
from io_util import screen, print_lock
from my_timer import chapter_timer



class ThreadManager:
    """
    Manages multiple threads for the application, including a timer, input, and output handling.
    """

    def __init__(self, synthesizer=None, chapters: int = 8, extra_essay: bool = False):
        self.initialize_events()
        self.load_config()
        self.synthesizer = synthesizer
        self.chapters = chapters
        self.screen = screen
        self.extra_essay_flag = extra_essay
        self.timer_thread = None
        self.output_thread = None
        self.input_thread = None

    def load_config(self):
        """
        Loads configuration settings from a file.
        """
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.warning_time = config.getint(
            'Timer', 'warning_time', fallback=300)
        self.remaining_time = config.getint(
            'Timer', 'chapter_time', fallback=1200)

    def get_timer_args(self) -> Tuple[Any, ...]:
        """
        Prepares and returns the arguments needed for the timer thread.
        """
        return (
            self.stop_flag,
            self.extra_essay,
            self.clock_ticking,
            self.remaining_time,
            self.warning_time,
            self.screen,
            print_lock,
            self.synthesizer
        )

    def get_output_args(self) -> Tuple[Any, ...]:
        """
        Returns the arguments needed for the output thread.
        """
        return (
            self.stop_flag,
            self.exit_flag,
            self.output_event,
            self.synthesizer,
            self.clock_ticking,
            self.chapters,
        )

    def get_input_args(self) -> Tuple[Tuple[Any, ...],]:
        """
        Returns the arguments needed for the input thread.
        """
        return (
            (self.stop_flag, self.exit_flag, self.output_event, self.clock_ticking),
        )

    def initialize_events(self):
        """
        Initializes threading events.
        """
        self.stop_flag = threading.Event()
        self.clock_ticking = threading.Event()
        self.output_event = threading.Event()
        self.exit_flag = threading.Event()
        self.extra_essay = threading.Event()

    def initialize_threads(self, chapter_num: int):
        """
        Initializes threads.
        """
        self.timer_thread = threading.Thread(
            target=chapter_timer, args=(self.get_timer_args(),))
        self.output_thread = threading.Thread(
            target=output_util, args=(chapter_num, self.get_output_args(),))
        self.input_thread = threading.Thread(
            target=input_util, args=self.get_input_args())

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

    def start_threads(self, chapter_num: int):
        """
        Starts all threads.
        """
        self.initialize_threads(chapter_num)
        self.timer_thread.start()
        self.output_thread.start()
        self.input_thread.start()

    def run_threads(self, chapter_num: int):
        """
        Starts threads for a specific chapter and ensures proper management.
        """
        try:
            self.initialize_for_chapter(chapter_num)
            self.start_threads(chapter_num)
            self.join_threads()
        except Exception as e:
            print(f"An error occurred: {e}")
            self.cleanup()

    def initialize_for_chapter(self, chapter_num: int):
        """
        Initializes or resets flags and timers for a new chapter.
        """
        self.stop_flag.clear()
        self.clock_ticking.set()
        if chapter_num > 0 and self.extra_essay_flag:
            self.extra_essay.set()

    def cleanup(self):
        """
        Performs necessary cleanup, especially in case of an error.
        """
        self.stop_flag.set()
        if self.timer_thread.is_alive():
            self.timer_thread.join()
        if self.output_thread.is_alive():
            self.output_thread.join()
        if self.input_thread.is_alive():
            self.input_thread.join()
