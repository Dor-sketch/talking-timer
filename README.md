# 🧠 Psycho Timer for the Psychometric Entrance Test

Psycho Timer is a Python program designed specifically for candidates preparing for the Psychometric Entrance Test (PET). It aids in effective time management during the test by setting individual timers for each section of the exam,  providing audible instructions and alerts, allow tests modifications and more - all combined with a simple user interface.

**Full interactive experience in less than 25 KB's!**

<div align="center" style="margin: 20px">
   <img src="https://github.com/Dor-sketch/PsychoTimer/assets/138825033/b8bc8d23-0aae-4983-8932-52adaa34b6a5" width="400" height="400" /></img>
</div>

---

### 📝 Table of Contents

<!-- @import "[TOC]" {cmd="toc" depthFrom=2 depthTo=2 orderedList=false} -->

<!-- code_chunk_output -->

- [📜 News](#-news)
- [✨ Features](#-features)
- [📦 Dependencies](#-dependencies)
- [🛠 Installation](#-installation)
- [🚀 Usage](#-usage)
- [📁 Files](#-files)
- [📚 Classes - Behind the Scenes](#-classes---behind-the-scenes)
- [🙏 Contributing](#-contributing)
- [📄 License](#-license)

<!-- /code_chunk_output -->

---

## 📜 News

The program has recently been updated to support text-to-speech capabilities not only with `Azure` but also with `Google Text-to-Speech` and even a local text-to-speech engine, providing enhanced flexibility and accessibility. It can now run **without an internet connection** , **without requiring an Azure SDK key** and **without using a single byte for audio files**.

Features has been tested on macOS and Ubuntu 22.04.

## ✨ Features

- **🔄 Speaker Factory**: New feature that automatically selects the best available text-to-speech engine based on the user's system and internet connectivity. It has the capability to fallback to Google Text-to-Speech and a local text-to-speech engine, enabling the program to run without an internet connection or an Azure SDK key.

   Use `FatimaNeural` voice!

   ![image](https://github.com/Dor-sketch/PsychoTimer/assets/138825033/e5101434-1889-4e75-9452-0e3c61b84bc2)

   Or use `UzmaNeural` voice - use *ANY VOICE!*

   ![image](https://github.com/Dor-sketch/PsychoTimer/assets/138825033/8bb84d10-ee72-4818-84c3-6f18c53d92ff)

- **🕐 Dynamic Section Timers**: Set up individual timers for each section of the PET based on user input.

  ![image](https://github.com/Dor-sketch/PsychoTimer/assets/138825033/9fde1ab0-ff05-45c5-bc3a-4b786544b2bb)

- **🔊 Voice Alerts**: Utilize Azure's text-to-speech capabilities to provide audible alerts, enhancing the user experience.
- **🗣 Randomized Voice Selection**: Every time the program starts, a unique voice is randomly selected for the text-to-speech synthesizer.
- **📝 Optional Essay Section**: Choose to include a 30-minute essay section at the start of the exam.
- **⏸ Pause & Resume**: Easily pause the timer with the "P" key and resume with the "R" key.
- **❌ Quick Exit**: Press "Q" to quickly quit the program anytime.
- **🧩 Modular Structure**: Separate modules for different functionalities (`my_timer.py`, `my_setup.py`, `io_util.py`, `SetupManager`) make it easier for developers to understand and contribute.

---

## 📦 Dependencies

This project uses a mix of Python Standard Library modules and Third-Party Libraries. Below is a list:

### Python Standard Library

- `threading`
- `typing`
- `atexit`
- `curses`
- `time`
- `socket`
- `subprocess`

### Third-Party Libraries

- `gtts` (Google Text-to-Speech)
- `pyttsx3`
- `azure.cognitiveservices.speech`

You can install the required third-party libraries using pip:

```bash
pip install gtts pyttsx3 azure-cognitiveservices-speech
```

## 🛠 Installation

1. Clone the repository to your local machine.
2. Install the required packages (see [Dependencies](#dependencies)).
3. **Optional**:
   1. If you want to use Azure's text-to-speech capabilities, you will need to create an Azure account and get an Azure SDK key. You can follow the instructions [here](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/get-started-text-to-speech?tabs=script%2Cwindowsinstall&pivots=programming-language-python).
   2. Create a new file called `azure_sdk_key.txt` in the same directory as `main.py`.
   3. Paste your Azure SDK key into the `azure_sdk_key.txt` file and save it.
4. Run the program by running `python main.py`.

---

## 🚀 Usage

Program includes interactive walkthrogh:

| ![image](https://github.com/Dor-sketch/PsychoTimer/assets/138825033/478132c8-13c1-42f2-9498-2ee4a9520eb7) | ![image](https://github.com/Dor-sketch/PsychoTimer/assets/138825033/3495ceab-4666-435e-9c13-9bab9645c2f7) |
|---|---|
| ![image](https://github.com/Dor-sketch/PsychoTimer/assets/138825033/cb1426d5-ff1e-4d66-abd2-30174aaf98ab) | ![image](https://github.com/Dor-sketch/PsychoTimer/assets/138825033/fa51c8b1-4698-4319-874d-c78680473001) |
| ![image](https://github.com/Dor-sketch/PsychoTimer/assets/138825033/3b84f4a8-0bb5-4840-afc6-783c6e7d4145) | ![image](https://github.com/Dor-sketch/PsychoTimer/assets/138825033/18f46792-82d7-4e27-8d80-1162e0927db3) |
| ![image](https://github.com/Dor-sketch/PsychoTimer/assets/138825033/5698a513-d67e-4626-80f5-5acbe3dd2a64) | ![image](https://github.com/Dor-sketch/PsychoTimer/assets/138825033/c5d65cd4-3267-4741-afaa-88589f063207) |
| ![image](https://github.com/Dor-sketch/PsychoTimer/assets/138825033/0600c7c5-d8ad-491c-8edf-3a760afaaff9) | ![image](https://github.com/Dor-sketch/PsychoTimer/assets/138825033/a05a445d-2433-4c7b-bca2-3e051d8e6d93) |

1. When prompted, enter the number of sections in the PET.
3. Follow the on-screen instructions to start and stop the timer for each section.
5. Press "P" to pause the timer, and "R" to resume the timer.
6. Press "Q" to quit the program.

## 📁 Files

- `main.py`: The main program file.
- `my_timer.py`: A module that contains the `section_timer` function for managing the section timer.
- `my_setup.py`: A module that contains the `setup` function for setting up the program.
- `io_util.py`: A module that contains utility functions for handling input and output.
- `azure_sdk_key.txt`: A file that contains your Azure SDK key (Optional).
- `README.md`: The README file.

## 📚 Classes - Behind the Scenes

### `SpeakerFactory`

A new addition to the codebase, the `SpeakerFactory` class serves as a factory for generating the appropriate speaker (text-to-speech engine) based on the system and connectivity. It encapsulates the logic for determining the best available speaker service to use and returns an instance of the corresponding speaker wrapper class (`AzureWrapper`, `GttsAsyncWrapper`, `Pyttsx3AzureWrapper`).

#### Key Responsibilities

- **Internet Connection Check**: Checks whether an internet connection is available.
- **Ubuntu 22.04 Check**: Determines if the system is running Ubuntu 22.04.
- **Azure SDK Key Availability**: Checks for the existence of an Azure SDK key.
- **Speaker Instance Creation**: Based on the above checks, it initializes and returns an appropriate speaker instance.

#### Method Descriptions

- `create_speaker`: Creates and returns an appropriate speaker instance.
- `check_internet_connection`: Checks for internet connectivity.
- `is_ubuntu_2204`: Checks if the system is running on Ubuntu 22.04.
- `read_azure_sdk_key`: Reads the Azure SDK key from a file.

### `ThreadManager`

This class handles the orchestration of multiple threads, including threads for timing (`timer_thread`), output (`output_thread`), and input (`input_thread`). It provides methods for preparing thread arguments, starting threads, and joining them back.

#### `ThreadManager` Key Responsibilities

- **Event Initialization**: Initializes several threading events like `stop_flag`, `clock_ticking`, `output_event`, `exit_flag`, and `extra_essay` that control the flow and behavior of the various threads.

- **Thread Arguments Preparation**: Methods like `get_timer_args`, `get_output_args`, and `get_input_args` prepare and return the sets of arguments needed for each of the threads.

- **Thread Execution**: Uses the `run_threads` method to start all threads and the `join_threads` method to join them back, ensuring they have completed their execution.

- **Resource Cleanup**: Implements the `__enter__` and `__exit__` methods to allow the object to be used with Python's `with` statement, ensuring that all threads are joined back at the end of the operation.

#### `ThreadManager` Method Descriptions

- `__init__`: Initializes thread events and sets basic configuration like warning times, chapters, and whether an extra essay is included.
- `initialize_events`: Initializes thread event objects for controlling thread behavior.
- `get_timer_args`, `get_output_args`, `get_input_args`: Prepare arguments for timer, output, and input threads, respectively.
- `run_threads`: Initiates and runs all the threads.
- `join_threads`: Joins all the threads ensuring they have completed their execution.

#### Context Management

The class follows the Context Manager protocol, allowing it to be used with Python's `with` statement. This ensures that all resources are properly cleaned up once out of scope.

#### Libraries and Dependencies

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

## 🙏 Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## 📄 License

This project is licensed under the [MIT License](LICENSE).

**Note:** This is an unofficial timer tool designed to help with the Israeli standard exam. This project is not affiliated with or endorsed by the official exam body.
