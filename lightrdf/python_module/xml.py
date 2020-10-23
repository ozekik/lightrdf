import io

from ..lightrdf import xml as _xml


class Parser:
    def __init__(self):
        pass

    def parse(self, filelike_or_filename, base_iri=None):
        if isinstance(filelike_or_filename, io.BufferedIOBase):
            return _xml.Parser().parse(filelike_or_filename, base_iri)
        else:
            return _xml.Parser().parse_from_filename(filelike_or_filename, base_iri)


class PatternParser:
    def __init__(self, pattern):
        self.pattern = pattern

    def parse(self, filelike_or_filename, base_iri=None):
        if isinstance(filelike_or_filename, io.BufferedIOBase):
            return _xml.PatternParser(self.pattern).parse(filelike_or_filename, base_iri)
        else:
            return _xml.PatternParser(self.pattern).parse_from_filename(filelike_or_filename, base_iri)
