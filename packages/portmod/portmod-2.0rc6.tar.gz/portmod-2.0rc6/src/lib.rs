#[macro_use]
extern crate serde_with;

mod conflicts;
mod dds;
mod error;
mod metadata;
mod news;
mod yaml;

use crate::conflicts::conflicts;
use crate::dds::get_dds_dimensions;
use crate::metadata::{
    CategoryMetadata, Group, GroupDeclaration, PackageMetadata, Person, Upstream,
};
use crate::news::News;
use crate::yaml::parse_yaml;
use digest::Digest;
use esplugin::{GameId, Plugin};
use fluent_bundle::types::FluentValue;
use fluent_templates::Loader;
use std::collections::HashMap;
use std::collections::HashSet;
use std::io::BufRead;
use std::io::BufReader;
use std::path::Path;
use unic_langid::LanguageIdentifier;
use walkdir::WalkDir;

use pyo3::prelude::*;
use pyo3::types::{PyDict, PyFloat, PyLong};
use pyo3::wrap_pyfunction;

#[cfg(debug_assertions)]
use fluent_templates::ArcLoader;

#[cfg(debug_assertions)]
fn debug_l10n_dir() -> String {
    let gil = Python::acquire_gil();
    let py = gil.python();
    fn get_dir(py: Python) -> PyResult<String> {
        let locale = PyModule::import(py, "portmod.l10n")?;
        Ok(locale.get("_DEBUG_L10N_DIR")?.extract()?)
    }
    let dir = get_dir(py).map_err(|e| {
        e.print_and_set_sys_last_vars(py);
    });
    if let Ok(dir) = dir {
        dir
    } else {
        panic!("Could not detect default encoding!");
    }
}

#[cfg(debug_assertions)]
thread_local!(static ARC_LOADER: ArcLoader = ArcLoader::builder(&debug_l10n_dir(), FALLBACK_LANG)
    .customize(|bundle| bundle.set_use_isolating(should_use_isolating()))
    .build()
    .unwrap());

fn should_use_isolating() -> bool {
    // Runtime cost of this should be minimal, but we might want to switch
    // to determining locale on the rust side of things.
    let gil = Python::acquire_gil();
    let py = gil.python();
    fn get_encoding(py: Python) -> PyResult<String> {
        let locale = PyModule::import(py, "locale")?;
        Ok(locale.call0("getpreferredencoding")?.extract()?)
    }
    let encoding = get_encoding(py).map_err(|e| {
        e.print_and_set_sys_last_vars(py);
    });
    if let Ok(encoding) = encoding {
        if encoding.starts_with("utf-") {
            return true;
        }
    } else {
        eprintln!("Could not detect default encoding!");
    }
    false
}

const FALLBACK_LANG: LanguageIdentifier = unic_langid::langid!("en-GB");

fluent_templates::static_loader! {
    static STATIC_LOADER = {
        locales: "./l10n",
        fallback_language: "en-GB",
        customise: |bundle| bundle.set_use_isolating(should_use_isolating()),
    };
}

