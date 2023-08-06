import json
import os
import sys
import threading
import time
import traceback

import psutil

from nehushtan.logger.NehushtanLogging import NehushtanLogging


class NehushtanFileLogger:
    """
    @since 0.1.25
    Another solution for logging, just use raw writing method to target file.
    """

    def __init__(
            self,
            title='default',
            log_dir: str = None,
            log_level=NehushtanLogging.DEBUG,
            categorize: bool = True,
            date_rotate: bool = True,
            print_higher_than_this_level=NehushtanLogging.CRITICAL
    ):
        self.title = title
        self.log_dir = log_dir
        self.log_level = log_level
        self.categorize = categorize
        self.date_rotate = date_rotate
        # self.print_as_well = print_as_well <-- should use print_higher_than_this_level=NehushtanLogging.NOTSET
        # If all, use NOTSET; if none, use FATAL
        if print_higher_than_this_level is True:
            self.print_higher_than_this_level = NehushtanLogging.NOTSET
        elif print_higher_than_this_level is False:
            self.print_higher_than_this_level = NehushtanLogging.CRITICAL
        else:
            self.print_higher_than_this_level = print_higher_than_this_level

    def get_target_file(self):
        if self.log_dir is None:
            return ''

        category_dir = self.log_dir

        if self.categorize:
            category_dir = os.path.join(self.log_dir, self.title)

        if not os.path.exists(category_dir):
            os.makedirs(category_dir)

        today = ''
        if self.date_rotate:
            today = time.strftime("%Y%m%d", time.localtime())
            today = f'-{today}'

        target_file = os.path.join(category_dir, f'{self.title}{today}.log')
        return target_file

    def write_raw_line_to_log(self, text: str, level: int = NehushtanLogging.INFO, end=os.linesep):
        """
        Parameter `level` is only used to determine stdout or stderr when file empty.
        Since 0.2.8, Parameter `end` added.
        """
        target_file = self.get_target_file()

        if target_file != '':
            file = open(target_file, 'a')
            file.write(text + end)
            file.flush()
            file.close()

        if target_file == '' or level > self.print_higher_than_this_level:
            if level >= NehushtanLogging.WARNING:
                print(text, file=sys.stderr, end=end)
            else:
                print(text, end=end)

        return self

    @staticmethod
    def get_level_label(level: int):
        return NehushtanLogging.get_label_of_level(level)

    def write_formatted_line_to_log(self, level: int, message: str, extra=None):
        if level < self.log_level:
            return self
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        level_label = NehushtanFileLogger.get_level_label(level)
        pid = os.getpid()
        thread = threading.currentThread()
        extra_json = self.ensure_extra_as_dict(extra)
        line = f'{now} <{self.title}> [{level_label}] <{pid}:{thread.getName()}> {message} | {extra_json}'
        return self.write_raw_line_to_log(line, level)

    def debug(self, message: str, extra=None):
        return self.write_formatted_line_to_log(NehushtanLogging.DEBUG, message, extra)

    def info(self, message: str, extra=None):
        return self.write_formatted_line_to_log(NehushtanLogging.INFO, message, extra)

    def notice(self, message: str, extra=None):
        return self.write_formatted_line_to_log(NehushtanLogging.NOTICE, message, extra)

    def warning(self, message: str, extra=None):
        return self.write_formatted_line_to_log(NehushtanLogging.WARNING, message, extra)

    def error(self, message: str, extra=None):
        return self.write_formatted_line_to_log(NehushtanLogging.ERROR, message, extra)

    def exception(self, message: str, exception: BaseException):
        just_the_string = ''.join(
            traceback.format_exception(
                etype=type(exception),
                value=exception,
                tb=exception.__traceback__
            )
        )
        return self.write_formatted_line_to_log(NehushtanLogging.ERROR, message, f'{type(exception).__name__}') \
            .write_raw_line_to_log(just_the_string, NehushtanLogging.ERROR)

    def critical(self, message: str, extra=None):
        return self.write_formatted_line_to_log(NehushtanLogging.CRITICAL, message, extra)

    def log_current_memory_usage_of_process(self, pid: int = None, level: int = NehushtanLogging.INFO):
        """
        Since 0.2.10
        Filed `pid` would use os.getpid() for None.
        """
        memory_usage = psutil.Process(pid=pid).memory_info()
        self.write_formatted_line_to_log(
            level,
            'Current Memory Usage Snapshot (in MB)',
            {'rss': memory_usage.rss/1024.0/1024.0, 'vms': memory_usage.vms/1024.0/1024.0}
        )

    def log_current_memory_usage_of_object(self, target_name: str, target, level: int = NehushtanLogging.INFO):
        """
        Since 0.2.10
        """
        memory_usage = sys.getsizeof(target)
        self.write_formatted_line_to_log(
            level,
            f'Current Memory Usage used by {target_name} (in MB)',
            memory_usage/1024.0/1024.0
        )

    @staticmethod
    def ensure_extra_as_dict(extra):
        """
        Since 0.1.25, add ensure_ascii as False to allow unicode chars
        """
        return json.dumps(extra, default=lambda inner_x: inner_x.__str__(), ensure_ascii=False)
