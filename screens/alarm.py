from kivy.uix.screenmanager import Screen
from database import Database
from widgets.alarm_card import AlarmCard
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout

class AddAlarmPopup(BoxLayout):
    pass

class AlarmScreen(Screen):
    db = Database()

    def on_enter(self):
        #self.db.add_alarm( "daily", "07:00", "Morning Exercise", 1)
        self.load_alarms()

    def load_alarms(self):
        self.ids.alarm_container.clear_widgets()
        alarms = self.db.get_alarms()

        for alarm in alarms:
            card = AlarmCard(
                alarm_screen = self,
                alarm_id = alarm["id"],
                alarm_type = alarm["alarm_type"],
                alarm_time = alarm["alarm_time"],
                message = alarm["message"],
                enabled = alarm["enabled"]
            )
            print("CARD CREATED:", card)
            self.ids.alarm_container.add_widget(card)

    def open_add_alarm_popup(self):
        content = AddAlarmPopup()
        popup = Popup(
            title="Add Alarm",
            size_hint=(0.8, 0.8),
            content = content
        )

        popup.open()