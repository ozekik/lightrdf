# LightRDF

[![](https://github.com/ozekik/lightrdf/workflows/CI/badge.svg)](https://github.com/ozekik/lightrdf/actions)
[![PyPI](https://img.shields.io/pypi/v/lightrdf.svg)](https://pypi.python.org/pypi/lightrdf/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/lightrdf.svg)](https://pypistats.org/packages/lightrdf)

A fast and lightweight Python RDF parser which wraps bindings to Rust's [Rio](https://github.com/Tpt/rio) using [PyO3](https://github.com/PyO3/pyo3).

## Contents

- [Features](#features)
- [Install](#install)
- [Basic Usage](#basic-usage)
  - [Iterate over all triples](#iterate-over-all-triples)
  - [Search triples with a triple pattern](#search-triples-with-a-triple-pattern)
  - [Search triples with a triple pattern (Regex)](#search-triples-with-a-triple-pattern-regex)
  <!-- - [Parse IRIs, blank nodes, literals](#parse-terms) -->
  - [Load file objects / texts](#load-file-objects--parse-texts)
- [Benchmark (WIP)](#benchmark-wip)
- [Alternatives](#alternatives)
- [Todo](#todo)
- [License](#license)

## Features

- Supports N-Triples, Turtle, and RDF/XML
- Handles large-size RDF documents
- Provides HDT-like interfaces

## Install

```
pip install lightrdf
```

## Basic Usage

### Iterate over all triples

With `Parser`:

```python
import lightrdf

parser = lightrdf.Parser()

for triple in parser.parse("./go.owl", base_iri=None):
    print(triple)
```

With `RDFDocument`:

```python
import lightrdf

doc = lightrdf.RDFDocument("./go.owl")

# `None` matches arbitrary term
for triple in doc.search_triples(None, None, None):
    print(triple)
```

### Search triples with a triple pattern

```python
import lightrdf

doc = lightrdf.RDFDocument("./go.owl")

for triple in doc.search_triples("http://purl.obolibrary.org/obo/GO_0005840", None, None):
    print(triple)

# Output:
# ('<http://purl.obolibrary.org/obo/GO_0005840>', '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>', '<http://www.w3.org/2002/07/owl#Class>')
# ('<http://purl.obolibrary.org/obo/GO_0005840>', '<http://www.w3.org/2000/01/rdf-schema#subClassOf>', '<http://purl.obolibrary.org/obo/GO_0043232>')
# ...
# ('<http://purl.obolibrary.org/obo/GO_0005840>', '<http://www.geneontology.org/formats/oboInOwl#inSubset>', '<http://purl.obolibrary.org/obo/go#goslim_yeast>')
# ('<http://purl.obolibrary.org/obo/GO_0005840>', '<http://www.w3.org/2000/01/rdf-schema#label>', '"ribosome"^^<http://www.w3.org/2001/XMLSchema#string>')
```

### Search triples with a triple pattern (Regex)

```python
import lightrdf
from lightrdf import Regex

doc = lightrdf.RDFDocument("./go.owl")

for triple in doc.search_triples(Regex("^<http://purl.obolibrary.org/obo/.*>$"), None, Regex(".*amino[\w]+?transferase")):
    print(triple)

# Output:
# ('<http://purl.obolibrary.org/obo/GO_0003961>', '<http://www.w3.org/2000/01/rdf-schema#label>', '"O-acetylhomoserine aminocarboxypropyltransferase activity"^^<http://www.w3.org/2001/XMLSchema#string>')
# ('<http://purl.obolibrary.org/obo/GO_0004047>', '<http://www.geneontology.org/formats/oboInOwl#hasExactSynonym>', '"S-aminomethyldihydrolipoylprotein:(6S)-tetrahydrofolate aminomethyltransferase (ammonia-forming) activity"^^<http://www.w3.org/2001/XMLSchema#string>')
# ...
# ('<http://purl.obolibrary.org/obo/GO_0050447>', '<http://www.w3.org/2000/01/rdf-schema#label>', '"zeatin 9-aminocarboxyethyltransferase activity"^^<http://www.w3.org/2001/XMLSchema#string>')
# ('<http://purl.obolibrary.org/obo/GO_0050514>', '<http://www.geneontology.org/formats/oboInOwl#hasExactSynonym>', '"spermidine:putrescine 4-aminobutyltransferase (propane-1,3-diamine-forming)"^^<http://www.w3.org/2001/XMLSchema#string>')
```

<!-- ### Parse IRIs, blank nodes, literals

```python
import lightrdf
from lightrdf import is_iri, is_blank, is_literal, parse

doc = lightrdf.RDFDocument("./go.owl")

for s, p, o in doc.search_triples(None, None, None):
    if is_iri(s):
        s = parse.iri(s)
``` -->

### Load file objects / texts

Load file objects with `Parser`:

```python
import lightrdf

parser = lightrdf.Parser()

with open("./go.owl", "rb") as f:
    for triple in parser.parse(f, format="owl", base_iri=None):
        print(triple)
```

Load file objects with `RDFDocument`:

```python
import lightrdf

with open("./go.owl", "rb") as f:
    doc = lightrdf.RDFDocument(f, parser=lightrdf.xml.PatternParser)

    for triple in doc.search_triples("http://purl.obolibrary.org/obo/GO_0005840", None, None):
        print(triple)
```

Load texts:

```python
import io
import lightrdf

data = """<http://one.example/subject1> <http://one.example/predicate1> <http://one.example/object1> .
_:subject1 <http://an.example/predicate1> "object1" .
_:subject2 <http://an.example/predicate2> "object2" ."""

doc = lightrdf.RDFDocument(io.BytesIO(data.encode()), parser=lightrdf.turtle.PatternParser)

for triple in doc.search_triples("http://one.example/subject1", None, None):
    print(triple)
```

## Benchmark (WIP)

> On MacBook Air (13-inch, 2017), 1.8 GHz Intel Core i5, 8 GB 1600 MHz DDR3

<https://gist.github.com/ozekik/b2ae3be0fcaa59670d4dd4759cdffbed>

```bash
$ wget -q http://purl.obolibrary.org/obo/go.owl
$ gtime python3 count_triples_rdflib_graph.py ./go.owl  # RDFLib 4.2.2
1436427
235.29user 2.30system 3:59.56elapsed 99%CPU (0avgtext+0avgdata 1055816maxresident)k
0inputs+0outputs (283major+347896minor)pagefaults 0swaps
$ gtime python3 count_triples_lightrdf_rdfdocument.py ./go.owl  # LightRDF 0.1.1
1436427
7.90user 0.22system 0:08.27elapsed 98%CPU (0avgtext+0avgdata 163760maxresident)k
0inputs+0outputs (106major+41389minor)pagefaults 0swaps
$ gtime python3 count_triples_lightrdf_parser.py ./go.owl  # LightRDF 0.1.1
1436427
8.00user 0.24system 0:08.47elapsed 97%CPU (0avgtext+0avgdata 163748maxresident)k
0inputs+0outputs (106major+41388minor)pagefaults 0swaps
```

<p align="center">
<img src="assets/benchmark1.png" width="480" />
</p>

<https://gist.github.com/ozekik/636a8fb521401070e02e010ce591fa92>

```bash
$ wget -q http://downloads.dbpedia.org/2016-10/dbpedia_2016-10.nt
$ gtime python3 count_triples_rdflib_ntparser.py dbpedia_2016-10.nt  # RDFLib 4.2.2
31050
1.63user 0.23system 0:02.47elapsed 75%CPU (0avgtext+0avgdata 26568maxresident)k
0inputs+0outputs (1140major+6118minor)pagefaults 0swaps
$ gtime python3 count_triples_lightrdf_ntparser.py dbpedia_2016-10.nt  # LightRDF 0.1.1
31050
0.21user 0.04system 0:00.36elapsed 71%CPU (0avgtext+0avgdata 7628maxresident)k
0inputs+0outputs (534major+1925minor)pagefaults 0swaps
```

<p align="center">
<img src="assets/benchmark2.png" width="480" />
</p>

## Alternatives

- [RDFLib](https://github.com/RDFLib/rdflib) – (Pros) pure-Python, matured, feature-rich / (Cons) takes some time to load triples
- [pyHDT](https://github.com/Callidon/pyHDT) – (Pros) extremely fast and efficient / (Cons) requires pre-conversion into HDT

## Todo

- [x] Push to PyPI
- [x] Adopt CI
- [x] Handle Base IRI
- [x] Add basic tests
- [ ] Switch to maturin-action from cibuildwheel
- [ ] Support NQuads and TriG
- [ ] Add docs
- [ ] Add tests for [w3c/rdf-tests](https://github.com/w3c/rdf-tests)
- [ ] Resume on error
- [x] Allow opening fp
- [ ] Support and test on RDF-star

## License

[Rio](https://github.com/Tpt/rio) and [PyO3](https://github.com/PyO3/pyo3) are licensed under the Apache-2.0 license.

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
