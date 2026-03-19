import unittest
import time
import requests
from pathlib import Path
from go_client import GoHTTPServer

class TestGoPythonClient(unittest.TestCase):
    """Тесты для Ср.3: Вызов Go из Python"""
    
    def setUp(self):
        """Подготовка к тесту"""
        self.port = 8082
        self.go_binary = Path(__file__).parent.parent / "go_http" / "http_server.exe"
        
        if not self.go_binary.exists():
            self.skipTest("Go бинарь не найден")
    
    def test_1_server_start_stop(self):
        """Тест запуска и остановки сервера через Python"""
        server = GoHTTPServer(self.go_binary, self.port)
        
        self.assertTrue(server.start())
        self.assertIsNotNone(server.process)
        
        time.sleep(2)
        health = server.health_check()
        self.assertIsNotNone(health)
        self.assertEqual(health['status'], 'healthy')
        
        server.stop()
        time.sleep(1)
        
        with self.assertRaises(Exception):
            requests.get(f"http://localhost:{self.port}/api/health", timeout=1)
    
    def test_2_process_text_reverse(self):
        """Тест отправки текста на реверс"""
        server = GoHTTPServer(self.go_binary, self.port)
        server.start()
        try:
            result = server.process_text("Hello", "reverse")
            self.assertIsNotNone(result)
            self.assertEqual(result['result'], "olleH")
            self.assertEqual(result['status'], 'success')
        finally:
            server.stop()
    
    def test_3_process_text_uppercase(self):
        """Тест отправки текста на uppercase"""
        server = GoHTTPServer(self.go_binary, self.port)
        server.start()
        try:
            result = server.process_text("hello", "uppercase")
            self.assertIsNotNone(result)
            self.assertEqual(result['result'], "HELLO")
        finally:
            server.stop()
    
    def test_4_process_text_lowercase(self):
        """Тест отправки текста на lowercase"""
        server = GoHTTPServer(self.go_binary, self.port)
        server.start()
        try:
            result = server.process_text("HELLO", "lowercase")
            self.assertIsNotNone(result)
            self.assertEqual(result['result'], "hello")
        finally:
            server.stop()
    
    def test_5_process_text_count(self):
        """Тест подсчета символов"""
        server = GoHTTPServer(self.go_binary, self.port)
        server.start()
        try:
            result = server.process_text("Hello World", "count")
            self.assertIsNotNone(result)
            self.assertEqual(result['result'], "Количество символов: 11")
        finally:
            server.stop()
    
    def test_6_process_text_words(self):
        """Тест подсчета слов"""
        server = GoHTTPServer(self.go_binary, self.port)
        server.start()
        try:
            result = server.process_text("one two three", "words")
            self.assertIsNotNone(result)
            self.assertEqual(result['result'], "Количество слов: 3")
        finally:
            server.stop()
    
    def test_7_invalid_option(self):
        """Тест с неверной опцией"""
        server = GoHTTPServer(self.go_binary, self.port)
        server.start()
        try:
            result = server.process_text("test", "invalid")
            self.assertIsNotNone(result)
            self.assertEqual(result['result'], "test")
        finally:
            server.stop()
    
    def test_8_health_check(self):
        """Тест проверки здоровья"""
        server = GoHTTPServer(self.go_binary, self.port)
        server.start()
        try:
            health = server.health_check()
            self.assertIsNotNone(health)
            self.assertIn('status', health)
            self.assertIn('uptime', health)
        finally:
            server.stop()
    
    def test_9_stats_check(self):
        """Тест получения статистики"""
        server = GoHTTPServer(self.go_binary, self.port)
        server.start()
        try:
            server.process_text("test1", "reverse")
            server.process_text("test2", "uppercase")
            time.sleep(1)
            
            stats = server.get_stats()
            self.assertIsNotNone(stats)
            self.assertIn('request_count', stats)
            self.assertGreaterEqual(stats['request_count'], 2)
        finally:
            server.stop()

if __name__ == '__main__':
    unittest.main(verbosity=2)