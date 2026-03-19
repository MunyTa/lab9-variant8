use pyo3::prelude::*;
use sha2::{Sha256, Digest};
use pyo3::types::PyBytes;

#[pyfunction]
fn xor_encrypt_bytes(data: Vec<u8>, key: Vec<u8>) -> Vec<u8> {
    let mut result = Vec::with_capacity(data.len());
    
    for (i, &byte) in data.iter().enumerate() {
        result.push(byte ^ key[i % key.len()]);
    }
    
    result
}

#[pyfunction]
fn xor_encrypt(data: String, key: String) -> PyResult<String> {
    let data_bytes = data.as_bytes();
    let key_bytes = key.as_bytes();
    let mut result = Vec::with_capacity(data_bytes.len());
    
    for (i, &byte) in data_bytes.iter().enumerate() {
        result.push(byte ^ key_bytes[i % key_bytes.len()]);
    }
    
    match String::from_utf8(result) {
        Ok(s) => Ok(s),
        Err(_) => {
            Ok(data)
        }
    }
}

#[pyfunction]
fn xor_decrypt(data: String, key: String) -> PyResult<String> {
    xor_encrypt(data, key)
}

#[pyfunction]
fn sha256_hash(data: String) -> String {
    let mut hasher = Sha256::new();
    hasher.update(data.as_bytes());
    let result = hasher.finalize();
    hex::encode(result)
}

#[pymodule]
fn rust_crypto(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(xor_encrypt, m)?)?;
    m.add_function(wrap_pyfunction!(xor_decrypt, m)?)?;
    m.add_function(wrap_pyfunction!(xor_encrypt_bytes, m)?)?;
    m.add_function(wrap_pyfunction!(sha256_hash, m)?)?;
    Ok(())
}