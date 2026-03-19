import subprocess
import time
import requests
from pathlib import Path
from crypto_wrapper import CryptoWrapper
from image_wrapper import ImageProcessor
import json

class GoOrchestrator:
    """Оркестратор для управления Go сервером"""
    
    def __init__(self, go_binary_path: Path, port: int = 8081):
        self.go_binary_path = go_binary_path
        self.port = port
        self.process = None
        self.base_url = f"http://localhost:{port}"
        
        if not self.go_binary_path.exists():
            raise FileNotFoundError(f"Go бинарь не найден: {go_binary_path}")
    
    def start(self):
        """Запуск Go сервера"""
        print(f"🚀 Запуск Go сервера на порту {self.port}...")
        
        self.process = subprocess.Popen(
            [str(self.go_binary_path), str(self.port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        time.sleep(2)
        
        try:
            response = requests.get(f"{self.base_url}/api/health", timeout=2)
            if response.status_code == 200:
                print("✅ Go сервер запущен")
                return True
        except:
            print("❌ Не удалось подключиться к серверу")
            return False
    
    def stop(self):
        """Остановка Go сервера"""
        if self.process:
            print("\n🛑 Остановка Go сервера...")
            self.process.terminate()
            self.process.wait(timeout=5)
            print("✅ Go сервер остановлен")
    
    def process_text(self, text: str, operation: str = "reverse") -> dict:
        """Отправка текста на обработку в Go"""
        try:
            response = requests.post(
                f"{self.base_url}/api/process",
                json={"text": text, "option": operation},
                timeout=5
            )
            return response.json()
        except Exception as e:
            return {"error": str(e), "status": "error"}
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()


class IntegrationDemo:
    """Демонстрация интеграции Go + Rust + Python"""
    
    def __init__(self, go_binary_path: Path, port: int = 8081):
        self.go_binary_path = go_binary_path
        self.port = port
        self.orchestrator = GoOrchestrator(go_binary_path, port)
        
        self.crypto = CryptoWrapper()
        self.image = ImageProcessor()
    
    def run_demo(self, test_image_path: Path = None):
        """Запуск демонстрации"""
        
        print("\n" + "="*60)
        print("🔷 ИНТЕГРАЦИЯ Go + Rust + Python")
        print("="*60)
        
        with self.orchestrator as go:
            
            print("\n1️⃣  Go: Обработка текста")
            print("-" * 40)
            
            texts = [
                ("Hello World", "reverse"),
                ("python programming", "uppercase"),
                ("GOLANG ROCKS", "lowercase"),
                ("Тестовое сообщение", "count"),
                ("one two three four five", "words")
            ]
            
            for text, op in texts:
                result = go.process_text(text, op)
                if "error" not in result:
                    print(f"   {op:10}: '{text}' → '{result['result']}'")
            
            print("\n2️⃣  Rust: Криптография")
            print("-" * 40)
            
            last_result = go.process_text("Secret Data", "reverse")
            if "error" not in last_result:
                data_to_encrypt = last_result['result']
                
                print(f"   Данные для шифрования: {data_to_encrypt}")
                
                key = self.crypto.generate_key(8)
                print(f"   Ключ шифрования: {key}")
                
                encrypted = self.crypto.encrypt(data_to_encrypt, key)
                print(f"   Зашифровано (XOR): {encrypted}")
                
                hashed = self.crypto.hash(data_to_encrypt)
                print(f"   SHA256 хеш: {hashed[:16]}...")
                
                decrypted = self.crypto.decrypt(encrypted, key)
                print(f"   Расшифровано: {decrypted}")
            
            if test_image_path and test_image_path.exists():
                print("\n3️⃣  Rust: Обработка изображений")
                print("-" * 40)
                
                info = self.image.get_info(test_image_path)
                print(f"   Исходное: {info['width']}x{info['height']} {info['format']}")
                
                resized = test_image_path.parent / "resized.png"
                self.image.resize_image(test_image_path, resized, 200, 150)
                print(f"   Изменен размер: {resized}")
                
                gray = test_image_path.parent / "grayscale.png"
                self.image.to_grayscale(test_image_path, gray)
                print(f"   Черно-белое: {gray}")
                
                rotated = test_image_path.parent / "rotated.png"
                self.image.rotate_image(test_image_path, rotated, 90)
                print(f"   Поворот на 90°: {rotated}")
            else:
                print("\n3️⃣  Rust: Обработка изображений (пропущено)")
                print("-" * 40)
                print("   Нет тестового изображения. Положите test_image.jpg в папку python_app")
            
            print("\n" + "="*60)
            print("✅ Интеграция завершена успешно!")
            print("="*60)