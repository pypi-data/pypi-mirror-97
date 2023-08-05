from gtts import gTTS
from playsound import playsound
import os

class speech:
    def __init__(self):
        self.lang = 'vi'
        self.slow = False
        self.path_file = os.path.abspath('am-thanh.mp3')

    def to_speech(self, text):
        data = gTTS(text=text, lang=self.lang, slow=self.slow)
        data.save(self.path_file)
        playsound(self.path_file)

        if os.path.exists(self.path_file):
            os.remove(self.path_file)
