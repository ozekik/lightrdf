import re
from typing import Tuple, Optional

iri_re = re.compile(r"<(.*)>")
blank_re = re.compile(r"_:(.*)")
literal_re = re.compile(r'"(.*)"(?:\^\^([^@]*))?(?:@(.*))?')


def iri(term: str) -> str:
    """Returns an IRI, i.e., the value inside `<` and `>`."""
    (iri,) = iri_re.match(term).groups()
    return iri


def blank(term: str) -> str:
    """Returns [a blank node label](https://www.w3.org/TR/n-triples/#h3_BNodes), i.e., the value after `_:`."""
    (id,) = blank_re.match(term).groups()
    return id


def literal(term: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """Returns a tuple `(value, datatype, language)`."""
    value, datatype, language = literal_re.match(term).groups()
    return value, datatype, language
