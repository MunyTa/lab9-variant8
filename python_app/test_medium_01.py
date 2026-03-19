import unittest
import subprocess
import time
import requests
import json
from pathlib import Path

class TestGoHTTPServer(unittest.TestCase):
    """Тесты для Ср.1: Go HTTP сервер"""
    
    @classmethod
    def setUpClass(cls):
        """Запускаем сервер перед тестами"""
        cls.port = 8081
        cls.base_url = f"http://localhost:{cls.port}"
        cls.go_binary = Path(__file__).parent.parent / "go_http" / "http_server.exe"
        
        if not cls.go_binary.exists():
            raise unittest.SkipTest("Go бинарь не найден")
        
        cls.process = subprocess.Popen(
            [str(cls.go_binary), str(cls.port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        time.sleep(2)
    
    @classmethod
    def tearDownClass(cls):
        """Останавливаем сервер после тестов"""
        cls.process.terminate()
        cls.process.wait()
    
    def test_1_health_endpoint(self):
        """Тест эндпоинта /api/health"""
        response = requests.get(f"{self.base_url}/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('uptime', data)
    
    def test_2_stats_endpoint(self):
        """Тест эндпоинта /api/stats"""
        response = requests.get(f"{self.base_url}/api/stats")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('request_count', data)
        self.assertIn('uptime', data)
    
    def test_3_reverse_operation(self):
        """Тест операции reverse"""
        payload = {"text": "Hello World", "option": "reverse"}
        response = requests.post(f"{self.base_url}/api/process", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['result'], "dlroW olleH")
        self.assertEqual(data['status'], 'success')
    
    def test_4_uppercase_operation(self):
        """Тест операции uppercase"""
        payload = {"text": "hello world", "option": "uppercase"}
        response = requests.post(f"{self.base_url}/api/process", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['result'], "HELLO WORLD")
    
    def test_5_lowercase_operation(self):
        """Тест операции lowercase"""
        payload = {"text": "HELLO WORLD", "option": "lowercase"}
        response = requests.post(f"{self.base_url}/api/process", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['result'], "hello world")
    
    def test_6_count_operation(self):
        """Тест операции count"""
        payload = {"text": "Hello", "option": "count"}
        response = requests.post(f"{self.base_url}/api/process", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['result'], "Количество символов: 5")
    
    def test_7_words_operation(self):
        """Тест операции words"""
        payload = {"text": "one two three", "option": "words"}
        response = requests.post(f"{self.base_url}/api/process", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['result'], "Количество слов: 3")
    
    def test_8_invalid_method(self):
        """Тест неверного HTTP метода"""
        response = requests.get(f"{self.base_url}/api/process")
        self.assertEqual(response.status_code, 405)
    
    def test_9_missing_text(self):
        """Тест отсутствующего поля text"""
        payload = {"option": "reverse"}
        response = requests.post(f"{self.base_url}/api/process", json=payload)
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data['status'], 'error')

if __name__ == '__main__':
    unittest.main(verbosity=2)