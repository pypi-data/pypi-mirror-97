import os
import time
import sys


class Instance(object):

    def __init__(self, path, backup, max_byte, debug, dir_mod=0o777):
        self.path = path
        self.backup = backup
        self.max_byte = max_byte
        self.debug = debug
        self.dir_mod = dir_mod

    def bytestr_to_size(self, byte_str):
        unit_map = {
            "k": 1024,
            "m": 1024 * 1024,
            "g": 1024 * 1024 * 1024
        }
        last_elment = byte_str[-1]
        unit = 1

        if last_elment in unit_map:
            byte_str = byte_str[:-1]
            unit = unit_map[last_elment]
        return int(byte_str) * unit

    def size_pretty(self, size):
        unit_list = ['k', 'm', 'g']
        unit = ''
        unit_index = -1
        while size > 1024:
            size = size // 1024
            unit_index += 1
            unit = unit_list[unit_index]
        return '{}{}'.format(size, unit)

    def create_path_dir_if_not_exists(self):
        dir_name = os.path.dirname(self.path)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name, self.dir_mod)

    def get_path_size(self, path):
        if not os.path.exists(path):
            return 0
        st = os.stat(path)
        return st.st_size

    def loop(self, interval=0.1):
        self.create_path_dir_if_not_exists()
        max_size_int = self.bytestr_to_size(self.max_byte)
        path_file = open(self.path, 'a', encoding='utf-8')
        # while 1:
            # read_str = sys.stdin.read()
        for read_str in sys.stdin:
            if read_str:
                sys.stdout.write(read_str)
                sys.stdout.flush()
                path_size = self.get_path_size(self.path)

                self.log_debug_message("max_size_pretty:{}, path_size_pretty:{}".format(self.max_byte, self.size_pretty(path_size)))
                if path_size > max_size_int:
                    self.backup_path(self.path)
                path_file.close()
                path_file = open(self.path, 'a', encoding='utf-8')
                path_file.write(read_str)
            # time.sleep(interval)

    def backup_path(self, path):
        path_list = [
            path,

        ]
        for i in range(1, self.backup + 1):
            path_list.append(
                "{}.{}".format(path, i)
            )
        n = len(path_list)
        for i in range(n - 2, -1, -1):
            src_path = path_list[i]
            dest_path = path_list[i + 1]
            message = "try backup path {}->{}".format(src_path, dest_path)
            self.log_debug_message(message)
            if os.path.exists(src_path):
                os.rename(src_path, dest_path)

    def log_debug_message(self, message):
        if self.debug:
            if not message.startswith(os.linesep):
                message = os.linesep + message
            if not message.endswith(os.linesep):
                message += os.linesep
            sys.stdout.write(message)
