from gtts import gTTS
import os
from pygame import mixer
Text = "C'est fini"
language = 'fr'
output = gTTS(text=Text,lang=language,slow=False)
output.save('output.mp3')

mixer.init()
mixer.music.load('/Users/carstenjuliansavage/PycharmProjects/Random_Project/output.mp3')
mixer.music.play()