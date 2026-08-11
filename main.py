from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from database import Database
from screens.add_task import AddTaskScreen
from screens.dashboard import DashboardScreen
from screens.statistics import StatisticsScreen


class GoalGrowthApp(App):

    def build(self):

        self.db = Database()

        Builder.load_file("kv/dashboard.kv")
        Builder.load_file("kv/add_task.kv")
        Builder.load_file("kv/task_card.kv")
        Builder.load_file("kv/statistics.kv")

        sm = ScreenManager()

        sm.add_widget(DashboardScreen(name="dashboard"))
        sm.add_widget(AddTaskScreen(name="add_task"))
        sm.add_widget(StatisticsScreen(name="statistics"))

        return sm


if __name__ == "__main__":
    GoalGrowthApp().run()
