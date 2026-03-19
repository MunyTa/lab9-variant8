#!/usr/bin/env python3
"""
Python клиент для взаимодействия с Go HTTP сервером
Демонстрация вызова скомпилированного Go бинаря из Python
"""

import subprocess
import requests
import json
import time
import sys
import os
from dataclasses import dataclass
from pathlib import Path

@dataclass
class ServerConfig:
    """Конфигурация сервера"""
    binary_path: Path
    port: int = 8080
    host: str = "localhost"
    timeout: int = 5
    startup_delay: float = 2.0

class GoHTTPServer:
    """Класс для управления Go HTTP сервером"""
    
    def __init__(self, binary_path, port=8080):
        self.binary_path = Path(binary_path).absolute()
        self.port = port
        self.process = None
        self.base_url = f"http://localhost:{port}"
        
        if not self.binary_path.exists():
            raise FileNotFoundError(f"Go бинарь не найден: {self.binary_path}")
    
    def start(self):
        """Запуск Go сервера"""
        print(f"🚀 Запуск Go сервера из {self.binary_path}...")
        
        try:
            self.process = subprocess.Popen(
                [str(self.binary_path), str(self.port)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            time.sleep(2)
            
            if self.process.poll() is not None:
                stderr = self.process.stderr.read()
                raise Exception(f"Сервер завершился с ошибкой: {stderr}")
            
            print("✅ Go сервер успешно запущен")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка запуска сервера: {e}")
            return False
    
    def stop(self):
        """Остановка Go сервера"""
        if self.process:
            print("\n🛑 Остановка Go сервера...")
            self.process.terminate()
            self.process.wait(timeout=5)
            print("✅ Go сервер остановлен")
    
    def process_text(self, text, option="reverse"):
        """Отправка текста на обработку"""
        url = f"{self.base_url}/api/process"
        payload = {
            "text": text,
            "option": option
        }
        
        try:
            response = requests.post(url, json=payload, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка при запросе: {e}")
            return None
    
    def health_check(self):
        """Проверка здоровья сервера"""
        try:
            response = requests.get(f"{self.base_url}/api/health", timeout=2)
            return response.json()
        except:
            return None
    
    def get_stats(self):
        """Получение статистики сервера"""
        try:
            response = requests.get(f"{self.base_url}/api/stats", timeout=2)
            return response.json()
        except:
            return None

def demonstrate_go_server():
    """Демонстрация работы с Go сервером"""
    
    print("=" * 60)
    print("ЗАДАНИЕ 3: Вызов Go бинаря из Python (subprocess)")
    print("=" * 60)
    
    binary_path = Path(__file__).parent.parent / "go_http" / "http_server.exe"
    
    server = GoHTTPServer(binary_path, port=8081)
    
    try:
        if not server.start():
            print("❌ Не удалось запустить сервер")
            return
        
        print("\n📊 Проверка здоровья сервера:")
        health = server.health_check()
        if health:
            print(f"   Статус: {health['status']}")
            print(f"   Время работы: {health['uptime']}")
        
        test_strings = [
            ("Hello, World!", "reverse"),
            ("python programming", "uppercase"),
            ("GOLANG IS AWESOME", "lowercase"),
            ("This is a test message", "count"),
            ("one two three four five", "words"),
        ]
        
        print("\n🔄 Демонстрация обработки текста:")
        for text, option in test_strings:
            print(f"\n   📝 Текст: '{text}'")
            print(f"   ⚙️  Операция: {option}")
            
            result = server.process_text(text, option)
            if result:
                print(f"   ✅ Результат: {result['result']}")
                print(f"   🕐 Время: {result['timestamp']}")
            else:
                print("   ❌ Ошибка обработки")
        
        print("\n📈 Статистика сервера:")
        stats = server.get_stats()
        if stats:
            print(f"   Запросов обработано: {stats['request_count']}")
            print(f"   Время работы: {stats['uptime']}")
            print(f"   Запросов в секунду: {stats['requests_per_second']:.2f}")
        
    finally:
        server.stop()
    
    print("\n" + "=" * 60)
    print("✅ Демонстрация завершена успешно!")

if __name__ == "__main__":
    demonstrate_go_server()