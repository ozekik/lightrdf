from pathlib import Path

from .lightrdf import nt, turtle, xml

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
        module = lightrdf.nt
    elif CONTENT_MAPPINGS[suffix] == "text/turtle":
        module = lightrdf.turtle
    elif CONTENT_MAPPINGS[suffix] == "application/rdf+xml":
        module = lightrdf.xml
    else:
        # TODO: Unimplemented error before this
        # Raise error, or fallback
        raise Error("cannot guess content type from extension")
    return module


class Parser:
    def __init__(self):
        pass

    def parse(self, filename, base_iri=""):
        path = Path(filename)
        parser = guess_module(path.suffix).Parser
        if base_iri:
            return parser().parse(filename, base_iri)
        else:
            return parser().parse(filename)


class PatternParser:
    def __init__(self, pattern):
        self.pattern = pattern

    def parse(self, filename, base_iri=""):
        path = Path(filename)
        parser = guess_module(path.suffix).PatternParser
        if base_iri:
            return parser(self.pattern).parse(filename, base_iri)
        else:
            return parser(self.pattern).parse(filename)


class RDFDocument:
    def __init__(self, filename, base_iri="", parser=None):
        self.filename = filename
        self.base_iri = base_iri
        if parser is None:
            path = Path(filename)
            parser = guess_module(path.suffix).PatternParser
        self.parser = parser

    def search_triples(self, s, p, o):
        if self.base_iri:
            return self.parser((s, p, o)).parse(self.filename, self.base_iri)
        else:
            return self.parser((s, p, o)).parse(self.filename)
