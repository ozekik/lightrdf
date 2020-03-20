use pyo3::prelude::*;
use pyo3::wrap_pymodule;

mod nt;
use nt::*;
mod turtle;
use turtle::*;
mod xml;
use xml::*;

mod common;
mod parser_macro;

#[pymodule]
fn lightrdf(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pymodule!(nt))?;
    m.add_wrapped(wrap_pymodule!(turtle))?;
    m.add_wrapped(wrap_pymodule!(xml))?;

    Ok(())
}
