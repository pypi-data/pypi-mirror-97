import os
from dataclasses import dataclass
from pathlib     import Path
from enum        import Enum

import pickle
import bz2
import lzma
import gzip
import io
import time

class Algorithm(Enum):
    gzip = "gzip"
    bz2  = "bz2"
    lzma = "lzma"
    lz4   = ""

_file_algorithm_mapper = {
    Algorithm.gzip: [gzip.GzipFile, ".pgz"],
    Algorithm.bz2:  [bz2.BZ2File,   ".pbz2"],
    Algorithm.lzma: [lzma.LZMAFile, ".xz"],
}

@dataclass
class Compressor:
    __version__ = "0.0.3 [3]"
    compressed: bool = True
    algorithm : Algorithm = Algorithm.bz2
    dump_path : str        = Path(os.path.expanduser(os.path.dirname(__file__)))
    dump_name : str        = "noname"

    def _use(self, algorithm: Algorithm) -> None:
        self.algorithm = algorithm 

    def dump(self, dump_path:Path, dump_name:str, data:dict) -> None:
        if not self.compressed:
            path2file= dump_path / (dump_name + ".pkl")
            with open(path2file, "wb") as f: pickle.dump(data, f)
        else:
            path2file= dump_path / (dump_name + _file_algorithm_mapper[self.algorithm][1])
            with _file_algorithm_mapper[self.algorithm][0](path2file, "wb") as f: 
                pickle.dump(data, f)

    def load(self, dump_path:Path, dump_name:str) -> dict:
        if not self.compressed:
            path2file = dump_path / (dump_name + ".pkl") 
            if os.path.exists(path2file): 
                with open(path2file, "rb") as f: data = pickle.load(f)
            else: data=dict()
        else:
            path2file = dump_path / (dump_name + _file_algorithm_mapper[self.algorithm][1]) 
            if os.path.exists(path2file):
                with open(path2file, "rb") as f:
                        data = _file_algorithm_mapper[self.algorithm][0](filename=f, mode="rb")
                        data = pickle.load(data)
            else: data=dict()
        return data