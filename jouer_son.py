from gtts import gTTS
import os
from pygame import mixer
Text = "J'ai fini le code"
language = 'fr'

def jouer_son(x):
    output = gTTS(text=x,lang=language,slow=False)
    output.save('output.mp3')
    mixer.init()
    mixer.music.load('output.mp3')
    mixer.music.play()

jouer_son(Text)