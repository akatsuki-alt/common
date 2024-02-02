from datetime import datetime, timedelta
from typing import List

from .database.objects import DBTask
from .logging import get_logger
from .utils import Schedule
from .app import database

import common.app as app
import threading
import time

class Task:
    
    def __init__(self, task_name: str) -> None:
        self.task_name = task_name

    def can_run(self) -> bool:
        return False
    
    def run(self) -> bool:
        return False
    
class RepeatedTask(Task):
    
    def __init__(self, task_name: str, interval: int) -> None:
        super().__init__(task_name)
        self.interval = interval
        
    def can_run(self) -> bool:
        with database.session as session:
            if (task := session.get(DBTask, self.task_name)):
                return (datetime.now() - task.last_run) >= timedelta(seconds=self.interval)
        return True

class ScheduledTask(Task):
    
    def __init__(self, task_name: str, time: Schedule) -> None:
        super().__init__(task_name)
        self.time = time
    
    def can_run(self) -> bool:
        with database.session as session:
            if (task := session.get(DBTask, self.task_name)):
                if (datetime.now() - task.last_run) <= timedelta(hours=23):
                    return False
        # 1 hour grace period
        return abs(self.time.current_delta()).seconds <= 3600

class Service:
    
    def __init__(self, service_name, daemonize=False) -> None:
        self.service_name = service_name
        self.daemonize = daemonize
        self.thread = threading.Thread(target=self.run, name=service_name, daemon=self.daemonize)
        self.logger = get_logger(service_name)

    def run(self):
        pass

class TaskedService(Service):
    
    def __init__(self, service_name, tasks: List[Task], daemonize=False) -> None:
        super().__init__(service_name, daemonize)
        self.tasks = tasks

    def can_run(self) -> bool:
        for task in self.tasks:
            if task.can_run():
                return True
        return False
    
    def run(self):
        while True:
            for task in self.tasks:
                if app.STOPPED:
                    return False
                if task.can_run():
                    self.logger.info(f'Starting task {task.task_name}')
                    start = datetime.now()
                    if not task.run():
                        self.logger.error(f'Failed to run task {task.task_name}!')
                    else:
                        with database.session as session:
                            if (dbtask := session.get(DBTask, task.task_name)):
                                task.last_run = datetime.now()
                            else:
                                dbtask = DBTask(name=task.task_name, last_run=datetime.now())
                                session.add(dbtask)
                            session.commit()
                    self.logger.info(f"Task {task.task_name} took {datetime.now() - start}.")
            time.sleep(1)