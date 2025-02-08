import speech_recognition as sr
import pyttsx3
import speech_recognition as sr
from pydub import AudioSegment

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()


# Function to convert speech to text
def mp3_to_text(mp3_file):
    recognizer = sr.Recognizer()

    # Convert MP3 to WAV (since SpeechRecognition needs WAV)
    wav_file = "temp_audio.wav"
    audio = AudioSegment.from_mp3(mp3_file)
    audio.export(wav_file, format="wav")

    with sr.AudioFile(wav_file) as source:
        audio_data = recognizer.record(source)  # Read the entire file

        try:
            text = recognizer.recognize_google(audio_data)  # Convert to text
            print("Transcribed Text:", text)
            return text
        except sr.UnknownValueError:
            print("Could not understand the audio.")
            return None
        except sr.RequestError:
            print("Error connecting to Google API.")
            return None


# Function to convert text to speech
def text_to_voice(text):
    if text:
        print("Speaking:", text)
        tts_engine.say(text)  # Convert text to speech
        tts_engine.runAndWait()


if __name__ == "__main__":
    # text_to_voice("Hello my name is adil")
    mp3_file_path = (
        "C:\\Users\\asus\\Downloads\\Secret Psychology to Nail an Interview.mp3"
    )
    mp3_to_text(mp3_file_path)
