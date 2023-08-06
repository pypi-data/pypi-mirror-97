import logging
import sys

from nehushtan.helper.CommonHelper import CommonHelper

logger_class = CommonHelper.class_with_class_path('nehushtan.logger.NehushtanLogger', 'NehushtanLogger')
logger = logger_class('test-for-autoload', [logging.StreamHandler(stream=sys.stdout)])
logger.info('miao')
