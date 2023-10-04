# Psycho Timer for the Psychometric Entrance Test


## Description:

Psycho Timer is a Python program designed specifically for candidates preparing for the Psychometric Entrance Test (PET). It aids in effective time management during the test by setting individual timers for each section of the exam. The program also integrates with Azure to utilize text-to-speech capabilities, providing audible alerts for enhanced user experience. It has been tested on macOS.

## Features:

- **Dynamic Section Timers**: Set up individual timers for each section of the PET based on user input.
- **Voice Alerts**: Utilize Azure's text-to-speech capabilities to provide audible alerts, enhancing the user experience.
- **Randomized Voice Selection**: Every time the program starts, a unique voice is randomly selected for the text-to-speech synthesizer.
- **Optional Essay Section**: Choose to include a 30-minute essay section at the start of the exam.
- **Pause & Resume**: Easily pause the timer with the "P" key and resume with the "R" key.
- **Quick Exit**: Press "Q" to quickly quit the program anytime.
- **Modular Structure**: Separate modules for different functionalities (`my_timer.py`, `my_setup.py`, `io_util.py`) make it easier for developers to understand and contribute.


## Installation

1. Clone the repository to your local machine.
2. Install the required packages by running `pip install -r requirements.txt`.
3. Create a new file called `azure_sdk_key.txt` in the same directory as `main.py`.
4. Paste your Azure SDK key into the `azure_sdk_key.txt` file and save it.
4. Run the program by running `python main.py`.

Note: This program has been tested on macOS.

## Usage

1. When prompted, enter the number of sections in the PET.
2. Follow the on-screen instructions to start and stop the timer for each section.
3. Press "P" to pause the timer, and "R" to resume the timer.
4. Press "Q" to quit the program.

## Files

- `main.py`: The main program file.
- `my_timer.py`: A module that contains the `section_timer` function for managing the section timer.
- `my_setup.py`: A module that contains the `setup` function for setting up the program.
- `io_util.py`: A module that contains utility functions for handling input and output.
- `azure_sdk_key.txt`: A file that contains your Azure SDK key.


## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
