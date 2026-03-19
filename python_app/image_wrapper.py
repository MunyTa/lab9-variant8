import rust_image_processor
from pathlib import Path
import os

class ImageProcessor:
    """Обертка для Rust библиотеки обработки изображений"""
    
    @staticmethod
    def resize_image(input_path: Path, output_path: Path, width: int, height: int):
        """
        Изменяет размер изображения
        
        Args:
            input_path: путь к исходному изображению
            output_path: путь для сохранения результата
            width: новая ширина
            height: новая высота
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Файл не найден: {input_path}")
        
        with open(input_path, 'rb') as f:
            image_bytes = f.read()
        
        result_bytes = rust_image_processor.resize_image(image_bytes, width, height)
        
        with open(output_path, 'wb') as f:
            f.write(result_bytes)
        
        print(f"✅ Изображение сохранено: {output_path} ({width}x{height})")
    
    @staticmethod
    def to_grayscale(input_path: Path, output_path: Path):
        """Конвертирует изображение в черно-белое"""
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Файл не найден: {input_path}")
        
        with open(input_path, 'rb') as f:
            image_bytes = f.read()
        
        result_bytes = rust_image_processor.grayscale(image_bytes)
        
        with open(output_path, 'wb') as f:
            f.write(result_bytes)
        
        print(f"✅ Черно-белое изображение сохранено: {output_path}")
    
    @staticmethod
    def rotate_image(input_path: Path, output_path: Path, degrees: int):
        """Поворачивает изображение (90, 180, 270 градусов)"""
        if degrees not in [90, 180, 270]:
            raise ValueError("Поддерживаются только углы: 90, 180, 270")
        
        with open(input_path, 'rb') as f:
            image_bytes = f.read()
        
        result_bytes = rust_image_processor.rotate(image_bytes, float(degrees))
        
        with open(output_path, 'wb') as f:
            f.write(result_bytes)
        
        print(f"✅ Изображение повернуто на {degrees}°: {output_path}")
    
    @staticmethod
    def get_info(input_path: Path) -> dict:
        """Возвращает информацию об изображении"""
        with open(input_path, 'rb') as f:
            image_bytes = f.read()
        
        info = rust_image_processor.get_image_info(image_bytes)
        return {
            "width": info[0],
            "height": info[1],
            "format": "PNG" if str(input_path).lower().endswith('.png') else "JPEG"
        }