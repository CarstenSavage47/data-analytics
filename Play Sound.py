from gtts import gTTS
import os
from playsound import playsound
Text = "C'est fini"
language = 'fr'
output = gTTS(text=Text,lang=language,slow=False)
output.save('output.mp4')
playsound('output.mp4')