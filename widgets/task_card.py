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

                
        delete_btn.background_color = (0, 0, 0, 0)
        cancel_btn.background_color = (0, 0, 0, 0)

        with delete_btn.canvas.before:
            Color(0.65, 0.12, 0.12, 1)
            delete_btn.bg = RoundedRectangle(
                pos=delete_btn.pos,
                size=delete_btn.size,
                radius=[20]
            )

        delete_btn.bind(
            pos=lambda instance, value: setattr(instance.bg, "pos", value),
            size=lambda instance, value: setattr(instance.bg, "size", value)
        )

        with cancel_btn.canvas.before:
            Color(0.25, 0.25, 0.25, 1)
            cancel_btn.bg = RoundedRectangle(
                pos=cancel_btn.pos,
                size=cancel_btn.size,
                radius=[20]
            )

        cancel_btn.bind(
            pos=lambda instance, value: setattr(instance.bg, "pos", value),
            size=lambda instance, value: setattr(instance.bg, "size", value)
        )
        
        buttons.add_widget(delete_btn)
        buttons.add_widget(cancel_btn)

        layout.add_widget(buttons)

        popup = Popup(
            title="Confirmation",
            content=layout,
            title_align="center",
            size_hint=(0.80, 0.20),
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

                        
        done_btn.background_color = (0, 0, 0, 0)
        cancel_btn.background_color = (0, 0, 0, 0)

        with done_btn.canvas.before:
            Color(0.10, 0.50, 0.25, 1)
            done_btn.bg = RoundedRectangle(
                pos=done_btn.pos,
                size=done_btn.size,
                radius=[20]
            )

        done_btn.bind(
            pos=lambda instance, value: setattr(instance.bg, "pos", value),
            size=lambda instance, value: setattr(instance.bg, "size", value)
        )

        with cancel_btn.canvas.before:
            Color(0.25, 0.25, 0.25, 1)
            cancel_btn.bg = RoundedRectangle(
                pos=cancel_btn.pos,
                size=cancel_btn.size,
                radius=[20]
            )

        cancel_btn.bind(
            pos=lambda instance, value: setattr(instance.bg, "pos", value),
            size=lambda instance, value: setattr(instance.bg, "size", value)
        )

        buttons.add_widget(done_btn)
        buttons.add_widget(cancel_btn)

        layout.add_widget(buttons)

        popup = Popup(
            title="Confirmation",
            content=layout,
            title_align="center",
            size_hint=(0.80, 0.20),
            auto_dismiss=False,
        )
        cancel_btn.bind(on_release=popup.dismiss)

        def complete_task(instance):
            self.complete_task()
            popup.dismiss()

        done_btn.bind(on_release=complete_task)
        popup.open()

    def start_timer(self):

        hours = TextInput(text="00", multiline=False, input_filter="int", halign="center", font_size="25sp")
        minutes = TextInput(text="00", multiline=False, input_filter="int", halign="center", font_size="25sp")
        seconds = TextInput(text="00", multiline=False, input_filter="int", halign="center", font_size="25sp")

        time_layout = BoxLayout(orientation="horizontal", spacing=dp(5), size_hint_y=None, height=dp(55))

        time_layout.add_widget(hours)
        time_layout.add_widget(Label(text=":", font_size="25sp", size_hint_x=None, width=dp(20)))
        time_layout.add_widget(minutes)
        time_layout.add_widget(Label(text=":", font_size="25sp", size_hint_x=None, width=dp(20)))
        time_layout.add_widget(seconds)

        start_button = Button(text="Start", size_hint_y=None, height=dp(45))
        cancel_button = Button(text="Cancel", size_hint_y=None, height=dp(45))

        buttons = BoxLayout(orientation="horizontal", spacing=dp(10), size_hint_y=None, height=dp(45))
        buttons.add_widget(start_button)
        buttons.add_widget(cancel_button)

        layout = BoxLayout(orientation="vertical", spacing=dp(15), padding=dp(15))
        layout.add_widget(Label(text="Set Timer", font_size="22sp", size_hint_y=None, height=dp(40)))

        layout.add_widget(time_layout)
        layout.add_widget(buttons)

        popup = Popup(title="Timer", content=layout, size_hint=(0.8, 0.4), auto_dismiss=False)
        timer_sound = SoundLoader.load("sounds/timer_end.wav")

        def start_countdown(instance):
            try:
                h = int(hours.text or 0)
                m = int(minutes.text or 0)
                s = int(seconds.text or 0)

                if m > 59 or s > 59:
                    return
                total_seconds = (h * 3600 + m * 60 + s)
                if total_seconds <= 0:
                    return
                layout.clear_widgets()

                timer_label = Label(text=self.format_time(total_seconds), font_size="45sp")
                stop_button = Button(text="Stop", size_hint_y=None, height=dp(45))
                pause_button = Button(text="Pause", size_hint_y=None, height=dp(45))

                # Buttons will be side-by-side
                timer_buttons = BoxLayout(orientation="horizontal", spacing=dp(10), size_hint_y=None, height=dp(45))
                timer_buttons.add_widget(pause_button)
                timer_buttons.add_widget(stop_button)

                # Timer first, buttons underneath
                layout.add_widget(timer_label)
                layout.add_widget(timer_buttons)

                self.remaining_seconds = total_seconds

                def update_timer(dt):
                    if self.remaining_seconds > 0:
                        self.remaining_seconds -= 1
                        timer_label.text = self.format_time(self.remaining_seconds)

                        if self.remaining_seconds == 0:
                            self.timer_event.cancel()

                            # 🔔 Play sound
                            if timer_sound:
                                timer_sound.play()

                            # ⏰ Finished popup
                            finished_label = Label(text="Timer Finished!", font_size="25sp")
                            ok_button = Button(text="OK", size_hint_y=None, height=dp(45))

                            finished_layout = BoxLayout(orientation="vertical", spacing=dp(15), padding=dp(15))
                            finished_layout.add_widget(finished_label)
                            finished_layout.add_widget(ok_button)

                            finished_popup = Popup(
                                title="Timer Finished!",
                                content=finished_layout,
                                size_hint=(0.75, 0.35),
                                auto_dismiss=False
                            )
                            def stop_sound_and_close(instance):
                                if timer_sound:
                                    timer_sound.stop()

                                finished_popup.dismiss()
                                popup.dismiss()

                                # 🏠 Go back to Dashboard
                                if self.dashboard:
                                    self.dashboard.manager.current = "dashboard"
                            ok_button.bind(on_release=stop_sound_and_close)
                            finished_popup.open()

                self.timer_event = Clock.schedule_interval(update_timer, 1)

                def pause_resume_timer(instance):
                    if pause_button.text == "Pause":

                        # Pause timer
                        if hasattr(self, "timer_event"):
                            self.timer_event.cancel()
                        pause_button.text = "Resume"

                    else:
                        # Resume timer
                        self.timer_event = Clock.schedule_interval(update_timer, 1)
                        pause_button.text = "Pause"
                pause_button.bind(on_release=pause_resume_timer)

                # Stop timer
                def stop_timer(instance):
                    if hasattr(self, "timer_event"):
                        self.timer_event.cancel()
                    popup.dismiss()
                stop_button.bind(on_release=stop_timer)
            except ValueError:
                pass

        start_button.bind(on_release=start_countdown)
        cancel_button.bind(on_release=lambda x: popup.dismiss())
        popup.open()


    def format_time(self, total_seconds):

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"