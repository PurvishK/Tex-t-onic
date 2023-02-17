# Import the required module for text
# to speech conversion
from gtts import gTTS

# This module is imported so that we can
# play the converted audio
from IPython.display import Audio

# The text that you want to convert to audio
mytext = 'Hi Komali'

# Language in which you want to convert
language = 'en'

# Passing the text and language to the engine
myobj = gTTS(mytext,lang=language)

# Saving the converted audio in a wav file named
# welcome
myobj.save("welcome.wav")

# Playing the converted file
Audio("welcome.wav",autoplay=True)

