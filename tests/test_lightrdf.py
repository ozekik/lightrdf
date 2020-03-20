import os
import pytest

import lightrdf

current_dir = os.path.abspath(os.path.dirname(__file__))

# fmt: off
testcases = [
    ("fao.nt", [
        ('http://purl.obolibrary.org/obo/FAO_0002011', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://www.w3.org/2002/07/owl#Class'),
        ('http://purl.obolibrary.org/obo/FAO_0002011', 'http://www.w3.org/2000/01/rdf-schema#subClassOf', 'http://purl.obolibrary.org/obo/FAO_0001001'),
        ('http://purl.obolibrary.org/obo/FAO_0002011', 'http://purl.obolibrary.org/obo/IAO_0000115', '"A hypha that emerges from a yeast-form cell upon stimulation by the pheromone of a compatible mating partner. An example is observed in Cryptococcus species."'),
        ('http://purl.obolibrary.org/obo/FAO_0002011', 'http://www.geneontology.org/formats/oboInOwl#created_by', '"midori"'),
        ('http://purl.obolibrary.org/obo/FAO_0002011', 'http://www.geneontology.org/formats/oboInOwl#creation_date', '"2020-01-23T16:29:54Z"'),
        ('http://purl.obolibrary.org/obo/FAO_0002011', 'http://www.geneontology.org/formats/oboInOwl#hasOBONamespace', '"fungal_anatomy_ontology"'),
        ('http://purl.obolibrary.org/obo/FAO_0002011', 'http://www.geneontology.org/formats/oboInOwl#id', '"FAO:0002011"'),
        ('http://purl.obolibrary.org/obo/FAO_0002011', 'http://www.w3.org/2000/01/rdf-schema#label', '"mating filament"'),
        ('Bf2541d9418081488bf51b62519d99390', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://www.w3.org/2002/07/owl#Axiom'),
        ('Bf2541d9418081488bf51b62519d99390', 'http://www.w3.org/2002/07/owl#annotatedSource', 'http://purl.obolibrary.org/obo/FAO_0002011'),
        ('Bf2541d9418081488bf51b62519d99390', 'http://www.w3.org/2002/07/owl#annotatedProperty', 'http://purl.obolibrary.org/obo/IAO_0000115'),
        ('Bf2541d9418081488bf51b62519d99390', 'http://www.w3.org/2002/07/owl#annotatedTarget', '"A hypha that emerges from a yeast-form cell upon stimulation by the pheromone of a compatible mating partner. An example is observed in Cryptococcus species."'),
        ('Bf2541d9418081488bf51b62519d99390', 'http://www.geneontology.org/formats/oboInOwl#hasDbXref', '"FAO:doi"'),
        ('http://purl.obolibrary.org/obo/NCBITaxon_4751', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://www.w3.org/2002/07/owl#Class'),
    ]),
    ("fao.ttl", [
        ('http://purl.obolibrary.org/obo/FAO_0002011', 'http://www.w3.org/2000/01/rdf-schema#label', '"mating filament"^^<http://www.w3.org/2001/XMLSchema#string>'),
        ('http://purl.obolibrary.org/obo/FAO_0002011', 'http://www.geneontology.org/formats/oboInOwl#id', '"FAO:0002011"^^<http://www.w3.org/2001/XMLSchema#string>'),
        ('http://purl.obolibrary.org/obo/FAO_0002011', 'http://www.geneontology.org/formats/oboInOwl#hasOBONamespace', '"fungal_anatomy_ontology"^^<http://www.w3.org/2001/XMLSchema#string>'),
        ('http://purl.obolibrary.org/obo/FAO_0002011', 'http://www.geneontology.org/formats/oboInOwl#creation_date', '"2020-01-23T16:29:54Z"^^<http://www.w3.org/2001/XMLSchema#string>'),
        ('http://purl.obolibrary.org/obo/FAO_0002011', 'http://www.geneontology.org/formats/oboInOwl#created_by', '"midori"^^<http://www.w3.org/2001/XMLSchema#string>'),
        ('http://purl.obolibrary.org/obo/FAO_0002011', 'http://purl.obolibrary.org/obo/IAO_0000115', '"A hypha that emerges from a yeast-form cell upon stimulation by the pheromone of a compatible mating partner. An example is observed in Cryptococcus species."^^<http://www.w3.org/2001/XMLSchema#string>'),
        ('http://purl.obolibrary.org/obo/FAO_0002011', 'http://www.w3.org/2000/01/rdf-schema#subClassOf', 'http://purl.obolibrary.org/obo/FAO_0001001'),
        ('http://purl.obolibrary.org/obo/FAO_0002011', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://www.w3.org/2002/07/owl#Class'),
        ('riog00000173', 'http://www.geneontology.org/formats/oboInOwl#hasDbXref', '"FAO:doi"^^<http://www.w3.org/2001/XMLSchema#string>'),
        ('riog00000173', 'http://www.w3.org/2002/07/owl#annotatedTarget', '"A hypha that emerges from a yeast-form cell upon stimulation by the pheromone of a compatible mating partner. An example is observed in Cryptococcus species."^^<http://www.w3.org/2001/XMLSchema#string>'),
        ('riog00000173', 'http://www.w3.org/2002/07/owl#annotatedProperty', 'http://purl.obolibrary.org/obo/IAO_0000115'),
        ('riog00000173', 'http://www.w3.org/2002/07/owl#annotatedSource', 'http://purl.obolibrary.org/obo/FAO_0002011'),
        ('riog00000173', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://www.w3.org/2002/07/owl#Axiom'),
        ('http://purl.obolibrary.org/obo/NCBITaxon_4751', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://www.w3.org/2002/07/owl#Class'),
    ]),
    ("fao.owl", [
        ('http://purl.obolibrary.org/obo/FAO_0002011', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://www.w3.org/2002/07/owl#Class'),
        ('http://purl.obolibrary.org/obo/FAO_0002011', 'http://www.w3.org/2000/01/rdf-schema#subClassOf', 'http://purl.obolibrary.org/obo/FAO_0001001'),
        ('http://purl.obolibrary.org/obo/FAO_0002011', 'http://purl.obolibrary.org/obo/IAO_0000115', '"A hypha that emerges from a yeast-form cell upon stimulation by the pheromone of a compatible mating partner. An example is observed in Cryptococcus species."^^<http://www.w3.org/2001/XMLSchema#string>'),
        ('http://purl.obolibrary.org/obo/FAO_0002011', 'http://www.geneontology.org/formats/oboInOwl#created_by', '"midori"^^<http://www.w3.org/2001/XMLSchema#string>'),
        ('http://purl.obolibrary.org/obo/FAO_0002011', 'http://www.geneontology.org/formats/oboInOwl#creation_date', '"2020-01-23T16:29:54Z"^^<http://www.w3.org/2001/XMLSchema#string>'),
        ('http://purl.obolibrary.org/obo/FAO_0002011', 'http://www.geneontology.org/formats/oboInOwl#hasOBONamespace', '"fungal_anatomy_ontology"^^<http://www.w3.org/2001/XMLSchema#string>'),
        ('http://purl.obolibrary.org/obo/FAO_0002011', 'http://www.geneontology.org/formats/oboInOwl#id', '"FAO:0002011"^^<http://www.w3.org/2001/XMLSchema#string>'),
        ('http://purl.obolibrary.org/obo/FAO_0002011', 'http://www.w3.org/2000/01/rdf-schema#label', '"mating filament"^^<http://www.w3.org/2001/XMLSchema#string>'),
        ('riog00000314', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://www.w3.org/2002/07/owl#Axiom'),
        ('riog00000314', 'http://www.w3.org/2002/07/owl#annotatedSource', 'http://purl.obolibrary.org/obo/FAO_0002011'),
        ('riog00000314', 'http://www.w3.org/2002/07/owl#annotatedProperty', 'http://purl.obolibrary.org/obo/IAO_0000115'),
        ('riog00000314', 'http://www.w3.org/2002/07/owl#annotatedTarget', '"A hypha that emerges from a yeast-form cell upon stimulation by the pheromone of a compatible mating partner. An example is observed in Cryptococcus species."^^<http://www.w3.org/2001/XMLSchema#string>'),
        ('riog00000314', 'http://www.geneontology.org/formats/oboInOwl#hasDbXref', '"FAO:doi"^^<http://www.w3.org/2001/XMLSchema#string>'),
        ('http://purl.obolibrary.org/obo/NCBITaxon_4751', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://www.w3.org/2002/07/owl#Class'),
    ]),
]
# fmt: on

# fmt: off
testcases_pattern = [
    ("fao.nt", [
        ('http://purl.obolibrary.org/obo/FAO_0002011', 'http://www.w3.org/2000/01/rdf-schema#subClassOf', 'http://purl.obolibrary.org/obo/FAO_0001001'),
    ]),
    ("fao.ttl", [
        ('http://purl.obolibrary.org/obo/FAO_0002011', 'http://www.w3.org/2000/01/rdf-schema#subClassOf', 'http://purl.obolibrary.org/obo/FAO_0001001'),
    ]),
    ("fao.owl", [
        ('http://purl.obolibrary.org/obo/FAO_0002011', 'http://www.w3.org/2000/01/rdf-schema#subClassOf', 'http://purl.obolibrary.org/obo/FAO_0001001'),
    ]),
]
# fmt: on


@pytest.mark.parametrize("filename,expected", testcases)
def test_parser(filename, expected):
    path = os.path.join(current_dir, filename)
    parser = lightrdf.Parser()
    triples = []
    for triple in parser.parse(path):
        triples.append(triple)
    assert len(triples) == 1840 and triples[-len(expected) :] == expected


@pytest.mark.parametrize("filename,expected", testcases_pattern)
def test_pattern_parser(filename, expected):
    path = os.path.join(current_dir, filename)
    parser = lightrdf.PatternParser(
        (
            "http://purl.obolibrary.org/obo/FAO_0002011",
            "http://www.w3.org/2000/01/rdf-schema#subClassOf",
            None,
        )
    )
    triples = []
    for triple in parser.parse(path):
        triples.append(triple)
    assert triples == expected


@pytest.mark.parametrize("filename,expected", testcases_pattern)
def test_rdf_document(filename, expected):
    path = os.path.join(current_dir, filename)
    doc = lightrdf.RDFDocument(path)
    triples = []
    pattern = (
        "http://purl.obolibrary.org/obo/FAO_0002011",
        "http://www.w3.org/2000/01/rdf-schema#subClassOf",
        None,
    )
    for triple in doc.search_triples(*pattern):
        triples.append(triple)
    # Repeat
    for triple in doc.search_triples(*pattern):
        triples.append(triple)
    assert triples == expected * 2
