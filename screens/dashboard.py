from kivy.uix.screenmanager import Screen

from database import Database
from widgets.task_card import TaskCard


class DashboardScreen(Screen):
    db = Database()

    def on_enter(self):
        self.db.daily_reset()
        self.load_tasks()

    def load_tasks(self):
        self.ids.fixed_container.clear_widgets()
        self.ids.growing_container.clear_widgets()
        fixed_tasks = self.db.get_fixed_tasks()
        growing_tasks = self.db.get_growing_tasks()

        # --------------------
        # Fixed Tasks
        # --------------------

        for task in fixed_tasks:
            card = TaskCard(
                task_id=task["id"],
                title=task["title"],
                target=str(task["target"]),
                unit=task["unit"],
                completed=bool(task["completed_today"]),
                growth="",
                dashboard=self,
            )
            self.ids.fixed_container.add_widget(card)

        # --------------------
        # Growing Tasks
        # --------------------

        for task in growing_tasks:
            card = TaskCard(
                task_id=task["id"],
                title=task["title"],
                target=str(task["target"]),
                unit=task["unit"],
                completed=bool(task["completed_today"]),
                growth=f"+{task['growth_percent']} %",
                dashboard=self,
            )
            self.ids.growing_container.add_widget(card)

    def add_task(self):
        self.manager.current = "add_task"

    def delete_task(self, task_id):
        self.db.delete_task(task_id)
        self.load_tasks()

    def edit_task(self, task_id):
        task = self.db.get_task(task_id)
        add_screen = self.manager.get_screen("add_task")
        add_screen.load_task(task)
        self.manager.current = "add_task"

    def complete_task(self, task_id):
        completed = self.db.complete_task(task_id)
        if completed:
            self.load_tasks()
        self.load_tasks()

    def open_statistics(self):
        self.manager.current = "statistics"

    def open_alarm(self):
        self.manager.current = "alarm"

    def close(self):
        self.connection.close()