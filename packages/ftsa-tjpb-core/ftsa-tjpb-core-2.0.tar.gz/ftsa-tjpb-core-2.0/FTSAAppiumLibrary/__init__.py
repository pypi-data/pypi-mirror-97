from AppiumLibrary import AppiumLibrary

from ftsa.core.properties import VERSION
from robot.api import logger


class FTSAAppiumLibrary(AppiumLibrary):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION

    def __init__(self):
        AppiumLibrary.__init__(self)

    def open_application(self, remote_url='http://127.0.0.1:4723/wd/hub', alias=None, timeout='20s', **kwargs):
        """ FTSA OPENS MOBILE APP

        FTSA opens the ``mobile app`` in the remote server defined to ``remote_url``, none ``alias``, ``timeout`` of 20s
        and ``appium desired capabilities`` (See more)[https://github.com/appium/appium/blob/master/docs/en/writing-running-appium/caps.md].

        Default options used:

        | remote_url  | http://127.0.0.1:4723/wd/hub  |
        | alias       | None                          |
        | timeout     | 20s                           |

        """
        logger.info(f'FTSA opens the mobile app in remote server "{remote_url}", with alias "{alias}" and timeout of {timeout}')
        super().open_application(remote_url, alias=alias, **kwargs)
        super().set_appium_timeout(timeout)

    def close_all_applications(self):
        """ FTSA CLOSES MOBILE APP

        FTSA closes application and takes a screenshot from the screen.

        """
        logger.info('FTSA closes mobile app taking a screenshot')
        super().capture_page_screenshot()
        super().close_all_applications()
