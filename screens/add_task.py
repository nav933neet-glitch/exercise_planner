from datetime import datetime

from kivy.uix.screenmanager import Screen

from database import Database


class AddTaskScreen(Screen):

    db = Database()
    editing = False
    editing_task_id = None

    def load_task(self, task):

        self.editing = True
        self.editing_task_id = task["id"]
        self.ids.task_name.text = task["title"]
        self.ids.target.text = str(task["target"])
        self.ids.unit.text = task["unit"]
        self.ids.task_type.text = task["task_type"]
        self.ids.growth.text = str(task["growth_percent"])

    def save_task(self):

        title = self.ids.task_name.text.strip()
        target = self.ids.target.text.strip()
        unit = self.ids.unit.text.strip()
        task_type = self.ids.task_type.text
        growth = self.ids.growth.text.strip()

        # -------------------------
        # Validation
        # -------------------------

        if title == "":
            return

        if target == "":
            return

        if not self.editing:
            if self.db.task_exists(title):
                return

        if growth == "":
            growth = 0

        if self.editing:
            self.db.update_task(
                self.editing_task_id,
                title,
                float(target),
                unit,
                task_type,
                float(growth),
            )
        else:
            self.db.add_task(
                title,
                float(target),
                unit,
                task_type,
                float(growth),
                datetime.now().strftime("%Y-%m-%d"),
            )

        self.clear_fields()
        self.manager.current = "dashboard"
        self.editing = False
        self.editing_task_id = None

    def clear_fields(self):
        self.editing = False
        self.editing_task_id = None
        self.ids.task_name.text = ""
        self.ids.target.text = ""
        self.ids.unit.text = ""
        self.ids.growth.text = ""
        self.ids.task_type.text = "fixed"

    def go_back(self):
        self.clear_fields()
        self.manager.current = "dashboard"
