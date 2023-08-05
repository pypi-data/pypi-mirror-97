from RequestsLibrary import RequestsLibrary


from ftsa.core.properties import VERSION
from robot.api import logger


class FTSARequestsLibrary(RequestsLibrary):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION

    def __init__(self):
        logger.info('[FTSARequestsLibrary] Initialized.')
        RequestsLibrary.__init__(self)
