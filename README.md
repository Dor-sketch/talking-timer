# 🧠 Psycho Timer for the Psychometric Entrance Test

## 📜 Description

Psycho Timer is a Python program designed specifically for candidates preparing for the Psychometric Entrance Test (PET). It aids in effective time management during the test by setting individual timers for each section of the exam. The program also integrates with Azure to utilize text-to-speech capabilities, providing audible alerts for enhanced user experience. It has been tested on macOS.

## ✨ Features

- **🕐 Dynamic Section Timers**: Set up individual timers for each section of the PET based on user input.
- **🔊 Voice Alerts**: Utilize Azure's text-to-speech capabilities to provide audible alerts, enhancing the user experience.
- **🗣 Randomized Voice Selection**: Every time the program starts, a unique voice is randomly selected for the text-to-speech synthesizer.
- **📝 Optional Essay Section**: Choose to include a 30-minute essay section at the start of the exam.
- **⏸ Pause & Resume**: Easily pause the timer with the "P" key and resume with the "R" key.
- **❌ Quick Exit**: Press "Q" to quickly quit the program anytime.
- **🧩 Modular Structure**: Separate modules for different functionalities (`my_timer.py`, `my_setup.py`, `io_util.py`, `SetupManager`) make it easier for developers to understand and contribute.

## Classes 📚

### `ThreadManager`

This class handles the orchestration of multiple threads, including threads for timing (`timer_thread`), output (`output_thread`), and input (`input_thread`). It provides methods for preparing thread arguments, starting threads, and joining them back.

#### Key Responsibilities:

- **Event Initialization**: Initializes several threading events like `stop_flag`, `clock_ticking`, `output_event`, `exit_flag`, and `extra_essay` that control the flow and behavior of the various threads.

- **Thread Arguments Preparation**: Methods like `get_timer_args`, `get_output_args`, and `get_input_args` prepare and return the sets of arguments needed for each of the threads.

- **Thread Execution**: Uses the `run_threads` method to start all threads and the `join_threads` method to join them back, ensuring they have completed their execution.

- **Resource Cleanup**: Implements the `__enter__` and `__exit__` methods to allow the object to be used with Python's `with` statement, ensuring that all threads are joined back at the end of the operation.

#### Method Descriptions:

- `__init__`: Initializes thread events and sets basic configuration like warning times, chapters, and whether an extra essay is included.
- `initialize_events`: Initializes thread event objects for controlling thread behavior.
- `get_timer_args`, `get_output_args`, `get_input_args`: Prepare arguments for timer, output, and input threads, respectively.
- `run_threads`: Initiates and runs all the threads.
- `join_threads`: Joins all the threads ensuring they have completed their execution.

#### Context Management:

The class follows the Context Manager protocol, allowing it to be used with Python's `with` statement. This ensures that all resources are properly cleaned up once out of scope.

#### Libraries and Dependencies:

- `threading`: Used for handling threads.
- `my_timer`: Contains the function for the timer thread.
- `my_setup.SetupManager`: For initial setup.
- `io_util`: Contains utility functions for input and output.

### `SetupManager`

Manages the program setup, including initializing the Azure text-to-speech synthesizer and handling user input for setting up the test chapters. It uses the `azure.cognitiveservices.speech` library for Azure's text-to-speech capabilities. The class follows a context manager pattern, using `__enter__` and `__exit__` methods to manage resources.

- **Resource Management**: It uses the context manager methods (`__enter__` and `__exit__`) to handle Azure synthesizer resource allocation and deallocation.
- **User Interactions**: This class takes care of fetching input from the user regarding the number of chapters and whether an extra essay is needed.
- **Speech Synthesis**: It initializes a speech synthesizer and selects a random voice for the session.
- **Validity Checks**: The class contains methods to validate user inputs.

## 🛠 Installation

1. Clone the repository to your local machine.
2. Install the required packages by running `pip install -r requirements.txt`.
3. Create a new file called `azure_sdk_key.txt` in the same directory as `main.py`.
4. Paste your Azure SDK key into the `azure_sdk_key.txt` file and save it.
5. Run the program by running `python main.py`.

Note: This program has been tested on macOS.

## 🚀 Usage

1. When prompted, enter the number of sections in the PET.
2. Follow the on-screen instructions to start and stop the timer for each section.
3. Press "P" to pause the timer, and "R" to resume the timer.
4. Press "Q" to quit the program.

## 📁 Files

- `main.py`: The main program file.
- `my_timer.py`: A module that contains the `section_timer` function for managing the section timer.
- `my_setup.py`: A module that contains the `setup` function for setting up the program.
- `io_util.py`: A module that contains utility functions for handling input and output.
- `azure_sdk_key.txt`: A file that contains your Azure SDK key.

## 🙏 Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## 📄 License

This project is licensed under the [MIT License](LICENSE).
