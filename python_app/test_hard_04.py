import unittest
import tempfile
import os
import shutil
import json
from pathlib import Path
from orchestrator import GoOrchestrator, IntegrationDemo
from crypto_wrapper import CryptoWrapper
from image_wrapper import ImageProcessor

class TestIntegration(unittest.TestCase):
    """Тесты для интеграции (Пов.4)"""
    
    def setUp(self):
        """Подготовка к тестам"""
        self.go_binary = Path(__file__).parent.parent / "go_http" / "http_server.exe"
        self.test_image = Path(__file__).parent / "test_image.jpg"
        
        if not self.go_binary.exists():
            self.skipTest("Go бинарь не найден")
    
    def test_orchestrator_start_stop(self):
        """Тест 1: Запуск и остановка оркестратора"""
        orchestrator = GoOrchestrator(self.go_binary, 8082)
        
        with orchestrator:
            import requests
            response = requests.get("http://localhost:8082/api/health", timeout=2)
            self.assertEqual(response.status_code, 200)
        
        with self.assertRaises(Exception):
            requests.get("http://localhost:8082/api/health", timeout=2)
    
    def test_orchestrator_process_text(self):
        """Тест 2: Обработка текста через оркестратор"""
        with GoOrchestrator(self.go_binary, 8083) as go:
            result = go.process_text("Hello", "reverse")
            self.assertIn("result", result)
            self.assertEqual(result["result"], "olleH")
    
    def test_crypto_integration(self):
        """Тест 3: Интеграция с криптобиблиотекой"""
        crypto = CryptoWrapper()
        
        key = crypto.generate_key(8)
        self.assertEqual(len(key), 8)
        
        original = "Secret Data"
        encrypted = crypto.encrypt(original, key)
        decrypted = crypto.decrypt(encrypted, key)
        
        self.assertEqual(decrypted, original)
        self.assertNotEqual(encrypted, original)
        
        hash_result = crypto.hash(original)
        self.assertEqual(len(hash_result), 64)
    
    def test_image_integration(self):
        """Тест 4: Интеграция с библиотекой изображений"""
        if not self.test_image.exists():
            self.skipTest("Тестовое изображение не найдено")
        
        image = ImageProcessor()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            
            info = image.get_info(self.test_image)
            self.assertIn("width", info)
            self.assertIn("height", info)
            
            resized = tmp_path / "resized.jpg"
            image.resize_image(self.test_image, resized, 100, 100)
            self.assertTrue(resized.exists())
            
            gray = tmp_path / "gray.jpg"
            image.to_grayscale(self.test_image, gray)
            self.assertTrue(gray.exists())
    
    def test_full_integration_demo(self):
        """Тест 5: Полная интеграция всех компонентов"""
        demo = IntegrationDemo(self.go_binary, 8084)
        
        try:
            demo.run_demo(self.test_image if self.test_image.exists() else None)
            success = True
        except Exception as e:
            success = False
            print(f"Ошибка: {e}")
        
        self.assertTrue(success)

if __name__ == '__main__':
    unittest.main(verbosity=2)