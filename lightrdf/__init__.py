import io
from pathlib import Path

from .python_module import nt
from .python_module import turtle
from .python_module import xml

__all__ = ["nt", "turtle", "xml", "Parser", "PatternParser", "RDFDocument"]

# Derived from https://github.com/rubensworks/rdf-parse.js/blob/master/lib/RdfParser.ts
CONTENT_MAPPINGS = {
    ".ttl": "text/turtle",
    ".turtle": "text/turtle",
    ".nt": "application/n-triples",
    ".ntriples": "application/n-triples",
    ".nq": "application/n-quads",
    ".nquads": "application/n-quads",
    ".rdf": "application/rdf+xml",
    ".rdfxml": "application/rdf+xml",
    ".xml": "application/rdf+xml",
    ".owl": "application/rdf+xml",
    ".n3": "text/n3",
    ".trig": "application/trig",
    ".jsonld": "application/ld+json",
    ".json": "application/json",
}


class Error(Exception):
    pass


def guess_module(suffix):
    if CONTENT_MAPPINGS[suffix] == "application/n-triples":
        module = nt
    elif CONTENT_MAPPINGS[suffix] == "text/turtle":
        module = turtle
    elif CONTENT_MAPPINGS[suffix] == "application/rdf+xml":
        module = xml
    else:
        # TODO: Unimplemented error before this
        # Raise error, or fallback
        raise Error("cannot guess content type from extension")
    return module


class Parser:
    def __init__(self):
        pass

    def parse(self, filelike_or_filename, format=None, base_iri=None):
        if isinstance(filelike_or_filename, io.BufferedIOBase):
            if format is None:
                raise Error("Format must be specified")
            parser = guess_module(f".{format}").Parser
        else:
            path = Path(filelike_or_filename)
            parser = guess_module(path.suffix).Parser
        if base_iri:
            return parser().parse(filelike_or_filename, base_iri)
        else:
            return parser().parse(filelike_or_filename)


class PatternParser:
    def __init__(self, pattern):
        self.pattern = pattern

    def parse(self, filelike_or_filename, format=None, base_iri=None):
        if isinstance(filelike_or_filename, io.BufferedIOBase):
            if format is None:
                raise Error("Format must be specified")
            parser = guess_module(f".{format}").PatternParser
        else:
            path = Path(filelike_or_filename)
            parser = guess_module(path.suffix).PatternParser
        if base_iri:
            return parser(self.pattern).parse(filelike_or_filename, base_iri)
        else:
            return parser(self.pattern).parse(filelike_or_filename)


class RDFDocument:
    def __init__(self, filelike_or_filename, base_iri=None, parser=None):
        self.filelike_or_filename = filelike_or_filename
        self.base_iri = base_iri
        if isinstance(filelike_or_filename, io.BufferedIOBase):
            if parser is None:
                raise Error("Parser must be specified")
            self.parser = parser
        else:
            if parser is None:
                path = Path(filelike_or_filename)
                parser = guess_module(path.suffix).PatternParser
            self.parser = parser

    def search_triples(self, s, p, o):
        if isinstance(self.filelike_or_filename, io.BufferedIOBase):
            self.filelike_or_filename.seek(0)
        if self.base_iri:
            return self.parser((s, p, o)).parse(self.filelike_or_filename, self.base_iri)
        else:
            return self.parser((s, p, o)).parse(self.filelike_or_filename)
