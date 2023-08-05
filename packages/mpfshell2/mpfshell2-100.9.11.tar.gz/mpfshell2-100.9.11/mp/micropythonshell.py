import os
import re
import sys
import time
import pathlib
import hashlib
import logging
import argparse

import mp
import mp.mpfshell
import serial.tools.list_ports


DIRECTORY_OF_THIS_FILE = pathlib.Path(__file__).absolute().parent

FILENAME_IDENTIFICATION = 'config_identification.py'

FILES_TO_SKIP=('boot.py', 'pybcdc.inf', 'README.txt', FILENAME_IDENTIFICATION)

class MicropythonShell:
    def __init__(self, str_port=None):
        # Speed up file transfers
        mp.mpfshell.MpFileExplorer.BIN_CHUNK_SIZE = 512

        if str_port is not None:
            print(f'Using {str_port}')
        else:
            str_port = MicropythonShell.get_first_port()
            print(f'Found {str_port}')
        if re.match(r'^COM\d+$', str_port) is None:
           raise Exception('Expected a string like "COM5", but got "{}"'.format(str_port))
        self.str_port = str_port

        self.__open()

    def __open(self):
        self.MpFileShell = mp.mpfshell.MpFileShell(color=False, caching=False, reset=False)
        self.MpFileShell.do_open(args=f'ser:{self.str_port}')
        if not self.is_connected:
            raise Exception(f'Failed to open "{self.str_port}"')

    @property
    def MpFileExplorer(self) -> mp.mpfshell.MpFileExplorer:
        assert self.MpFileShell is not None
        return self.MpFileShell.fe

    @classmethod
    def get_first_port(cls):
        def is_pyboard(port):
            try:
                return (port.vid == 0xF055) and (port.pid == 0x9800)
            except AttributeError: # port.vid or port.pid not defined
                return False
        list_ports = serial.tools.list_ports.comports()
        list_ports = [port for port in list_ports if is_pyboard(port)]
        if len(list_ports) == 0:
            raise Exception('No serial interface found!')
        if len(list_ports) > 1:
            print('More than one serial interface connected. Will use the first one!')
            MicropythonShell.list_ports(list_ports)
        return list_ports[0].device

    @classmethod
    def list_ports(cls, list_ports):
        for port in list_ports:
            print(f'  {port.device} pid=0x{port.pid:X} vid=0x{port.vid:X} description={port.description}')

    @property
    def is_connected(self):
        return self.MpFileShell is not None

    def soft_reset(self):
        assert self.is_connected

        self.MpFileExplorer.con.write(b"\x04")  # ctrl-D: soft reset
        data = self.MpFileExplorer.read_until(1, b"soft reboot\r\n")
        if data.endswith(b"soft reboot\r\n"):
            return
        raise Exception("could not do soft reset")

    def machine_reset(self):
        assert self.is_connected
        print('performing "machine.reset()" This will reconnect the usb on your pc')
        self.MpFileExplorer.exec_('import machine')
        try:
            self.MpFileExplorer.exec_('machine.reset()')
        except serial.serialutil.SerialException as _e:
            time.sleep(0.5)
            self.__open()
            return
        raise Exception('Reboot did not occur!')

    def __get_hash_local(self, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return hashlib.sha256(data).hexdigest()

    def __up_listfiles_remote(self):
        file_to_exec = DIRECTORY_OF_THIS_FILE.joinpath('micropythonshell_up_listfiles.py')
        self.MpFileExplorer.execfile(file_to_exec)
        files = self.MpFileExplorer.eval('up_listfiles()')
        files = eval(files)
        return files

    def __do_folder_diff(self, directory_local, FILES_TO_SKIP):
        '''
        Compare the remote and local directory listing, compare the sha256.
        '''
        assert isinstance(directory_local, pathlib.Path)
        files_to_delete = set()
        files_to_download = set([f.name for f in directory_local.glob('*') if f.is_file()])

        files = self.__up_listfiles_remote()
        for filename_remote, sha256_remote in files:
            sha256_remote = sha256_remote.decode('utf-8')
            # print(f'  {sha256_remote}: {filename_remote}')
            filename_local = pathlib.Path(directory_local).joinpath(filename_remote)
            if not filename_local.exists():
                if FILES_TO_SKIP is None:
                    continue
                if filename_remote in FILES_TO_SKIP:
                    continue
                files_to_delete.add(filename_remote)
                continue
            sha256_local = self.__get_hash_local(filename_local)
            if sha256_remote == sha256_local:
                # File equal
                files_to_download.remove(filename_remote)
                continue

        return files_to_delete, files_to_download

    def sync_folder(self, directory_local, FILES_TO_SKIP=FILES_TO_SKIP):
        '''
        Update the pyboard filesystem according to 'directory_local'.
        If FILES_TO_SKIP is a list, all these files will not be deleted.
        If FILES_TO_SKIP is None, no files will be deleted at all.
        '''
        assert self.is_connected
        assert isinstance(FILES_TO_SKIP, (list, tuple, type(None)))
        if isinstance(directory_local, str):
            directory_local = pathlib.Path(directory_local)

        if not directory_local.exists():
            print(f'Directory "{directory_local}" does not exist and will not be replicated!')
            return

        files_to_delete, files_to_download = self.__do_folder_diff(directory_local, FILES_TO_SKIP)
        
        for file_to_download in files_to_download:
            filename_local = f'{directory_local}/{file_to_download}'
            print(f'  downloading: {file_to_download}')
            self.MpFileExplorer.put(src=filename_local, dst=file_to_download)
        
        for file_to_delete in files_to_delete:
            print(f'  delete {file_to_delete}')
            self.MpFileExplorer.rm(file_to_delete)

        if (len(files_to_delete) == 0) and (len(files_to_download) == 0):
            print(f'  Directory "{directory_local}": already synchronized')
            return

        print(f'  soft reset (filessystem was touched, modules must be reloaded)')
        self.soft_reset()

        files_to_delete, files_to_download = self.__do_folder_diff(directory_local, FILES_TO_SKIP)
        if (len(files_to_delete) > 0) or (len(files_to_download) > 0):
            print(f'  Transmission error! files_to_delete={files_to_delete}, files_to_download={files_to_download}')

    def repl(self, start_main=False, args=None):
        assert self.is_connected
        self.MpFileShell.do_repl(start_main=start_main, args=args)

    def close(self):
        if not self.is_connected:
            return
        self.MpFileShell.do_close(args=None)
        self.MpFileShell = None


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--loglevel",
        help="loglevel (CRITICAL, ERROR, WARNING, INFO, DEBUG)",
        default="ERROR",
    )
    parser.add_argument(
        "port", help="specify serial port, for example COM12", nargs="?", action="store", default=None
    )
    parser.add_argument(
        "--no_main",
        help="does not run 'main.py' (it may be started later by pressing <ctrl-D>)",
        action="store_true",
        default=False,
    )

    args = parser.parse_args()

    format = "%(asctime)s\t%(levelname)s\t%(message)s"

    logging.basicConfig(format=format, level=args.loglevel)

    logging.info("Micropython File Shell v%s started" % mp.version.FULL)
    logging.info(
        "Running on Python %d.%d using PySerial %s"
        % (sys.version_info[0], sys.version_info[1], serial.VERSION)
    )

    r = MicropythonShell(str_port=args.port)
    r.sync_folder(directory_local='micropython')
    r.repl(start_main=not args.no_main)
    r.close()

def test():
    r = MicropythonShell()
    r.sync_folder(directory_local='micropython')
    r.soft_reset()
    r.machine_reset()
    r.repl()
    r.close()

if __name__ == "__main__":
    main()