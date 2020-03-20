# LightRDF

A fast and lightweight Python RDF parser which wraps bindings to Rust's [Rio](https://github.com/Tpt/rio) using [PyO3](https://github.com/PyO3/pyo3).

## Features

- Supports N-Triples, Turtle, and RDF/XML
- Handles large-size RDF documents
- Provides HDT-like interfaces

## Install

```
pip install lightrdf
```

## Usage

**Iterate over all triples (Parser)**

```python
import lightrdf

parser = lightrdf.Parser()  # or lightrdf.xml.Parser() for xml

for triple in parser.parse("./go.owl", base_iri=""):
    print(triple)
```
**Iterate over all triples (HDT-like)**

```python
import lightrdf

doc = lightrdf.RDFDocument("./go.owl")
# ...or lightrdf.RDFDocument("./go.owl", base_iri="", parser=lightrdf.xml.PatternParser) for xml

# `None` matches arbitrary term
for triple in doc.search_triples(None, None, None):
    print(triple)
```

**Triple pattern (HDT-like)**

```python
import lightrdf

doc = lightrdf.RDFDocument("./go.owl")

for triple in doc.search_triples("http://purl.obolibrary.org/obo/GO_0005840", None, None):
    print(triple)

# Output:
# ('http://purl.obolibrary.org/obo/GO_0005840', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://www.w3.org/2002/07/owl#Class')
# ('http://purl.obolibrary.org/obo/GO_0005840', 'http://www.w3.org/2000/01/rdf-schema#subClassOf', 'http://purl.obolibrary.org/obo/GO_0043232')
# ...
# ('http://purl.obolibrary.org/obo/GO_0005840', 'http://www.geneontology.org/formats/oboInOwl#inSubset', 'http://purl.obolibrary.org/obo/go#goslim_yeast')
# ('http://purl.obolibrary.org/obo/GO_0005840', 'http://www.w3.org/2000/01/rdf-schema#label', '"ribosome"^^<http://www.w3.org/2001/XMLSchema#string>')
```

## Benchmark (WIP)

```
```

## Alternatives

- [RDFLib](https://github.com/RDFLib/rdflib) – (Pros) pure-Python, matured, feature-rich / (Cons) takes some time to load triples
- [pyHDT](https://github.com/Callidon/pyHDT) – (Pros) extremely fast and efficient / (Cons) requires pre-conversion into HDT

## Todo

- [ ] Push to PyPI
- [ ] Adopt CI
- [ ] Handle Base IRI
- [ ] Support NQuads and TriG
- [ ] Add docs
- [ ] Add tests
- [ ] Refactor
- [ ] Resume on error
- [ ] Allow opening fp

## License

[Rio](https://github.com/PyO3/pyo3) and [PyO3](https://github.com/PyO3/pyo3) are licensed under the Apache-2.0 license.

    Copyright 2020 Kentaro Ozeki

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
