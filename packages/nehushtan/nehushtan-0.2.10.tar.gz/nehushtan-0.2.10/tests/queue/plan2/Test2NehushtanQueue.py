from nehushtan.queue.NehushtanQueue import NehushtanQueue
from nehushtan.queue.NehushtanQueueDelegate import NehushtanQueueDelegate


class Test2NehushtanQueue(NehushtanQueue):
    def __init__(self, delegate: NehushtanQueueDelegate):
        super().__init__(delegate)
