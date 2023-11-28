"""
This module contains the SpeakerFactory class, which is used to create a speaker.

The SpeakerFactory class is used to create a speaker. It checks if the user has
an internet connection, and if so, it checks if the user is using Ubuntu 22.04.

If the user is using Ubuntu 22.04, or if the user does not have an internet
connection, the SpeakerFactory class will create a GttsAsyncWrapper object.

If the user is not using Ubuntu 22.04 and has an internet connection, the
SpeakerFactory class will check if the user has an Azure SDK key. If the user
has an Azure SDK key, the SpeakerFactory class will create an AzureWrapper
object. If the user does not have an Azure SDK key, the SpeakerFactory class
will create a GttsAsyncWrapper object.

If the user is using Ubuntu 22.04 and has an internet connection, the
SpeakerFactory class will create a Pyttsx3AzureWrapper object.
"""
import socket
import subprocess
import random
import pyttsx3
import azure.cognitiveservices.speech as speechsdk
from gtts import gTTS
from io_util import wait_for_key
from io_util import screen

AZURE_SDK_KEY_FILE = "azure_sdk_key.txt"
AZURE_SDK_REGION = "eastus"


class SpeakerFactory:
    """
    A factory class for creating a speaker.
    """
    @staticmethod
    def create_speaker() -> object:
        """
        Creates a speaker.

        :return: A speaker.
        """
        speaker = None

        if SpeakerFactory.check_internet_connection():
            if SpeakerFactory.is_ubuntu_2204() or not SpeakerFactory.read_azure_sdk_key():
                speaker = GttsAsyncWrapper()
            else:
                speaker = AzureWrapper()
        else:
            speaker = Pyttsx3AzureWrapper()

        return speaker

    @staticmethod
    def check_internet_connection() -> bool:
        """
        Checks if the user has an internet connection.

        :return: True if the user has an internet connection, False otherwise.
        """
        try:
            socket.gethostbyname('www.google.com')
            return True
        except socket.error:
            return False

    @staticmethod
    def is_ubuntu_2204() -> bool:
        """
        Checks if the user is using Ubuntu 22.04.

        :return: True if the user is using Ubuntu 22.04, False otherwise.
        """
        try:
            with open("/etc/os-release") as f:
                content = f.readlines()
            for line in content:
                if line.startswith("NAME="):
                    if "Ubuntu" not in line:
                        return False
                if line.startswith("VERSION_ID="):
                    if '22.04' in line:
                        return True
        except FileNotFoundError:
            return False
        return False

    @staticmethod
    def read_azure_sdk_key() -> str:
        """
        Reads the Azure SDK key from the file.

        :return: The Azure SDK key.
        """
        try:
            with open(AZURE_SDK_KEY_FILE, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            return ""


class GttsAsyncWrapper:
    """
    A wrapper class for gTTS that mimics Azure TTS's interface.
    """
    def __init__(self, lang='en'):
        self.lang = lang
        self.speak_text_async("Hello, world! I am google text to speech!")

    def speak_text_async(self, text):
        """
        Mimics Azure's speak_text_async method.

        :param text: The text to be spoken.
        """
        tts = gTTS(text=text, lang=self.lang)
        tts.save("temp.mp3")
        subprocess.Popen(["mpg321", "temp.mp3"],
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL,
                         shell=False)


class Pyttsx3AzureWrapper:
    """A wrapper class for pyttsx3 that mimics Azure TTS's interface."""

    def __init__(self):
        """Initialize the pyttsx3 engine."""
        self.engine = pyttsx3.init()

    def speak_text_async(self, text: str):
        """
        Mimics Azure's speak_text_async method.

        :param text: The text to be spoken.
        """
        self.engine.say(text)
        self.engine.runAndWait()


class AzureWrapper:
    """
    A wrapper class for Azure TTS.
    """
    def __init__(self):
        self.synthesizer = self.setup_synthesizer()

    def speak_text_async(self, text: str) -> None:
        """
        Mimics Azure's speak_text_async method.

        :param text: The text to be spoken.
        """
        self.synthesizer.speak_text_async(text)

    def read_azure_sdk_key(self) -> str:
        """
        Reads the Azure SDK key from the file.

        :return: The Azure SDK key.
        """
        try:
            with open(AZURE_SDK_KEY_FILE, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            return None

    def setup_synthesizer(self) -> speechsdk.SpeechSynthesizer:
        """
        Sets up the Azure TTS synthesizer.

        :return: The Azure TTS synthesizer.
        """
        subscription_key = self.read_azure_sdk_key()
        speech_config = speechsdk.SpeechConfig(
            subscription=subscription_key, region=AZURE_SDK_REGION)
        audio_config = speechsdk.audio.AudioOutputConfig(
            use_default_speaker=True)
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config, audio_config=audio_config)
        voices_result = synthesizer.get_voices_async().get()
        voices = voices_result.voices

        while True:
            random_voice = random.choice(voices)
            # Set the speech synthesis voice to the random voice
            speech_config.speech_synthesis_voice_name = random_voice.name
            synthesizer.speak_text_async("Hello, world!")

            # Replace this with your actual display method
            print("Tester voice is:", random_voice.name)

            user_input = wait_for_key()

            if user_input == 'c':
                break
            else:
                del synthesizer
                synthesizer = speechsdk.SpeechSynthesizer(
                    speech_config=speech_config, audio_config=audio_config)

        return synthesizer
