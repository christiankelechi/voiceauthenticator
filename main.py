from PyQt6.QtWidgets import QMainWindow,QLabel,QTextEdit,QApplication,QPushButton
import sys
import alarm
import datetime
import time
import platform
import winsound
import user_storage
from transformers import AutoTokenizer, OPTForQuestionAnswering
import torch


class LoginView(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setFixedSize(600,600)
        
        self.login_email=QTextEdit(self)
        self.login_email.setPlaceholderText("Enter Email")
        self.login_email.setGeometry(30,30,500,40)
        
        self.password_field=QTextEdit(self)
        self.password_field.setPlaceholderText("Enter Password")
        self.password_field.setGeometry(30,100,500,40)
        
        self.submit_button=QPushButton(self)
        self.submit_button.setText("Login")
        self.submit_button.setStyleSheet("background-color:blue;")
        self.submit_button.setGeometry(30,300,500,40)
        
        self.submit_button.clicked.connect(self.storeData)
        self.show()
    
    

    
    
    def runAlarm(self):
        current_time = datetime.datetime.now()
        # print("Current Time:", current_time)


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
        
        
        email=self.login_email.toPlainText()
        password=self.password_field.toPlainText()
        
        if password=='1234':
            user_storage.storeCredentials(email=email,password=password)
            text = f"Welcome to Codeblaze Academy, Your password for reference is as follows : {password}"

            import pyttsx4
            engine = pyttsx4.init()
          
            engine.say(text)
            engine.runAndWait()
        else:
            self.runAlarm()
            
        
    
app=QApplication(sys.argv)
window=LoginView()
sys.exit(app.exec())