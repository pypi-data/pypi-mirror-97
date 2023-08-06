import appdirs
import hashlib
import shutil
from pathlib import Path
from ..signature import Signature
from ..general import util, constants
from .compile_examiner import compile_cpp_to_o


class OCache:
    def __init__(self, cpp_std=constants.DEFAULT_CPP_STANDARD):
        self._cache_dir = Path(appdirs.user_cache_dir(Signature.appname, Signature.appauthor))
        if not self._cache_dir.is_dir():
            self._cache_dir.mkdir(parents=True)

        files = util.get_files_in_dir(self._cache_dir)
        self._files = {file.name:file for file in files}
        self._cpp_std = cpp_std
    
    def _get_hashed_name(self, path):
        path = Path(path)
        assert path.is_file(), path.absolute().as_posix()

        hasher = hashlib.md5()
        with path.open('rb') as f:
            hasher.update(f.read())
        return f"{str(hasher.hexdigest())[:16]}.o"

    def get(self, path):
        name = self._get_hashed_name(path)
        return self._files.get(name, None)

    def add(self, path):
        name = self._get_hashed_name(path)
        cached_path = Path(self._cache_dir, name).absolute().as_posix()
        self._files[name] = Path(compile_cpp_to_o(path.absolute().as_posix(), cached_path, working_dir=path.parent.absolute().as_posix(), std=self._cpp_std))

    def add_or_get(self, path):
        cached = self.get(path)
        if cached:
            return cached
        self.add(path)
        return self.get(path)

    def clear(self):
        if self._cache_dir.is_dir():
            shutil.rmtree(self._cache_dir.absolute().as_posix())
        self._cache_dir.mkdir(parents=True)
        self._files = {}
