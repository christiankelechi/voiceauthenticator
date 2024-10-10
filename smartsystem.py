import sys
import time
import datetime
import winsound
from PyQt6.QtWidgets import QMainWindow, QTextEdit, QApplication, QPushButton
import speech_recognition as sr
import user_storage
import pyttsx4


class LoginView(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setFixedSize(600, 600)

        self.login_email = QTextEdit(self)
        self.login_email.setPlaceholderText("Enter Username")
        self.login_email.setGeometry(30, 30, 500, 40)

        self.password_field = QTextEdit(self)
        self.password_field.setPlaceholderText("Enter Password")
        self.password_field.setGeometry(30, 100, 500, 40)

        self.submit_button = QPushButton(self)
        self.submit_button.setText("Login")
        self.submit_button.setStyleSheet("background-color:black;color:white;")
        self.submit_button.setGeometry(30, 300, 200, 40)
        self.submit_button.clicked.connect(self.storeData)

        self.record_button = QPushButton(self)
        self.record_button.setText("Login Via Voice")
        self.record_button.setStyleSheet("background-color:black;color:white;")
        self.record_button.setGeometry(300, 300, 200, 40)
        self.record_button.clicked.connect(self.recordVoice)
        
        
        self.show()

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

        # Record and set password
        engine.say("Please pronounce your password...")
        engine.runAndWait()
        password = self.recognize_speech("Listening for password...", recognizer)
        if password:
            self.password_field.setText(password)
            engine.say(f"Password recorded.")
            engine.runAndWait()

        engine.say("Pronounce Login to enable you to login, note if password is incorrect you will be denied access and the root user will be notified..")
        engine.runAndWait()
        login_prompt = self.recognize_speech("Listening for login prompt...", recognizer)
    
        if login_prompt:
                
            if login_prompt.lower()=='login':
                self.storeData()
                
             
            
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
        siren_sound = "policealarm.wav"
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
