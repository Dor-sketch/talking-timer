"""
This module contains the SetupManager class, which is responsible for getting
the number of chapters from the user.
"""

import io_util

from speaker import SpeakerFactory


# Define the instructions as a list of strings
instructions = [
    'Press any key to continue to the next instruction or "Space" key to skip.',
    "This program will help you keep track of your time while studying for the PET exam.",
    'Press the "n" key to move to the next chapter, and press "q" to quit.',
    "The timer will run for 20 minutes, and you will be notified when the time is up.",
    'You can also use the "q" key to quit the program at any time.',
]

# Define a dictionary to map integers to spoken string equivalents
number_dict = {
    0: "zero",
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
}


class SetupManager:
    """
    A class to manage the setup of the program.
    """
    def __init__(self):
        self.synthesizer = SpeakerFactory.create_speaker()
        self.chapters, self.extra_essay = self.get_total_chapters()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        del self.synthesizer

    def check_valid_chapters(self, chapters) -> bool:
        """
        Checks if the number of chapters is valid.

        :param chapters: The number of chapters.
        :return: True if the number of chapters is valid, False otherwise.
        """
        if chapters < 1 or chapters > 8:
            return False
        return True

    def get_setup(self) -> tuple:
        """
        Gets the setup for the program.

        :return: A tuple containing the synthesizer,
            the number of chapters, and whether or not there is an extra essay.
        """
        return self.synthesizer, self.chapters, self.extra_essay

    # a function to get the number of chapters from the user

    def get_chapters_from_input(self) -> int:
        """
        Gets the number of chapters from the user.

        :return: The number of chapters.
        """
        self.synthesizer.speak_text_async("Welcome back!")  # async = non-blocking
        for instruction in instructions:
            # Print the instruction to the io_util.screen
            io_util.screen.addstr(instruction + "\n")
            io_util.screen.refresh()  # Update the io_util.screen to show the instruction
            key = io_util.wait_for_key()  # Wait for the user to press a key
            if key == (
                " "
            ):
                break
        io_util.screen.clear()

        self.synthesizer.speak_text_async("How many chapters?")
        io_util.screen.addstr("Enter the number of chapters: ")
        chapters_str = ""
        while True:
            char = io_util.wait_for_key()
            if char == "\n":
                if self.check_valid_chapters(int(chapters_str)):
                    break
                else:
                    io_util.screen.addstr("Invalid number, try again: ")
                    chapters_str = ""
                    continue
            elif char.isdigit():
                chapters_str += char
                io_util.screen.addstr(char)
            elif char == "\b":
                chapters_str = chapters_str[:-1]
                io_util.screen.addstr("\b \b")
        chapters = int(chapters_str)
        return chapters

    def ask_for_extra_essay(self) -> bool:
        """
        Asks the user if they have an extra essay.

        :return: True if the user has an extra essay, False otherwise.
        """
        self.synthesizer.speak_text_async("Do you have an extra essay?")
        io_util.screen.addstr('\nPress "Y" for 30 minutes essay other key to pass: ')

        while True:
            char = io_util.wait_for_key()
            io_util.screen.addstr(char)
            if char == "\n":
                break
            elif char == "y":
                return True

    def get_total_chapters(self) -> tuple:
        """
        Gets the total number of chapters from the user.

        :return: A tuple containing the number of chapters and whether or not
            there is an extra essay.
        """
        chapters = self.get_chapters_from_input()
        extra_essay = self.ask_for_extra_essay()
        if extra_essay:
            chapters += 1

        self.synthesizer.speak_text_async(
            "Oh Yeah! press any key when you are ready... and good luck!"
        )
        io_util.screen.addstr(f"\nNumber of chapters: {number_dict[chapters]}")
        if extra_essay:
            io_util.screen.addstr(" + exta essay")
        io_util.wait_for_key()
        self.synthesizer.speak_text_async("Test Started!")
        return chapters, extra_essay