#[allow(dead_code)]
#[allow(non_snake_case)]
fn main() {
    use pyo3::create_exception;
    use pyo3::prelude::*;

    #[pyfunction]
    pub fn parse_package_metadata(filename: String) -> PyResult<PackageMetadata> {
        Ok(parse_yaml(filename)?)
    }

    #[pyfunction]
    pub fn parse_category_metadata(filename: String) -> PyResult<CategoryMetadata> {
        Ok(parse_yaml(filename)?)
    }

    #[pyfunction]
    pub fn parse_yaml_dict(filename: String) -> PyResult<HashMap<String, String>> {
        Ok(parse_yaml(filename)?)
    }

    #[pyfunction]
    pub fn parse_groups(filename: String) -> PyResult<HashMap<String, GroupDeclaration>> {
        Ok(parse_yaml(filename)?)
    }

    #[pyfunction]
    pub fn parse_yaml_dict_dict(
        filename: String,
    ) -> PyResult<HashMap<String, HashMap<String, String>>> {
        Ok(parse_yaml(filename)?)
    }

    #[pyfunction]
    pub fn parse_news(filename: String) -> PyResult<News> {
        Ok(parse_yaml(filename)?)
    }

    #[pyfunction]
    fn file_conflicts(dirs: Vec<String>, ignore: Vec<&str>) -> PyResult<()> {
        let mut entries = Vec::new();
        let mut ignore_set = HashSet::new();
        for extstr in ignore {
            for val in extstr.split(',') {
                ignore_set.insert(val.to_string().to_lowercase());
            }
        }
        for dir in dirs {
            let mut files = HashSet::new();
            for file in WalkDir::new(&dir)
                .into_iter()
                .filter_map(Result::ok)
                .filter(|e| {
                    !e.file_type().is_dir()
                        && e.path()
                            .extension()
                            .map(|ext| {
                                !ignore_set.contains(&ext.to_str().unwrap_or("").to_lowercase())
                            })
                            .unwrap_or(true)
                })
            {
                if let Ok(suffix) = file.path().strip_prefix(&dir) {
                    files.insert(suffix.display().to_string());
                } else {
                    panic!(
                        "Internal Error: File {} is not in directory {}!",
                        file.path().display(),
                        &dir
                    );
                }
            }
            entries.push((dir.to_string(), files));
        }
        conflicts("Directories", "Files", &entries)?;
        Ok(())
    }

    #[pyfunction]
    fn get_masters(filename: String) -> PyResult<Vec<String>> {
        let mut plugin = Plugin::new(GameId::Morrowind, Path::new(&filename));
        plugin
            .parse_file(true)
            .map_err(|x| crate::error::Error::PluginError(filename.clone(), x))?;
        let list = plugin
            .masters()
            .map_err(|x| crate::error::Error::PluginError(filename.clone(), x))?;
        Ok(list)
    }

    #[pyfunction]
    fn dds_dimensions(file: String) -> PyResult<(u32, u32)> {
        let (width, height) = get_dds_dimensions(file)?;
        Ok((width, height))
    }

    #[pyfunction]
    fn l10n_lookup(lang: String, text_id: String, args: &PyDict) -> PyResult<String> {
        let lang_id: LanguageIdentifier = match lang.parse() {
            Ok(lang_id) => lang_id,
            Err(_) => {
                let gil = Python::acquire_gil();
                let py = gil.python();
                let log = py.import("portmod.log")?;
                log.call(
                    "warn_once",
                    (format!(
                        "User language identifier \"{}\" could not be parsed",
                        lang
                    ),),
                    None,
                )?;
                FALLBACK_LANG
            }
        };
        let args: Vec<PyResult<(String, FluentValue)>> = args
            .iter()
            .map(|(key, value)| {
                let typ = value.get_type();
                let key: String = key.extract()?;
                Ok(if typ.is_subclass::<PyLong>()? {
                    let value: i64 = value.extract()?;
                    (key, FluentValue::Number(value.into()))
                } else if typ.is_subclass::<PyFloat>()? {
                    let value: f64 = value.extract()?;
                    (key, FluentValue::Number(value.into()))
                } else {
                    (key, FluentValue::String(value.str()?.to_string().into()))
                })
            })
            .collect();
        for result in &args {
            if let Err(x) = result {
                let gil = Python::acquire_gil();
                let py = gil.python();
                return Err(x.clone_ref(py));
            }
        }
        let args: HashMap<String, FluentValue> = args.into_iter().map(|x| x.unwrap()).collect();
        #[cfg(debug_assertions)]
        return ARC_LOADER.with(|loader| Ok(loader.lookup_with_args(&lang_id, &text_id, &args)));
        #[cfg(not(debug_assertions))]
        Ok(STATIC_LOADER.lookup_with_args(&lang_id, &text_id, &args))
    }

    /// Hashes the given file
    /// 30MB appears to be a good buffer size for both large and small files
    #[pyfunction]
    fn _get_hash(
        filename: String,
        funcs: Vec<String>,
        buffer_size: usize,
    ) -> PyResult<Vec<String>> {
        let mut results: HashMap<&str, String> = HashMap::new();

        fn get_hash<T: Digest, R: std::io::Read>(
            hasher: T,
            reader: &mut BufReader<R>,
        ) -> PyResult<String>
        where
            T::OutputSize: std::ops::Add,
            <T::OutputSize as std::ops::Add>::Output: digest::generic_array::ArrayLength<u8>,
        {
            let mut hasher = hasher;
            loop {
                let buffer = reader.fill_buf()?;
                let size = buffer.len();
                if size == 0 {
                    break;
                }
                hasher.update(&buffer);
                reader.consume(size);
            }
            Ok(format!("{:x}", hasher.finalize()))
        }

        for func in &funcs {
            let file = std::fs::File::open(&filename)?;
            let mut reader = BufReader::with_capacity(buffer_size, file);
            match func.as_str() {
                "BLAKE3" => {
                    let mut hasher = blake3::Hasher::new();
                    loop {
                        let buffer = reader.fill_buf()?;
                        let size = buffer.len();
                        if size == 0 {
                            break;
                        }
                        if size > 128 * 1024 {
                            hasher.update_with_join::<blake3::join::RayonJoin>(&buffer[0..size]);
                        } else {
                            hasher.update(&buffer);
                        }
                        reader.consume(size);
                    }
                    results.insert("BLAKE3", format!("{:x}", hasher.finalize()));
                }
                "SHA512" => {
                    results.insert("SHA512", get_hash(sha2::Sha512::new(), &mut reader)?);
                }
                "BLAKE2B" => {
                    results.insert("BLAKE2B", get_hash(blake2::Blake2b::new(), &mut reader)?);
                }
                "MD5" => {
                    results.insert("MD5", get_hash(md5::Md5::new(), &mut reader)?);
                }
                _ => return Err(error::Error::UnsupportedHashType(func.clone()).into()),
            }
        }

        Ok(funcs
            .iter()
            .map(|func| results[func.as_str()].clone())
            .collect())
    }

    #[pymodule]
    /// A Python module implemented in Rust.
    fn portmod(_: Python, m: &PyModule) -> PyResult<()> {
        m.add_wrapped(wrap_pyfunction!(file_conflicts))?;
        m.add_wrapped(wrap_pyfunction!(get_masters))?;
        m.add_wrapped(wrap_pyfunction!(dds_dimensions))?;
        m.add_wrapped(wrap_pyfunction!(parse_package_metadata))?;
        m.add_wrapped(wrap_pyfunction!(parse_category_metadata))?;
        m.add_wrapped(wrap_pyfunction!(parse_yaml_dict))?;
        m.add_wrapped(wrap_pyfunction!(parse_yaml_dict_dict))?;
        m.add_wrapped(wrap_pyfunction!(parse_groups))?;
        m.add_wrapped(wrap_pyfunction!(parse_news))?;
        m.add_wrapped(wrap_pyfunction!(l10n_lookup))?;
        m.add_wrapped(wrap_pyfunction!(_get_hash))?;
        m.add_class::<PackageMetadata>()?;
        m.add_class::<Upstream>()?;
        m.add_class::<CategoryMetadata>()?;
        m.add_class::<Group>()?;
        m.add_class::<Person>()?;
        m.add_class::<GroupDeclaration>()?;
        m.add_class::<News>()?;

        Ok(())
    }

    create_exception!(portmod, Error, pyo3::exceptions::PyException);
}
