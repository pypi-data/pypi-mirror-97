import os
import logging

logging.basicConfig(level=os.getenv('DEEPOMATIC_LOG_LEVEL', 'INFO'),
                    format='[%(levelname)s %(name)s %(asctime)s %(process)d %(thread)d %(filename)s:%(lineno)s] %(message)s')
