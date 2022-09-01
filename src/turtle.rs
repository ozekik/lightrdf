extern crate signal_hook;
use oxiri::Iri;
use pyo3::prelude::*;
use pyo3::types::PyTuple;
use pyo3_file::PyFileLikeObject;
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
            pattern: (None, None, None) as common::TriplePattern,
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
            pattern: (None, None, None) as common::TriplePattern,
            term: term,
        })
    }
}

#[pyclass]
struct PatternParser {
    pattern: common::TriplePattern,
}

#[pymethods]
impl PatternParser {
    #[new]
    fn new(pattern: &PyTuple) -> Self {
        let _pattern: common::TriplePattern = (
            pattern.get_item(0).unwrap().extract::<Option<String>>().unwrap(),
            pattern.get_item(1).unwrap().extract::<Option<String>>().unwrap(),
            pattern.get_item(2).unwrap().extract::<Option<String>>().unwrap(),
        );
        PatternParser { pattern: _pattern }
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
            pattern: self.pattern.clone(),
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
            pattern: self.pattern.clone(),
            term: term,
        })
    }
}

#[pymodule]
pub(crate) fn turtle(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Parser>()?;
    m.add_class::<PatternParser>()?;

    Ok(())
}
