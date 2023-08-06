import os

class Version:
    def __init__(self, v_str):
        self._split = v_str.split('.')
        self.major = self._get_version_at_index(0)
        self.minor = self._get_version_at_index(1)
        self.patch = self._get_version_at_index(2)

    def _get_version_at_index(self, index):
        try:
            return int(self._split[index])
        except:
            return None

    def __repr__(self):
        return '.'.join(str(v) for v in [self.major, self.minor, self.patch] if v is not None)


class Signature:
    appname = "General-Testing-And-Feedback"
    appauthor = "LITE"
    authors = 'Titusz Ban, Craig Evans & Sam Wilson @ Leeds Institute for Teaching Excellence'

    @staticmethod
    def get_version():
        version_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), "VERSION")
        if not os.path.isfile(version_file):
            return None
        with open(version_file) as f:
            return Version(f.read())
