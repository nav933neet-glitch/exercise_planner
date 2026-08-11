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


class TaskCard(BoxLayout):

    task_id = NumericProperty()
    title = StringProperty()
    target = StringProperty()
    unit = StringProperty()
    growth = StringProperty()
    dashboard = ObjectProperty(None)
    completed = BooleanProperty(False)

    def delete_task(self):
        if self.dashboard:
            self.dashboard.delete_task(self.task_id)

    def edit_task(self):
        if self.dashboard:
            self.dashboard.edit_task(self.task_id)

    def complete_task(self):
        if self.dashboard:
            self.dashboard.complete_task(self.task_id)

    def show_delete_popup(self):
        layout = BoxLayout(orientation="vertical", spacing=5, padding=10)
        layout.add_widget(Label(text="Are you sure you want to Delete this task?"))

        buttons = BoxLayout(size_hint_y=None, height=40, spacing=10)

        delete_btn = Button(text="Delete")
        cancel_btn = Button(text="Cancel")

        buttons.add_widget(delete_btn)
        buttons.add_widget(cancel_btn)

        layout.add_widget(buttons)

        popup = Popup(
            title="Confirmation",
            content=layout,
            title_align="center",
            size_hint=(0.4, 0.25),
            auto_dismiss=False,
        )
        cancel_btn.bind(on_release=popup.dismiss)

        def delete_task(instance):
            self.delete_task()
            popup.dismiss()

        delete_btn.bind(on_release=delete_task)
        popup.open()

    def show_complete_popup(self):
        layout = BoxLayout(orientation="vertical", spacing=5, padding=10)
        layout.add_widget(Label(text="Are you Done this task?"))

        buttons = BoxLayout(size_hint_y=None, height=40, spacing=10)

        done_btn = Button(text="Done")
        cancel_btn = Button(text="Cancel")

        buttons.add_widget(done_btn)
        buttons.add_widget(cancel_btn)

        layout.add_widget(buttons)

        popup = Popup(
            title="Confirmation",
            content=layout,
            title_align="center",
            size_hint=(0.4, 0.25),
            auto_dismiss=False,
        )
        cancel_btn.bind(on_release=popup.dismiss)

        def complete_task(instance):
            self.complete_task()
            popup.dismiss()

        done_btn.bind(on_release=complete_task)
        popup.open()
