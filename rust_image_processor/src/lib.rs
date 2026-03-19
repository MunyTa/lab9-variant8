use pyo3::prelude::*;
use image::{ImageFormat, DynamicImage, imageops::FilterType};
use std::io::Cursor;

#[pyfunction]
fn resize_image(image_bytes: Vec<u8>, width: u32, height: u32) -> PyResult<Vec<u8>> {
    let img = match image::load_from_memory(&image_bytes) {
        Ok(img) => img,
        Err(e) => return Err(pyo3::exceptions::PyIOError::new_err(e.to_string())),
    };
    
    let resized = img.resize_exact(width, height, FilterType::Lanczos3);
    
    let mut buffer = Vec::new();
    if let Err(e) = resized.write_to(&mut Cursor::new(&mut buffer), ImageFormat::Png) {
        return Err(pyo3::exceptions::PyIOError::new_err(e.to_string()));
    }
    
    Ok(buffer)
}

#[pyfunction]
fn grayscale(image_bytes: Vec<u8>) -> PyResult<Vec<u8>> {
    let img = match image::load_from_memory(&image_bytes) {
        Ok(img) => img,
        Err(e) => return Err(pyo3::exceptions::PyIOError::new_err(e.to_string())),
    };
    
    let gray = img.grayscale();
    
    let mut buffer = Vec::new();
    if let Err(e) = gray.write_to(&mut Cursor::new(&mut buffer), ImageFormat::Png) {
        return Err(pyo3::exceptions::PyIOError::new_err(e.to_string()));
    }
    
    Ok(buffer)
}

#[pyfunction]
fn rotate(image_bytes: Vec<u8>, degrees: f32) -> PyResult<Vec<u8>> {
    let img = match image::load_from_memory(&image_bytes) {
        Ok(img) => img,
        Err(e) => return Err(pyo3::exceptions::PyIOError::new_err(e.to_string())),
    };
    
    let rotated = match degrees as i32 {
        90 => img.rotate90(),
        180 => img.rotate180(),
        270 => img.rotate270(),
        _ => img,
    };
    
    let mut buffer = Vec::new();
    if let Err(e) = rotated.write_to(&mut Cursor::new(&mut buffer), ImageFormat::Png) {
        return Err(pyo3::exceptions::PyIOError::new_err(e.to_string()));
    }
    
    Ok(buffer)
}

#[pyfunction]
fn get_image_info(image_bytes: Vec<u8>) -> PyResult<Vec<u32>> {
    let img = match image::load_from_memory(&image_bytes) {
        Ok(img) => img,
        Err(e) => return Err(pyo3::exceptions::PyIOError::new_err(e.to_string())),
    };
    
    Ok(vec![img.width(), img.height()])
}

#[pymodule]
fn rust_image_processor(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(resize_image, m)?)?;
    m.add_function(wrap_pyfunction!(grayscale, m)?)?;
    m.add_function(wrap_pyfunction!(rotate, m)?)?;
    m.add_function(wrap_pyfunction!(get_image_info, m)?)?;
    Ok(())
}