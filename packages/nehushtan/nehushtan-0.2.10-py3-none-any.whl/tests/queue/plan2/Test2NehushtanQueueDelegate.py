import time
from random import random

from nehushtan.logger.NehushtanFileLogger import NehushtanFileLogger
from nehushtan.queue.NehushtanQueueDelegate import NehushtanQueueDelegate
from nehushtan.queue.NehushtanQueueTask import NehushtanQueueTask
from nehushtan.queue.situation.NoNextTaskSituation import NoNextTaskSituation
from tests.queue.plan2.Test2NehushtanQueueTask import Test2NehushtanQueueTask


class Test2NehushtanQueueDelegate(NehushtanQueueDelegate):

    def __init__(self, config_dictionary: dict = None, logger: NehushtanFileLogger = None):
        super().__init__(config_dictionary, logger)
        self.last_task_id = 1000

    def when_loop_reports_error(self, error_message: str):
        self.logger.error('Test2NehushtanQueueDelegate when_loop_reports_error', error_message)

    def when_loop_terminates(self):
        self.logger.critical('Test2NehushtanQueueDelegate when_loop_terminates')

    def when_loop_should_not_run(self):
        self.logger.warning('Test2NehushtanQueueDelegate when_loop_should_not_run sleep 10')
        time.sleep(10)

    def check_next_task(self) -> NehushtanQueueTask:
        self.logger.info('Test2NehushtanQueueDelegate check_next_task')
        if random() > 0.7:
            self.last_task_id += 1
            self.logger.info('Test2NehushtanQueueDelegate check_next_task -> create new task')
            return Test2NehushtanQueueTask(task_id=self.last_task_id)
        else:
            raise NoNextTaskSituation('No task to execute')

    def when_no_task_to_do(self):
        self.logger.info('Test2NehushtanQueueDelegate when_no_task_to_do sleep 5')
        time.sleep(5)

    def when_task_not_executable(self, task: NehushtanQueueTask):
        self.logger.info('Test2NehushtanQueueDelegate when_task_not_executable', {'task_id': task.get_task_reference()})

    def when_to_execute_task(self, task: NehushtanQueueTask, pid: int):
        self.logger.info(
            'Test2NehushtanQueueDelegate when_to_execute_task',
            {'task_id': task.get_task_reference(), 'pid': pid}
        )

    def when_task_executed(self, task: NehushtanQueueTask, pid: int):
        self.logger.info(
            'Test2NehushtanQueueDelegate when_task_executed',
            {'task_id': task.get_task_reference(), 'pid': pid}
        )

    def when_task_raised_exception(self, task: NehushtanQueueTask, exception: Exception):
        self.logger.exception(
            f'Test2NehushtanQueueDelegate when_task_raised_exception task_id={task.get_task_reference()}',
            exception
        )
