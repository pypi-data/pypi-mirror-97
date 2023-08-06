import shutil

from nehushtan.logger.NehushtanFileLogger import NehushtanFileLogger
from tests.queue.plan2.Test2NehushtanQueue import Test2NehushtanQueue
from tests.queue.plan2.Test2NehushtanQueueDelegate import Test2NehushtanQueueDelegate

if __name__ == '__main__':
    shutil.rmtree('/Users/leqee/code/nehushtan/log/queue-plan2')

    config_dictionary = {}
    logger = NehushtanFileLogger('loop', '/Users/leqee/code/nehushtan/log/queue-plan2')
    delegate = Test2NehushtanQueueDelegate(config_dictionary, logger)

    Test2NehushtanQueue(delegate).loop()
