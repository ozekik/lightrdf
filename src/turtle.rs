extern crate signal_hook;
use itertools::Itertools;
use oxiri::Iri;
use pyo3::prelude::*;
use pyo3::types::PyTuple;
use pyo3_file::PyFileLikeObject;
use regex::{escape, Regex};
use rio_api::parser::TriplesParser;
use rio_turtle::{TurtleError, TurtleParser};
use std::fs::File;
use std::io::BufReader;
use std::iter;
use std::sync::atomic::AtomicBool;
use std::sync::Arc;

use super::common;
use super::gen_create_iter;

gen_create_iter!(TurtleError);

#[pyclass]
struct Parser {}

#[pymethods]
impl Parser {
    #[new]
    fn new() -> Self {
        Parser {}
    }
    fn parse(&self, file: PyObject, base_iri: Option<&str>) -> PyResult<common::TriplesIterator> {
        let f = PyFileLikeObject::with_requirements(file, true, false, false)?;
        let buf = BufReader::new(f);
        let parser = TurtleParser::new(
            buf,
            base_iri.and_then(|iri| Iri::parse(iri.to_string()).ok()),
        );
        let term = Arc::new(AtomicBool::new(false));
        Ok(common::TriplesIterator {
            it: Box::new(create_iter(parser)),
            pattern: (None, None, None) as common::RegexTriplePattern,
            term: term,
        })
    }
    fn parse_from_filename(
        &self,
        filename: &str,
        base_iri: Option<&str>,
    ) -> PyResult<common::TriplesIterator> {
        let f = File::open(filename)?;
        let buf = BufReader::new(f);
        let parser = TurtleParser::new(
            buf,
            base_iri.and_then(|iri| Iri::parse(iri.to_string()).ok()),
        );
        let term = Arc::new(AtomicBool::new(false));
        Ok(common::TriplesIterator {
            it: Box::new(create_iter(parser)),
            pattern: (None, None, None) as common::RegexTriplePattern,
            term: term,
        })
    }
}

#[pyclass]
struct PatternParser {
    // pattern: common::TriplePattern,
    pattern_re: common::RegexTriplePattern,
}

#[pymethods]
impl PatternParser {
    #[new]
    #[pyo3(signature = (pattern, regex = true))]
    fn new(pattern: &PyTuple, regex: bool) -> Self {
        let _pattern = pattern.extract::<common::TriplePattern>().unwrap();
        let pattern_re: (Option<Regex>, Option<Regex>, Option<Regex>) =
            vec![_pattern.0.clone(), _pattern.1.clone(), _pattern.2.clone()]
                .iter()
                .map(|x| match x {
                    None => None,
                    Some(term) => {
                        if regex {
                            Some(Regex::new(term).unwrap())
                        } else {
                            Some(Regex::new(&escape(term)).unwrap())
                        }
                    }
                })
                .collect_tuple()
                .unwrap();
        PatternParser {
            // pattern: _pattern,
            pattern_re,
        }
    }
    fn parse(&self, file: PyObject, base_iri: Option<&str>) -> PyResult<common::TriplesIterator> {
        let f = PyFileLikeObject::with_requirements(file, true, false, false)?;
        let buf = BufReader::new(f);
        let parser = TurtleParser::new(
            buf,
            base_iri.and_then(|iri| Iri::parse(iri.to_string()).ok()),
        );
        let term = Arc::new(AtomicBool::new(false));
        Ok(common::TriplesIterator {
            it: Box::new(create_iter(parser)),
            pattern: self.pattern_re.clone(),
            term: term,
        })
    }
    fn parse_from_filename(
        &self,
        filename: &str,
        base_iri: Option<&str>,
    ) -> PyResult<common::TriplesIterator> {
        let f = File::open(filename)?;
        let buf = BufReader::new(f);
        let parser = TurtleParser::new(
            buf,
            base_iri.and_then(|iri| Iri::parse(iri.to_string()).ok()),
        );
        let term = Arc::new(AtomicBool::new(false));
        Ok(common::TriplesIterator {
            it: Box::new(create_iter(parser)),
            pattern: self.pattern_re.clone(),
            term: term,
        })
    }
}

#[pymodule]
pub(crate) fn turtle(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<Parser>()?;
    m.add_class::<PatternParser>()?;

    Ok(())
}
