// Copyright 2019-2020 Portmod Authors
// Distributed under the terms of the GNU General Public License v3

use crate::error::Error;
use std::fs::File;
use std::io::Read;

pub fn parse_yaml<T: for<'de> serde::Deserialize<'de>>(filename: String) -> Result<T, Error> {
    let mut file = File::open(&filename).map_err(|e| Error::IOError(filename.clone(), e))?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)
        .map_err(|e| Error::IOError(filename.clone(), e))?;

    Ok(serde_yaml::from_str(&contents).map_err(|e| Error::YamlError(filename.clone(), e))?)
}
