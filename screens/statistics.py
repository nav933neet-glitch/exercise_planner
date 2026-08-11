from kivy.uix.screenmanager import Screen

from database import Database


class StatisticsScreen(Screen):

    db = Database()

    def on_enter(self):
        self.load_statistics()

    def load_statistics(self):
        stats = self.db.get_statistics()
        self.ids.total_tasks.text = str(stats["total_tasks"])
        self.ids.fixed_tasks.text = str(stats["fixed_tasks"])
        self.ids.growing_tasks.text = str(stats["growing_tasks"])
        self.ids.completed_today.text = (
            f"{stats['completed_today']} / {stats['total_tasks']}"
        )

        self.ids.total_completed.text = str(stats["total_completed"])
        self.ids.progress.text = f"{stats['progress']} %"

        self.ids.current_streak.text = f"{stats['current_streak']} Days"
        self.ids.best_streak.text = f"{stats['best_streak']} Days"