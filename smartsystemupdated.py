import sys
import time
import datetime
import winsound
import wave
import numpy as np
from PyQt6.QtWidgets import QMainWindow, QTextEdit, QApplication, QPushButton
import speech_recognition as sr
import user_storage
import pyttsx4
from pydub import AudioSegment
from pydub.playback import play

class LoginView(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(1200, 620)

        self.login_email = QTextEdit(self)
        self.login_email.setPlaceholderText("Enter Username")
        self.login_email.setStyleSheet("font-size:80px")
        self.login_email.setGeometry(30, 30, 1000, 100)

        self.password_field = QTextEdit(self)
        self.password_field.setPlaceholderText("Enter Password")
        self.password_field.setGeometry(30, 200, 1000, 100)
        self.password_field.setStyleSheet("font-size:80px")

        self.submit_button = QPushButton(self)
        self.submit_button.setText("Login")
        self.submit_button.setStyleSheet("background-color:black;color:white;")
        self.submit_button.setGeometry(30, 370, 500, 40)
        self.submit_button.clicked.connect(self.storeData)

        self.record_button = QPushButton(self)
        self.record_button.setText("Login Via Voice")
        self.record_button.setStyleSheet("background-color:black;color:white;")
        self.record_button.setGeometry(600, 370, 500, 40)
        self.record_button.clicked.connect(self.recordVoice)

        self.show()
    def verify_phrase(self):
        recognizer = sr.Recognizer()
        engine = pyttsx4.init()

        # Record the verification phrase again for comparison
        engine.say("Please pronounce your verification phrase for confirmation...")
        engine.runAndWait()
        verification_audio = self.record_and_save_audio("Listening for verification phrase for confirmation...", recognizer, 'user_verification.wav')

        if verification_audio:
            # Compare the new recording with the saved verification phrase
            if self.compare_audio('verification_phrase.wav', 'user_verification.wav'):
                self.storeData()
            else:
                engine.say("Verification failed. Access denied.")
                engine.runAndWait()
                self.runAlarm()

    def compare_audio(self, original_file, new_file):
        # Load the original and new audio files using pydub
        original_audio = AudioSegment.from_wav(original_file)
        new_audio = AudioSegment.from_wav(new_file)

        # Normalize the audio
        original_audio = original_audio.set_frame_rate(44100).set_channels(1).set_sample_width(2)
        new_audio = new_audio.set_frame_rate(44100).set_channels(1).set_sample_width(2)

        # Compare the audio files
        return self.compare_tone(original_audio, new_audio)

    def compare_tone(self, original_audio, new_audio):
        # Calculate the pitch of the audio files
        original_pitch = self.calculate_pitch(original_audio)
        new_pitch = self.calculate_pitch(new_audio)

        # Compare the pitch values
        pitch_difference = abs(original_pitch - new_pitch)
        return pitch_difference < 0.1  # Adjust the threshold as needed

    def calculate_pitch(self, audio):
        # Calculate the pitch using pydub's pitch_shift function
        # This is a simplified approach, you may need to adjust it based on your requirements
        return audio.pitch_shift(1000, 44100)
    
    def recordVoice(self):
        recognizer = sr.Recognizer()
        engine = pyttsx4.init()

        # Record and set username
        engine.say("Please pronounce your username...")
        engine.runAndWait()
        username = self.recognize_speech("Listening for username...", recognizer)
        if username:
            self.login_email.setText(username.lower())
            engine.say(f"Username '{username}' recorded.")
            engine.runAndWait()

        # Record and save password as WAV file
        engine.say("Please pronounce your password...")
        engine.runAndWait()
        password_audio = self.record_and_save_audio("Listening for password...", recognizer, 'user_password.wav')

        if password_audio:
            engine.say("Password recorded.")
            engine.runAndWait()

        engine.say("Please pronounce a phrase for verification...")
        engine.runAndWait()
        verification_audio = self.record_and_save_audio("Listening for verification phrase...", recognizer, 'verification_phrase.wav')

        if verification_audio:
            engine.say("Verification phrase recorded.")
            engine.runAndWait()

        engine.say("Pronounce Login to enable you to login.")
        engine.runAndWait()
        login_prompt = self.recognize_speech("Listening for login prompt...", recognizer)

        if login_prompt and login_prompt.lower() == 'login':
            self.verify_phrase()

    def record_and_save_audio(self, prompt, recognizer, filename):
        with sr.Microphone() as source:
            print(prompt)
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            audio_data = audio.get_wav_data()

            # Save the audio data as a WAV file
            self.save_audio_to_wav(filename, audio_data)
            print(f'Recorded and saved as {filename}')
            return True

    def save_audio_to_wav(self, filename, audio_data):
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)  # mono
            wf.setsampwidth(2)  # 16 bits
            wf.setframerate(44100)  # Sample rate
            wf.writeframes(audio_data)

    # def verify_phrase(self):
    #     recognizer = sr.Recognizer()
    #     engine = pyttsx4.init()

    #     # Record the verification phrase again for comparison
    #     engine.say("Please pronounce your verification phrase for confirmation...")
    #     engine.runAndWait()
    #     verification_audio = self.record_and_save_audio("Listening for verification phrase for confirmation...", recognizer, 'user_verification.wav')

    #     if verification_audio:
    #         # Compare the new recording with the saved verification phrase
    #         if self.compare_audio('verification_phrase.wav', 'user_verification.wav'):
    #             self.storeData()
    #         else:
    #             engine.say("Verification failed. Access denied.")
    #             engine.runAndWait()
    #             self.runAlarm()

    # def compare_audio(self, original_file, new_file):
    #     # Load the original and new audio files using pydub
    #     original_audio = AudioSegment.from_wav(original_file)
    #     new_audio = AudioSegment.from_wav(new_file)

    #     # Normalize the audio
    #     original_audio = original_audio.set_frame_rate(44100).set_channels(1).set_sample_width(2)
    #     new_audio = new_audio.set_frame_rate(44100).set_channels(1).set_sample_width(2)

    #     # Compare the audio files
    #     return self.audio_similarity(original_audio, new_audio)

    # def audio_similarity(self, original_audio, new_audio):
    #     # Calculate similarity using RMS (Root Mean Square) energy
    #     original_rms = original_audio.rms
    #     new_rms = new_audio.rms

    #     # Compare RMS values
    #     return original_rms == new_rms  # You can implement a more sophisticated comparison if needed

    def recognize_speech(self, prompt, recognizer):
        with sr.Microphone() as source:
            print(prompt)
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio)
                print(f"Recognized: {text}")
                return text
            except sr.UnknownValueError:
                print("Sorry, I could not understand the audio.")
                return ""
            except sr.RequestError as e:
                print(f"Could not request results from the speech recognition service; {e}")
                return ""

    def runAlarm(self):
        current_time = datetime.datetime.now()
        incremented_time = current_time + datetime.timedelta(seconds=1)
        print("Incremented Time:", incremented_time)

        while datetime.datetime.now() < incremented_time:
            time.sleep(1)
        siren_sound = "week_3_and_4/policealarm.wav"
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=5)
        while datetime.datetime.now() < end_time:
            winsound.PlaySound(siren_sound, winsound.SND_FILENAME)

        print(end_time)

    def storeData(self):
        email = self.login_email.toPlainText()
        password = self.password_field.toPlainText()

        engine = pyttsx4.init()

        if password == '1234':
            user_storage.storeCredentials(email=email, password=password)
            text = f"Welcome to Codeblaze Academy, Your password for reference is as follows: {password}"
            engine.say(text)
            engine.runAndWait()
        else:
            text = f"Incorrect password '{password}'. Access denied."
            engine.say(text)
            engine.runAndWait()
            self.runAlarm()

app = QApplication(sys.argv)
window = LoginView()
sys.exit(app.exec())