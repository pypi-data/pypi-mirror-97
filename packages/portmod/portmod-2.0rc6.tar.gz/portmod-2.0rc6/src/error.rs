// Copyright 2019-2020 Portmod Authors
// Distributed under the terms of the GNU General Public License v3

use derive_more::{Display, From};
use pyo3::{exceptions::PyOSError, PyErr};

#[derive(Debug, Display, From)]
pub enum Error {
    #[display(fmt = "{}: {}", _0, _1)]
    IOError(String, std::io::Error),
    #[display(fmt = "{}: {}", _0, _1)]
    YamlError(String, serde_yaml::Error),
    LanguageIdentifierError(unic_langid::LanguageIdentifierError),
    StdError(Box<dyn std::error::Error>),
    UnsupportedHashType(String),
    #[display(fmt = "Error when parsing file {}: {}", _0, _1)]
    PluginError(String, esplugin::Error),
}

impl std::convert::From<Error> for PyErr {
    fn from(err: Error) -> PyErr {
        PyOSError::new_err(err.to_string())
    }
}
