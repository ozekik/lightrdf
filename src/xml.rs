extern crate signal_hook;
use pyo3::prelude::*;
use pyo3::types::PyTuple;
use rio_api::parser::TriplesParser;
use rio_xml::{RdfXmlError, RdfXmlParser};
use std::convert::From;
use std::fs::File;
use std::io::BufReader;
use std::iter;
use std::sync::atomic::AtomicBool;
use std::sync::Arc;

use super::common;
use super::gen_create_iter;

gen_create_iter!(RdfXmlError);

#[pyclass]
struct Parser {}

#[pymethods]
impl Parser {
  #[new]
  fn new() -> Self {
    Parser {}
  }
  fn parse(&self, filename: &str, base_iri: Option<&str>) -> PyResult<common::TriplesIterator> {
    let f = File::open(filename)?;
    let buf = BufReader::new(f);
    if let Ok(parser) = RdfXmlParser::new(buf, base_iri.unwrap_or("")) {
      let term = Arc::new(AtomicBool::new(false));
      Ok(common::TriplesIterator {
        it: Box::new(create_iter(parser)),
        pattern: (None, None, None) as common::TriplePattern,
        term: term,
      })
    } else {
      Err(common::Error::py_err("parser initialization failed"))
    }
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
      pattern.get_item(0).extract::<Option<String>>().unwrap(),
      pattern.get_item(1).extract::<Option<String>>().unwrap(),
      pattern.get_item(2).extract::<Option<String>>().unwrap(),
    );
    PatternParser { pattern: _pattern }
  }
  fn parse(&self, filename: &str, base_iri: Option<&str>) -> PyResult<common::TriplesIterator> {
    let f = File::open(filename)?;
    let buf = BufReader::new(f);
    if let Ok(parser) = RdfXmlParser::new(buf, base_iri.unwrap_or("")) {
      let term = Arc::new(AtomicBool::new(false));
      Ok(common::TriplesIterator {
        it: Box::new(create_iter(parser)),
        pattern: self.pattern.clone(),
        term: term,
      })
    } else {
      Err(common::Error::py_err("parser initialization failed"))
    }
  }
}

#[pymodule]
fn xml(_py: Python, m: &PyModule) -> PyResult<()> {
  m.add_class::<Parser>()?;
  m.add_class::<PatternParser>()?;

  Ok(())
}
