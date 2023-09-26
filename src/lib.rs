use pyo3::prelude::*;
use pyo3::wrap_pymodule;

mod nt;
mod turtle;
mod xml;

mod common;
mod parser_macro;

#[pymodule]
fn lightrdf(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pymodule!(nt::nt))?;
    m.add_wrapped(wrap_pymodule!(turtle::turtle))?;
    m.add_wrapped(wrap_pymodule!(xml::xml))?;

    Ok(())
}
