from kivy.properties import (
    BooleanProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty,
)

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.audio import SoundLoader

from kivy.uix.textinput import TextInput

class AlarmCard(BoxLayout):

    def __init__(self, alarm_screen, alarm_id, alarm_type, alarm_time, message, enabled, **kwargs):

         
        self.alarm_screen = alarm_screen
        self.alarm_id = alarm_id
        self.alarm_type = alarm_type
        self.alarm_time = alarm_time
        self.message = message
        self.enabled = enabled
        super().__init__(**kwargs)

    def toggle_alarm(self):
        new_enabled = 0 if self.enabled == 1 else 1
        self.alarm_screen.db.update_alarm_enabled(self.alarm_id, new_enabled)
        self.alarm_screen.load_alarms()

    def delete_alarm(self):
        self.alarm_screen.db.delete_alarm(self.alarm_id)
        self.alarm_screen.load_alarms()