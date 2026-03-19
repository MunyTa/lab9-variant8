import rust_crypto
import random
import string

class CryptoWrapper:
 
    @staticmethod
    def encrypt(text: str, key: str) -> str:
        return rust_crypto.xor_encrypt(text, key)
    
    @staticmethod
    def decrypt(text: str, key: str) -> str:
        return rust_crypto.xor_decrypt(text, key)
    
    @staticmethod
    def hash(text: str) -> str:
        return rust_crypto.sha256_hash(text)
    
    @staticmethod
    def generate_key(length: int = 8) -> str:
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(random.choice(chars) for _ in range(length))
    
    @staticmethod
    def encrypt_bytes(data: bytes, key: bytes) -> bytes:
        return rust_crypto.xor_encrypt_bytes(data, key)