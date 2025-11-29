import os
from os import makedirs
from os import path


def check_dir(dir_path):
    dir_path = path.abspath(dir_path)
    if not path.isdir(dir_path):
        makedirs(dir_path)

    return dir_path


class PlatformServices:
    @staticmethod
    def sys_root():
        return path.curdir

    def _int_folder_path(self, *args):
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
