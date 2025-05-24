import hashlib
from typing import List


class BloomFilter:
    def __init__(self, size: int = 1000, num_hashes: int = 3):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size

    def _hashes(self, item: str) -> List[int]:
        hashes = []
        for i in range(self.num_hashes):
            hash_input = f"{item}-{i}".encode("utf-8")
            hash_digest = hashlib.sha256(hash_input).hexdigest()
            hash_int = int(hash_digest, 16)
            hashes.append(hash_int % self.size)
        return hashes

    def add(self, item: str):
        if not isinstance(item, str):
            return
        for hash_index in self._hashes(item):
            self.bit_array[hash_index] = 1

    def __contains__(self, item: str) -> bool:
        if not isinstance(item, str):
            return False
        return all(self.bit_array[i] for i in self._hashes(item))

def check_password_uniqueness(bloom_filter: BloomFilter, passwords: List[str]) -> dict:
    result = {}

    for password in passwords:
        if not isinstance(password, str) or not password.strip():
            result[password] = "Invalid password"
        elif password in bloom_filter:
            result[password] = "Duplicate password"
        else:
            bloom_filter.add(password)
            result[password] = "Unique password"

    return result

if __name__ == "__main__":
    # Ініціалізація фільтра Блума
    bloom = BloomFilter(size=1000, num_hashes=3)

    # Додавання існуючих паролів
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    # Перевірка нових паролів
    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest", "", None, 12345]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    # Виведення результатів
    for password, status in results.items():
        print(f"Пароль '{password}' — {status}.")
