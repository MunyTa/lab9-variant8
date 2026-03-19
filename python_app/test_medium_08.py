import unittest
import rust_crypto

class TestRustCrypto(unittest.TestCase):
    
    def test_xor_encrypt_decrypt(self):
        """Тест XOR шифрования и дешифровки с ASCII"""
        original = "Hello World"
        key = "key123"
        
        encrypted = rust_crypto.xor_encrypt(original, key)
        decrypted = rust_crypto.xor_decrypt(encrypted, key)
        
        self.assertEqual(decrypted, original)
        self.assertNotEqual(encrypted, original)
    
    def test_xor_with_different_keys(self):
        """Тест что разные ключи дают разные результаты"""
        text = "Test"
        key1 = "key1"
        key2 = "key2"
        
        enc1 = rust_crypto.xor_encrypt(text, key1)
        enc2 = rust_crypto.xor_encrypt(text, key2)
        
        self.assertNotEqual(enc1, enc2)
    
    def test_xor_empty_string(self):
        """Тест с пустой строкой"""
        empty = ""
        key = "key"
        
        encrypted = rust_crypto.xor_encrypt(empty, key)
        decrypted = rust_crypto.xor_decrypt(encrypted, key)
        
        self.assertEqual(decrypted, empty)
        self.assertEqual(encrypted, empty)
    
    def test_xor_with_unicode(self):
        """Тест с Unicode символами - исправлено!"""
        text = "Привет, мир! 你好 🌍"
        key = "unicode_key"
        
        text_bytes = text.encode('utf-8')
        key_bytes = key.encode('utf-8')
        
        encrypted_bytes = rust_crypto.xor_encrypt_bytes(text_bytes, key_bytes)
        decrypted_bytes = rust_crypto.xor_encrypt_bytes(encrypted_bytes, key_bytes)
        
        decrypted = decrypted_bytes.decode('utf-8')
        
        self.assertEqual(decrypted, text)
    
    def test_sha256_hash(self):
        """Тест SHA256 хеширования"""
        text = "Hello World"
        
        expected_hash = "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e"
        
        result = rust_crypto.sha256_hash(text)
        
        self.assertEqual(result, expected_hash)
        self.assertEqual(len(result), 64)
    
    def test_sha256_empty_string(self):
        """Тест SHA256 для пустой строки"""
        empty = ""
        
        expected_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        
        result = rust_crypto.sha256_hash(empty)
        
        self.assertEqual(result, expected_hash)
    
    def test_xor_with_long_key(self):
        """Тест с длинным ключом"""
        text = "Short text"
        long_key = "This is a very long key that exceeds the text length"
        
        encrypted = rust_crypto.xor_encrypt(text, long_key)
        decrypted = rust_crypto.xor_decrypt(encrypted, long_key)
        
        self.assertEqual(decrypted, text)
    
    def test_sha256_different_inputs(self):
        """Тест что разные входные данные дают разные хеши"""
        hash1 = rust_crypto.sha256_hash("Hello")
        hash2 = rust_crypto.sha256_hash("hello")
        
        self.assertNotEqual(hash1, hash2)
        self.assertEqual(len(hash1), 64)
        self.assertEqual(len(hash2), 64)

if __name__ == '__main__':
    unittest.main(verbosity=2)