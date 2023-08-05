import datetime
import time

import requests
from win10toast import ToastNotifier


class NotionToaster:
    def __init__(self, tasks_server, notion_token, delta_minutes=15):
        self.tasks_server = tasks_server
        self.notion_token = notion_token
        self.delta_minutes = delta_minutes
        self.toaster = ToastNotifier()
        self.today_tasks = {}

    def _get_today_tasks(self, base_url, token):
        today = datetime.date.today()
        response = requests.get(base_url + "/tasks?due=" + str(today), headers={'Notion-Token': token})
        return response.json()

    def _filter_near_tasks(self, tasks):
        now = datetime.datetime.now()
        near_tasks = []

        for task in tasks:
            task_due = datetime.datetime.strptime(task["due"], "%Y-%m-%dT%H:%M:%S")
            if abs((task_due - now).total_seconds() / 60) < self.delta_minutes:
                near_tasks.append(task)

        return near_tasks

    def _toast(self, task):
        try:
            task["project"]
        except KeyError:
            task["project"] = ''

        self.toaster.show_toast(task["name"],
                           " ".join([task["project"], task["due"][11:16]]),
                           icon_path=None,
                           duration=10,
                           threaded=True)

        # Wait for threaded notification to finish
        while self.toaster.notification_active():
            time.sleep(0.1)

    def run(self):
        self.today_tasks = self._get_today_tasks(self.tasks_server, self.notion_token)
        near_tasks = self._filter_near_tasks(self.today_tasks)

        for task in near_tasks:
            self._toast(task)

        # Wait for threaded notification to finish
        while self.toaster.notification_active():
            time.sleep(0.1)
