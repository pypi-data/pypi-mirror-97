from dataclasses       import dataclass, field
from pathlib           import Path
from typing            import Any
import os, sys, shutil, signal, atexit
from storer.compressor import compressor

@dataclass
class Storer:
    __version__ = "1.0.7 [57]"
    internal_name:  str  = "[Storer]"
    dump_name:      str  = "noname"
    dump_path:      str  = Path(os.path.expanduser(os.path.dirname(__file__)))
    verbose:        bool = False
    data:           dict = field(default_factory=dict)
    default_dir:    str  = "data"
    compressed:     bool = True
    separations:    int  = int(1e6)
    _backup_dir:    str  = "backup"
    backup_list:    list = field(default_factory=list)
    _put_counter:   int  = 0
    _dump_counter:  int  = 0
    _dump_name:     str  = None
    _extension:     str  = None
    _test:          bool = False

    def __post_init__(self):
        if self.verbose: print(f"[Storer v.{self.__version__ }] is initialized!")
        self._dump_name = self.dump_name
        if self.dump_path == Path(os.path.expanduser(os.path.dirname(__file__))) or self.dump_path == "." :
            self.dump_path = Path(os.path.expanduser(os.path.dirname(__file__))) / "data"
        else:
            self.dump_path = Path(os.path.expanduser(self.dump_path))

        if self.verbose: print(f"Dump folder: [{self.dump_path}]")
        os.makedirs(self.dump_path, exist_ok=True)
        self._extension = ".pbz2" if self.compressed else ".pkl"
        self._initialization()  # creating _backup_list
        self.compressor = compressor.Compressor(compressed = self.compressed,
                                                dump_path  = self.dump_path,
                                                dump_name  = self.dump_name)
        if not self._test: atexit.register(self.dump)

    def _exit(self, signum, frame):
        self.dump()
        sys.exit(0)

    def _cleanup(self) -> None:
        """
        Cleanup the dump_path directory fully: including all folders and files.
        Assuming the folder is used only for Storer purposes.
        """
        if self.verbose: print(f"Cleaning...[{self.dump_path}]")
        shutil.rmtree(self.dump_path)

    def _get_priv_dump_name(self) -> None:
        self.dump_name      = self._dump_name + "_" + str(self._dump_counter)
        self._dump_counter -= 1
        if self._dump_counter < 0: self._dump_counter = 0

    def _get_next_dump_name(self) -> None:
        self.dump_name      = self._dump_name + "_" + str(self._dump_counter)
        self._dump_counter += 1

    def _initialization(self) -> None:
        """
        Internal needs.
        """
        signal.signal(signal.SIGINT, self._exit)
        _backup_list = [p for p in self.dump_path.iterdir() if p.is_file() and str(p).endswith((".pkl", "gzip", "bz2", "lzma"))]
        for path_fname in _backup_list: self.backup_list.append(str(path_fname.name).split(self._extension)[0])

        if self.verbose:
            if len(self.backup_list):
                print(f"{self.internal_name} [BACKUPS] Found: ")
                for path_fname in self.backup_list: print(f"    --> {path_fname}")
            else: print(f"{self.internal_name} No data is available for loading...")

        if len(self.backup_list) == 0: self.backup_list.append(self.dump_name)
        self.backup_list.sort()

    def put(self, what=None, name: str = None) -> None:
        """
        Put an element to internal field of data
        """
        self.data[name]   = what
        self._put_counter+=1
        if self._put_counter >= self.separations:
            self.dump(_next_dump_name=True)
            self._get_next_dump_name()
            self._put_counter   = 0

    def get(self, name: str = None) -> Any:
        """
        Get an item from dump[s]
        """
        if name in self.data: return self.data[name]
        for dump_name in self.backup_list:
            data = self._load(dump_name=str(dump_name))
            if name in data: self.data = data; return data[name]
        return False

    def dump(self, backup:bool = False, _next_dump_name:bool = False) -> None:
        """
        Create a dump.

        Typical usage: dump()
        """
        if backup: dump_path = self.dump_path / self._backup_dir
        else:      dump_path = self.dump_path

        if self.data:
            if self.verbose: print(f"{self.internal_name} Path:{self.dump_path} Name:{self.dump_name} dumping...")
            self.compressor.dump(dump_path=dump_path, dump_name=self.dump_name, data=self.data)
            if backup or _next_dump_name: self.data = dict()

    def _load(self, dump_name:str = None) -> dict:
        """
        Internal needs.
        """
        if not dump_name: dump_name = self.dump_name
        data = self.compressor.load(dump_path=self.dump_path, dump_name=dump_name)
        return data

    def show(self, get_string = False) -> Any:
        """
        The show method: will show what currently is in the internal data
        """
        string = ""
        for name in self.data:
            string += "key: {0:10} | value:  {1:4}; ".format(name, str(self.data[name]))
        if get_string: return string
        else: print(string)

    def backup(self) -> None:
        """
        Backuping the current dump_name in separate folder [<dump_path> / backup ]
        """
        if self.verbose: print(f"Backup...")
        os.makedirs(self.dump_path / self._backup_dir, exist_ok=True)
        self.dump(backup=True)
