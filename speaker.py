import socket
import subprocess
from gtts import gTTS
import pyttsx3
import azure.cognitiveservices.speech as speechsdk
import random

AZURE_SDK_KEY_FILE = "azure_sdk_key.txt"
AZURE_SDK_REGION = "eastus"


class SpeakerFactory:
    @staticmethod
    def create_speaker():
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
    def check_internet_connection():
        try:
            socket.gethostbyname('www.google.com')
            return True
        except socket.error:
            return False

    @staticmethod
    def is_ubuntu_2204():
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
    def read_azure_sdk_key():
        try:
            with open(AZURE_SDK_KEY_FILE, 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            return None


class GttsAsyncWrapper:
    def __init__(self, lang='en'):
        self.lang = lang
        self.speak_text_async("Hello, world! I am google text to speech!")

    def speak_text_async(self, text):
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
    def __init__(self):
        self.synthesizer = self.setup_synthesizer()

    def speak_text_async(self, text: str):
        self.synthesizer.speak_text_async(text)

    def read_azure_sdk_key(self):
        try:
            with open(AZURE_SDK_KEY_FILE, 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            return None

    def setup_synthesizer(self):
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
            # Replace this with your actual input method
            user_input = input(
                "Press 'c' to continue or any other key to choose again: ")

            if user_input == 'c':
                break
            else:
                del synthesizer

        return synthesizer
