"""
streebog.py - Основной алгоритм ГОСТ 34.11-2018 (Стрибог)

Реализация функции хэширования с поддержкой 256 и 512 бит.
Потоковый API для обработки данных произвольной длины.
"""

from typing import Optional
from constants import IV_512, IV_256
from compression import g
from utils import (
    add_mod_2n_512,
    chunk_64,
    pad_last_block,
    bytes_to_int,
    int_to_bytes,
    xor_bytes
)


# ============================================================================
# КЛАСС STREEBOG - ПОТОКОВЫЙ ИНТЕРФЕЙС
# ============================================================================

class Streebog:
    """
    Криптографическая хэш-функция ГОСТ 34.11-2018 (Стрибог).
    
    Поддерживает потоковую обработку данных с накоплением состояния.
    
    Args:
        out_bits: Длина выходного хэша (256 или 512 бит)
        
    Example:
        >>> hasher = Streebog(512)
        >>> hasher.update(b"Hello")
        >>> hasher.update(b" World")
        >>> hasher.final().hex()
        '...'
    """
    
    def __init__(self, out_bits: int = 512):
        """
        Инициализация хэшера.
        
        Args:
            out_bits: 256 или 512
            
        Raises:
            ValueError: Если out_bits не 256 и не 512
        """
        if out_bits not in (256, 512):
            raise ValueError(f"out_bits должен быть 256 или 512, получено {out_bits}")
        
        self.out_bits = out_bits
        
        # Инициализационный вектор
        self.h = IV_512 if out_bits == 512 else IV_256
        
        # Счётчик обработанных бит (mod 2^512)
        self.N = bytes(64)
        
        # Контрольная сумма (сумма блоков mod 2^512)
        self.Sigma = bytes(64)
        
        # Буфер для неполных блоков
        self.buffer = bytearray()
        
        # Флаг финализации
        self._finalized = False
    
    
    def update(self, data: bytes) -> None:
        """
        Добавляет данные в хэш.
        
        Args:
            data: Блок данных произвольной длины
            
        Raises:
            RuntimeError: Если вызвано после final()
        """
        if self._finalized:
            raise RuntimeError("Нельзя вызывать update() после final()")
        
        # Добавляем в буфер
        self.buffer.extend(data)
        
        # Обрабатываем полные блоки по 64 байта
        while len(self.buffer) >= 64:
            block = bytes(self.buffer[:64])
            self.buffer = self.buffer[64:]
            
            self._process_block(block)
    
    
    def _process_block(self, block: bytes) -> None:
        """
        Обрабатывает один полный блок (64 байта).
        
        Обновляет h, N, Σ согласно Этапу 2 стандарта.
        
        Args:
            block: Полный блок сообщения (64 байта)
        """
        assert len(block) == 64
        
        # Применяем функцию сжатия: h := g_N(h, block)
        self.h = g(self.N, self.h, block)
        
        # Обновляем счётчик: N := N ⊞ 512
        block_bits = int_to_bytes(512, 64)
        self.N = add_mod_2n_512(self.N, block_bits)
        
        # Обновляем контрольную сумму: Σ := Σ ⊞ block
        self.Sigma = add_mod_2n_512(self.Sigma, block)
    
    
    def final(self) -> bytes:
        if self._finalized:
            raise RuntimeError("final() уже был вызван")
        self._finalized = True

        # 1) Подготовка последнего блока
        last_len_bits = len(self.buffer) * 8
        last_block = pad_last_block(bytes(self.buffer))  # паддинг сообщения

        # 2) g_N(h, m) ДОЛЖЕН использовать текущий N (до инкремента!)
        self.h = g(self.N, self.h, last_block)

        # 3) Обновить N и Σ ПОСЛЕ g_N, как в RFC
        self.N = add_mod_2n_512(self.N, int_to_bytes(last_len_bits, 64))
        self.Sigma = add_mod_2n_512(self.Sigma, last_block)

        # 4) g_0(h, N) и g_0(h, Σ)
        self.h = g(bytes(64), self.h, self.N)
        self.h = g(bytes(64), self.h, self.Sigma)

        # 5) Усечение для 256 бит
        return self.h[:32] if self.out_bits == 256 else self.h

# ============================================================================
# ФУНКЦИИ-ОБЁРТКИ
# ============================================================================

def hash_512(message: bytes) -> bytes:
    """
    Вычисляет 512-битный хэш сообщения (one-shot).
    
    Args:
        message: Сообщение произвольной длины
        
    Returns:
        Хэш-код (64 байта)
        
    Example:
        >>> hash_512(b"").hex()
        '...'  # известный тест-вектор для пустой строки
    """
    hasher = Streebog(512)
    hasher.update(message)
    return hasher.final()


