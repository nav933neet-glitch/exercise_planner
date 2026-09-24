from kivy.uix.screenmanager import Screen
from database import Database

class AddAlarmScreen(Screen):
    db = Database()

    def save_alarm(self):

        alarm_time = self.ids.alarm_time.text
        message = self.ids.alarm_message.text
        alarm_type = self.ids.alarm_type.text
        enabled = 1 if self.ids.alarm_enabled.active else 0

        self.db.add_alarm(alarm_type, alarm_time, message, enabled)
        print("Alarm saved!")

        self.manager.current = "alarm"

    def cancel(self):
        self.manager.current = "alarm"