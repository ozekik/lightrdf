def is_iri(term: str):
    return term.startswith("<")


def is_blank(term: str):
    return term.startswith("_:")


def is_literal(term: str):
    return term.startswith('"')
