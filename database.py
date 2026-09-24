import sqlite3
from datetime import date, timedelta


class Database:

    def __init__(self):
        self.connection = sqlite3.connect("database/app.db")
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

        self.create_tables()
        self.add_timer_columns()
        self.initialize_settings()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                target REAL NOT NULL,
                unit TEXT,
                task_type TEXT,
                growth_percent REAL,
                completed_today INTEGER DEFAULT 0,
                created_at TEXT,

                timer_remaining INTEGER DEFAULT 0,
                timer_status TEXT DEFAULT 'idle',
                timer_started_at TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS task_history(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER NOT NULL,
                history_date TEXT NOT NULL,
                target REAL NOT NULL,
                completed INTEGER DEFAULT 0,
                completed_time TEXT,
                FOREIGN KEY(task_id)
                    REFERENCES tasks(id)

            )
            """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS app_settings(
                key TEXT PRIMARY KEY,
                value TEXT
            )
            """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS alarms(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alarm_type TEXT,
            alarm_time TEXT,
            message TEXT,
            enabled INTEGER
            )""")
        self.connection.commit()

    def add_task(self, title, target, unit, task_type, growth_percent, created_at):
        self.cursor.execute(
            """ INSERT INTO tasks (title, target, unit, task_type, growth_percent, created_at) VALUES (?, ?, ?, ?, ?, ?)""",
            (title, target, unit, task_type, growth_percent, created_at),
        )

        today = date.today().isoformat()
        task_id = self.cursor.lastrowid
        self.cursor.execute(
            "INSERT INTO task_history( task_id, history_date, target, completed) VALUES(?,?,?,?)",
            (task_id, today, target, 0),
        )
        self.connection.commit()

    def get_tasks(self):
        self.cursor.execute("SELECT * FROM tasks")
        return self.cursor.fetchall()

    def get_fixed_tasks(self):
        self.cursor.execute("""SELECT * FROM tasks WHERE task_type = 'fixed' """)
        return self.cursor.fetchall()

    def get_growing_tasks(self):
        self.cursor.execute("""SELECT * FROM tasks WHERE task_type = 'growing' """)
        return self.cursor.fetchall()

    def update_task(self, task_id, title, target, unit, task_type, growth_percent):
        self.cursor.execute(
            """UPDATE tasks SET title=?, target=?, unit=?, task_type=?, growth_percent=? WHERE id=?""",
            (title, target, unit, task_type, growth_percent, task_id),
        )
        self.connection.commit()

    def delete_task(self, id):
        self.cursor.execute("DELETE FROM task_history WHERE task_id=?", (id,))
        self.cursor.execute("DELETE FROM tasks WHERE id=?", (id,))
        self.connection.commit()

    def task_exists(self, title):
        self.cursor.execute("SELECT id FROM tasks WHERE title=?", (title,))
        return self.cursor.fetchone()

    def get_task(self, task_id):
        self.cursor.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
        return self.cursor.fetchone()

    def complete_task(self, task_id):

        task = self.get_task(task_id)
        if task["completed_today"] == 1:
            return False
        target = task["target"]
        growth = task["growth_percent"]
        task_type = task["task_type"]

        if task_type == "growing":
            new_target = round(target * (1 + growth / 100), 2)
            self.cursor.execute(
                "UPDATE tasks SET target=?, completed_today=1 WHERE id=?",
                (new_target, task_id),
            )
        else:
            self.cursor.execute(
                "UPDATE tasks SET completed_today=1 WHERE id=?", (task_id,)
            )

        today = date.today().isoformat()
        self.cursor.execute(
            "UPDATE task_history SET completed=1 WHERE task_id=? AND history_date=?",
            (task_id, today),
        )

        self.connection.commit()

    def initialize_settings(self):
        self.cursor.execute(
            "INSERT OR IGNORE INTO app_settings (key, value) VALUES ('last_reset', DATE('now'))"
        )
        self.connection.commit()

    def daily_reset(self):
        today = date.today().isoformat()
        self.cursor.execute(" SELECT value FROM app_settings WHERE key='last_reset' ")
        last_reset = self.cursor.fetchone()["value"]
        if last_reset == today:
            return
        self.cursor.execute(" UPDATE tasks SET completed_today = 0")
        self.cursor.execute(
            " UPDATE app_settings SET value=? WHERE key='last_reset' ", (today,)
        )

        tasks = self.get_tasks()
        for task in tasks:
            self.cursor.execute(
                "INSERT OR IGNORE INTO task_history(task_id, history_date, target, completed) VALUES(?,?,?,?)",
                (task["id"], today, task["target"], 0),
            )
        self.connection.commit()

    def get_statistics(self):
        statistics = {}
        self.cursor.execute("SELECT COUNT(*) FROM tasks")
        statistics["total_tasks"] = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT COUNT(*) FROM tasks WHERE task_type='fixed' ")
        statistics["fixed_tasks"] = self.cursor.fetchone()[0]
        self.cursor.execute(" SELECT COUNT(*) FROM tasks WHERE task_type='growing' ")
        statistics["growing_tasks"] = self.cursor.fetchone()[0]
        self.cursor.execute(" SELECT COUNT(*) FROM tasks WHERE completed_today=1")
        statistics["completed_today"] = self.cursor.fetchone()[0]
        self.cursor.execute(" SELECT COUNT(*) FROM task_history WHERE completed = 1")
        statistics["total_completed"] = self.cursor.fetchone()[0]
        statistics["current_streak"] = self.get_current_streak()
        statistics["best_streak"] = self.get_best_streak()

        if statistics["total_tasks"] == 0:
            statistics["progress"] = 0
        else:
            statistics["progress"] = round(
                statistics["completed_today"] / statistics["total_tasks"] * 100, 1
            )

        return statistics

    def get_current_streak(self):
        self.cursor.execute("""
        SELECT history_date FROM task_history GROUP BY history_date HAVING COUNT(*) = SUM(completed)ORDER BY
          history_date DESC
        """)
        rows = self.cursor.fetchall()

        if not rows:
            return 0
        completed_dates = {
            row["history_date"] for row in rows
        }

        today = date.today()
        yesterday = today - timedelta(days=1)
        today_completed = today.isoformat() in completed_dates

        streak = 0
        current = yesterday

        while current.isoformat() in completed_dates:
            streak += 1
            current -= timedelta(days=1)
        if today_completed:
            streak += 1

        return streak

    def get_best_streak(self):
        self.cursor.execute("""
            SELECT history_date FROM task_history GROUP BY history_date HAVING COUNT(*) = SUM(completed) ORDER BY history_date
        """)
        rows = self.cursor.fetchall()

        if not rows:
            return 0
        dates = [date.fromisoformat(row["history_date"]) for row in rows]
        best = 1
        current = 1

        for i in range(1, len(dates)):
            if dates[i] == dates[i - 1] + timedelta(days=1):
                current += 1
                best = max(best, current)
            else:
                current = 1

        return best

    def create_daily_history(self):
        today = date.today().isoformat()
        tasks = self.get_tasks()

        for task in tasks:
            self.cursor.execute("SELECT id FROM task_history WHERE task_id=? AND history_date=?",
                (task["id"], today),)
            exists = self.cursor.fetchone()

            if exists:
                continue
            self.cursor.execute("INSERT INTO task_history (task_id, history_date, target, completed) VALUES(?,?,?,0)",
                (task["id"], today, task["target"]),)
        self.connection.commit()

    def add_timer_columns(self):
        columns = [
            ("timer_remaining", "INTEGER DEFAULT 0"),
            ("timer_status", "TEXT DEFAULT 'idle'"),
            ("timer_started_at", "TEXT")
        ]

        for column, definition in columns:
            try:
                self.cursor.execute(
                    f"ALTER TABLE tasks ADD COLUMN {column} {definition}"
                )
            except sqlite3.OperationalError:
                pass

        self.connection.commit()

    def save_timer(self, task_id, remaining_seconds, status):
        self.cursor.execute("UPDATE tasks SET timer_remaining=?, timer_status=? WHERE id=?",
            (remaining_seconds, status, task_id))
        self.connection.commit()

    def get_timer(self, task_id):
        self.cursor.execute("SELECT timer_remaining, timer_status, timer_started_at FROM tasks WHERE id=?", (task_id,))
        return self.cursor.fetchone()

    def reset_timer(self, task_id):
        self.cursor.execute("UPDATE tasks SET timer_remaining=0, timer_status='idle', timer_started_at=NULL WHERE id=?",
            (task_id,))
        self.connection.commit()

    def add_alarm(self, alarm_type, alarm_time, message, enabled):
        self.cursor.execute(
            """INSERT INTO alarms(alarm_type, alarm_time, message, enabled) VALUES (?, ?, ?, ?)""",
            (alarm_type, alarm_time, message, enabled),
        )
        self.connection.commit()

    def get_alarms(self):
        self.cursor.execute("SELECT * FROM alarms")
        return self.cursor.fetchall()

    def delete_alarm(self, alarm_id):
        self.cursor.execute("DELETE FROM alarms WHERE id = ?", (alarm_id,))
        self.connection.commit()

    def update_alarm_enabled(self, alarm_id, enabled):
        self.cursor.execute("UPDATE alarms SET enabled = ? WHERE id = ?", (enabled, alarm_id))
        self.connection.commit()