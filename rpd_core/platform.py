import os
from os import makedirs
from os import path


def check_dir(dir_path):
    """
    Ensures the existence of a directory at the specified path.

    This function takes a directory path as input and ensures that the directory
    exists. If the directory does not exist, it will be created. The function
    returns the absolute path of the directory.

    :param dir_path: A string specifying the directory path to check or create.
    :type dir_path: str
    :return: The absolute path of the directory.
    :rtype: str
    """
    dir_path = path.abspath(dir_path)
    if not path.isdir(dir_path):
        makedirs(dir_path)

    return dir_path


class PlatformServices:
    """
    Provides utility methods to manage directory paths for various purposes within
    the workspace of the system. Includes functionality for accessing input, output,
    temporary, logs, and data folder paths. This class helps in organizing and
    managing file paths efficiently.

    The class is designed to simplify directory creation and maintenance in a system
    environment by generating paths dynamically based on file or folder requirements.

    :ivar sys_root: Represents the root directory of the system.
    :type sys_root: Callable
    """

    @staticmethod
    def sys_root():
        return path.curdir

    def _int_folder_path(self, *args):
        """
        Builds and returns a validated directory path by combining the provided arguments.

        All arguments provided are concatenated into a single directory path relative to
        the system root. Only non-`None` arguments are used in constructing the path.
        The constructed path is then validated to ensure it meets the directory structure
        requirements.

        :param args: Variable arguments representing parts of the directory path. Any
            `None` values will be omitted.
        :return: The full validated directory path constructed by combining the provided
            non-`None` arguments.
        """
        return check_dir(
            path.join(self.sys_root(), *[arg for arg in args if arg is not None])
        )

    def fldr_inbox(self, file_name=None):
        return self._int_folder_path("_workspace", "in", file_name)

    def fldr_outbox(self, file_name=None):
        return self._int_folder_path("_workspace", "out", file_name)

    def fldr_temp(self, file_name=None):
        return self._int_folder_path("_workspace", "tmp", file_name)

    def fldr_logs(self, file_name=None):
        return self._int_folder_path("_workspace", "logs", file_name)

    def fldr_data(self, file_name=None):
        return self._int_folder_path("_workspace", "dat", file_name)

    def __init__(self):
        pass
