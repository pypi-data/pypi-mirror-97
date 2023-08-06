import logging

from nehushtan.logger.NehushtanFileLogger import NehushtanFileLogger

if __name__ == '__main__':
    file_logger = NehushtanFileLogger('test', '/Users/leqee/code/nehushtan/log', log_level=logging.INFO)

    file_logger.critical('C', {"A": "B"})
    file_logger.error('E', 111)
    file_logger.warning('W', 'dd')
    file_logger.info('I', file_logger)
    file_logger.debug('D')

    try:
        raise ValueError('A<>B')
    except Exception as error:
        file_logger.exception('X', error)
