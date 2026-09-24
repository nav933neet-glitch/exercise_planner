import os
from kivy.core.audio import SoundLoader

timer_sound = SoundLoader.load("sounds/timer_end.wav")

if timer_sound:
    timer_sound.play()
    print("✅ Timer sound loaded")
else:
    print("❌ Timer sound NOT loaded")