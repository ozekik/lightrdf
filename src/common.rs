extern crate signal_hook;
use pyo3::create_exception;
use pyo3::exceptions;
use pyo3::prelude::*;
use regex::Regex;
use rio_api::model::{Subject, Term, Triple};
use rio_turtle::TurtleError;
use rio_xml::RdfXmlError;
use std::convert::From;
use std::error;
use std::fmt;
use std::iter;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;

pub type StringTriple = (String, String, String);
pub type TriplePattern = (Option<String>, Option<String>, Option<String>);
pub type RegexTriplePattern = (Option<Regex>, Option<Regex>, Option<Regex>);

// // https://docs.rs/rio_turtle/0.4.0/src/rio_turtle/error.rs.html
// create_exception!(turtle, IO, exceptions::Exception);
// create_exception!(turtle, UnknownPrefix, exceptions::Exception);
// create_exception!(turtle, PrematureEOF, exceptions::Exception);
// create_exception!(turtle, UnexpectedByte, exceptions::Exception);
// create_exception!(turtle, InvalidUnicodeCodePoint, exceptions::Exception);
// create_exception!(turtle, InvalidIri, exceptions::Exception);

// // https://docs.rs/rio_xml/0.2.0/src/rio_xml/error.rs.html
// create_exception!(xml, Xml, exceptions::Exception);
// create_exception!(xml, InvalidIri, exceptions::Exception);
// create_exception!(xml, Other, exceptions::Exception);

create_exception!(lightrdf, Error, exceptions::PyException);

#[derive(Debug)]
pub enum ParserError {
    TurtleError(TurtleError),
    RdfXmlError(RdfXmlError),
}

impl fmt::Display for ParserError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match *self {
            ParserError::TurtleError(ref e) => write!(f, "{}", e),
            ParserError::RdfXmlError(ref e) => write!(f, "{}", e),
        }
    }
}

impl error::Error for ParserError {}

impl From<TurtleError> for ParserError {
    fn from(e: TurtleError) -> Self {
        match &e {
            _ => ParserError::TurtleError(e),
        }
    }
}

impl From<RdfXmlError> for ParserError {
    fn from(e: RdfXmlError) -> Self {
        match &e {
            _ => ParserError::RdfXmlError(e),
        }
    }
}

pub fn triple_to_striple(t: Triple) -> StringTriple {
    let subj = match t.subject {
        Subject::NamedNode(node) => node.to_string(),
        Subject::BlankNode(node) => node.to_string(),
        Subject::Triple(triple) => triple.to_string(), // TODO: Handle RDF-star
    };
    let pred = t.predicate.to_string();
    let obj = match t.object {
        Term::NamedNode(node) => node.to_string(),
        Term::BlankNode(node) => node.to_string(),
        Term::Literal(literal) => literal.to_string(),
        Term::Triple(triple) => triple.to_string(), // TODO: Handle RDF-star
    };
    (subj, pred, obj) as StringTriple
}

#[pyclass]
pub struct TriplesIterator {
    pub it: Box<dyn iter::Iterator<Item = Result<StringTriple, ParserError>> + Send>,
    pub pattern: RegexTriplePattern,
    pub term: Arc<AtomicBool>,
}

#[pymethods]
impl TriplesIterator {
    fn __iter__(slf: PyRefMut<Self>) -> PyResult<PyObject> {
        let py = unsafe { Python::assume_gil_acquired() };
        signal_hook::flag::register(signal_hook::consts::SIGINT, Arc::clone(&slf.term))?;
        Ok(slf.into_py(py))
    }

    fn __next__(mut slf: PyRefMut<Self>) -> PyResult<Option<StringTriple>> {
        while !slf.term.load(Ordering::Relaxed) {
            match slf.it.next() {
                Some(Ok(t)) => {
                    if (slf.pattern.0.is_some() && !slf.pattern.0.as_ref().unwrap().is_match(&t.0))
                        || (slf.pattern.1.is_some()
                            && !slf.pattern.1.as_ref().unwrap().is_match(&t.1))
                        || (slf.pattern.2.is_some()
                            && !slf.pattern.2.as_ref().unwrap().is_match(&t.2))
                    {
                        continue;
                    }
                    return Ok(Some(t));
                }
                Some(Err(e)) => {
                    // Rio can recover from error in case of ntriples/nquads
                    // continue;
                    return match e {
                        ParserError::TurtleError(_) => Err(Error::new_err(e.to_string())),
                        ParserError::RdfXmlError(_) => Err(Error::new_err(e.to_string())),
                    };
                }
                _ => {
                    return Err(exceptions::PyStopIteration::new_err(""));
                }
            }
        }
        Err(exceptions::PyKeyboardInterrupt::new_err(""))
    }
}
