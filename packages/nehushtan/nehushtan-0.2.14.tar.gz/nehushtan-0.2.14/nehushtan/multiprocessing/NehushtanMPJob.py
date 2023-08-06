from abc import abstractmethod

from nehushtan.logger.NehushtanFileLogger import NehushtanFileLogger


class NehushtanMPJob:
    """
    Since 0.2.13
    """

    def __init__(self, name: str, logger: NehushtanFileLogger):
        """
        Override this and extend the parameters
        """
        self.__name = name
        self.__logger = logger
        self.__pid = 0

    def get_name(self):
        return self.__name

    def get_logger(self):
        return self.__logger

    def set_pid(self, pid: int):
        self.__pid = pid
        return self

    def get_pid(self):
        return self.__pid

    @abstractmethod
    def handle(self):
        """
        Run in sub process
        """
        pass

    def when_exited(self, exit_code: int):
        """
        Run in main process
        It is called when main process found worker process exited
        """
        pass
