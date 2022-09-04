import re
import string


def escape(x: str):
    # TODO: Use Rust regex escape
    x = re.escape(x)
    for w in string.whitespace:
        x = x.replace(f"\\{w}", w)
    return x


class Term:
    def __str__(self):
        return self.pattern


class Regex(Term):
    def __init__(self, pattern):
        self.pattern = pattern


class IRI(Term):
    def __init__(self, iri):
        self.iri = iri
        iri = iri if type(iri) is Regex or iri is None else escape(iri)
        self.pattern = "^<{}>$".format(iri if iri else "(.*)")


class Blank(Term):
    def __init__(self, id):
        self.id = id
        id = id if type(id) is Regex or id is None else escape(id)
        self.pattern = "^_:{}$".format(id if id else "(.*)")


class Literal(Term):
    def __init__(self, value, datatype, language):
        self.value = value
        self.datatype = datatype
        self.language = language
        value = value if type(value) is Regex or value is None else escape(value)
        datatype = (
            datatype
            if type(datatype) is Regex or datatype is None
            else escape(datatype)
        )
        language = (
            language
            if type(language) is Regex or language is None
            else escape(language)
        )
        self.pattern = '^"{}"{}{}$'.format(
            value if value else "(.*)",
            f"^^{datatype}" if datatype else r"(?:\^\^([^@]*))?",
            f"@{language}" if language else r"(?:@(.*))?",
        )


class Triple(Term):
    # TODO
    pass