def hash_256(message: bytes) -> bytes:
    """
    Вычисляет 256-битный хэш сообщения (one-shot).
    
    Args:
        message: Сообщение произвольной длины
        
    Returns:
        Хэш-код (32 байта)
        
    Example:
        >>> hash_256(b"").hex()
        '...'  # известный тест-вектор для пустой строки
    """
    hasher = Streebog(256)
    hasher.update(message)
    return hasher.final()


# ============================================================================
# ТЕСТОВЫЕ ВЕКТОРЫ
# ============================================================================

# Из Приложения А ГОСТ 34.11-2018

TEST_VECTORS_512 = {
    # Пример 1: M_1 (строка "012...012")
    bytes.fromhex(
        "323130393837363534333231303938373635343332313039383736353433323130"
        "393837363534333231303938373635343332313039383736353433323130"
    ): bytes.fromhex(
        "486f64c1917879417fef082b3381a4e211c324f074654c38823a7b76f830ad00"
        "fa1fbae42b1285c0352f227524bc9ab16254288dd6863dccd5b9f54a1ad0541b"
    ),
    
    # Пример 2: M_2 (кириллица)
    bytes.fromhex(
        "fbe2e5f0eee3c820fbeafaebef20fffbf0e1e0f0f520e0ed20e8ece0ebe5f0f2f1"
        "20fff0eeec20f120faf2fee5e2202ce8f6f3ede220e8e6eee1e8f0f2d1202ce8f0"
        "f2e5e220e5d1"
    ): bytes.fromhex(
        "28fbc9bada033b1460642bdcddb90c3fb3e56c497ccd0f62b8a2ad4935e85f03"
        "7613966de4ee00531ae60f3b5a47f8dae06915d5f2f194996fcabf2622e6881e"
    ),
}

TEST_VECTORS_256 = {
    # Пример 1: M_1
    bytes.fromhex(
        "323130393837363534333231303938373635343332313039383736353433323130"
        "393837363534333231303938373635343332313039383736353433323130"
    ): bytes.fromhex(
        "00557be5e584fd52a449b16b0251d05d27f94ab76cbaa6da890b59d8ef1e159d"
    ),
    
    # Пример 2: M_2
    bytes.fromhex(
        "fbe2e5f0eee3c820fbeafaebef20fffbf0e1e0f0f520e0ed20e8ece0ebe5f0f2f1"
        "20fff0eeec20f120faf2fee5e2202ce8f6f3ede220e8e6eee1e8f0f2d1202ce8f0"
        "f2e5e220e5d1"
    ): bytes.fromhex(
        "508f7e553c06501d749a66fc28c6cac0b005746d97537fa85d9e40904efed29d"
    ),
}


# ============================================================================
# САМОТЕСТИРОВАНИЕ
# ============================================================================

def _self_check() -> None:
    """Проверка корректности на тест-векторах из стандарта"""
    
    print("Проверка тест-векторов 512 бит...")
    for message, expected in TEST_VECTORS_512.items():
        result = hash_512(message)
        if result == expected:
            print(f"  ✓ Тест пройден (длина сообщения: {len(message)} байт)")
        else:
            print(f"  ✗ ОШИБКА!")
            print(f"    Ожидалось: {expected.hex()}")
            print(f"    Получено:  {result.hex()}")
            raise AssertionError("Тест-вектор 512 не совпал")
    
    print("\nПроверка тест-векторов 256 бит...")
    for message, expected in TEST_VECTORS_256.items():
        result = hash_256(message)
        if result == expected:
            print(f"  ✓ Тест пройден (длина сообщения: {len(message)} байт)")
        else:
            print(f"  ✗ ОШИБКА!")
            print(f"    Ожидалось: {expected.hex()}")
            print(f"    Получено:  {result.hex()}")
            raise AssertionError("Тест-вектор 256 не совпал")
    
    # Тест потокового API
    print("\nПроверка потокового API...")
    hasher = Streebog(512)
    msg = b"Hello, World!"
    hasher.update(msg[:5])
    hasher.update(msg[5:])
    result_stream = hasher.final()
    result_oneshot = hash_512(msg)
    assert result_stream == result_oneshot, "Потоковый API даёт другой результат"
    print("  ✓ Потоковый API работает корректно")
    
    print("\n✓ Все тесты пройдены успешно!")


if __name__ == "__main__":
    _self_check()
