from SSHLibrary import SSHLibrary

from ftsa.core.properties import VERSION
from robot.api import logger


class FTSASSHLibrary(SSHLibrary):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION

    def open_connection(self, host, username, keyfile, password, port=22, jump_host=None, prompt='#'):
        """*FTSA Opens a new SSH connection*

        FTSA opens a new SSH connection to the given ``host``, ``username``, ``keyfile`` and ``password``

        Default values applied:
        | port      | 22   |
        | jump_host | None |

        """
        logger.info(f'FTSA Full opens a new SSH connection with public key file "{keyfile}" for host "{host}" '
                    f'and username "{username}" in port "{port}"')
        super().open_connection(host=host, port=port, prompt=prompt)
        super().enable_ssh_logging(logfile='ssh.log')

        if keyfile is None:
            super().login(username=username, password=password)
        else:
            if jump_host is not None:
                super().login_with_public_key(username=username, keyfile=keyfile, password=password, jumphost_index_or_alias=jump_host)
            else:
                super().login_with_public_key(username=username, keyfile=keyfile, password=password)

