import io

from ..lightrdf import nt as _nt


class Parser:
    def __init__(self):
        pass

    def parse(self, filelike_or_filename):
        if isinstance(filelike_or_filename, io.BufferedIOBase):
            return _nt.Parser().parse(filelike_or_filename)
        else:
            return _nt.Parser().parse_from_filename(filelike_or_filename)


class PatternParser:
    def __init__(self, pattern):
        self.pattern = pattern

    def parse(self, filelike_or_filename):
        if isinstance(filelike_or_filename, io.BufferedIOBase):
            return _nt.PatternParser(self.pattern).parse(filelike_or_filename)
        else:
            return _nt.PatternParser(self.pattern).parse_from_filename(filelike_or_filename)
