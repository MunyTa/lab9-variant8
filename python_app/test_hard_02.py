import unittest
import tempfile
import os
import shutil
from pathlib import Path
from image_wrapper import ImageProcessor
from PIL import Image

class TestImageProcessor(unittest.TestCase):
    
    def setUp(self):
        """Используем реальное изображение test_image.jpg"""
        self.test_dir = tempfile.mkdtemp()
        
        source_image = Path(__file__).parent / "test_image.jpg"
        
        if not source_image.exists():
            raise FileNotFoundError(
                f"Файл {source_image} не найден! "
                "Положите любое изображение в папку python_app и назовите test_image.jpg"
            )
        
        self.test_image = Path(self.test_dir) / "test_image.jpg"
        shutil.copy(source_image, self.test_image)
        
        print(f"✅ Использую изображение: {source_image}")
    
    def tearDown(self):
        """Удаление временных файлов"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_resize_image(self):
        """Тест изменения размера"""
        output = Path(self.test_dir) / "resized.jpg"
        ImageProcessor.resize_image(self.test_image, output, 100, 100)
        
        self.assertTrue(output.exists())
        
        with Image.open(output) as img:
            self.assertEqual(img.size, (100, 100))
    
    def test_grayscale(self):
        """Тест конвертации в Ч/Б"""
        output = Path(self.test_dir) / "gray.jpg"
        ImageProcessor.to_grayscale(self.test_image, output)
        
        self.assertTrue(output.exists())
        
        with Image.open(output) as img:
            self.assertEqual(img.mode, 'L')
    
    def test_rotate_90(self):
        """Тест поворота на 90 градусов"""
        output = Path(self.test_dir) / "rotated.jpg"
        ImageProcessor.rotate_image(self.test_image, output, 90)
        
        self.assertTrue(output.exists())
    
    def test_rotate_invalid(self):
        """Тест неверного угла поворота"""
        output = Path(self.test_dir) / "rotated.jpg"
        with self.assertRaises(ValueError):
            ImageProcessor.rotate_image(self.test_image, output, 45)
    
    def test_get_info(self):
        """Тест получения информации"""
        info = ImageProcessor.get_info(self.test_image)
        
        self.assertIn("width", info)
        self.assertIn("height", info)
        self.assertIn("format", info)
        self.assertIsInstance(info["width"], int)
        self.assertIsInstance(info["height"], int)
        print(f"📸 Информация: {info}")
    
    def test_file_not_found(self):
        """Тест на отсутствующий файл"""
        with self.assertRaises(FileNotFoundError):
            ImageProcessor.resize_image(Path("nonexistent.jpg"), Path("out.jpg"), 100, 100)

if __name__ == '__main__':
    unittest.main(verbosity=2)