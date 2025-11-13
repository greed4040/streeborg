# primitives.py
"""
Примитивные преобразования для ГОСТ 34.11-2018 (Стрибог)
Исправленная версия с правильной матрицей A из RFC 6986
"""

from constants import A_MATRIX, PI, TAU


def l(b: bytes) -> bytes:
    """
    Линейное преобразование l: V_64 -> V_64
    
    Умножение вектора b на матрицу A над GF(2).
    
    Формула из RFC 6986:
    c = b_63(Vec_4(a_(0,15))||...||Vec_4(a_(0,0))) ⊕ ... ⊕ 
        b_0(Vec_4(a_(63,15))||...||Vec_4(a_(63,0)))
    
    где если b_i = 0, то результат 0^64
        если b_i = 1, то Vec_4(a_(63-i,15))||...||Vec_4(a_(63-i,0))
    
    Args:
        b: 8 байт входных данных
        
    Returns:
        8 байт выходных данных
    """
    assert len(b) == 8, f"l требует 8 байт, получено {len(b)}"
    
    result = 0
    
    # Обрабатываем каждый байт
    for byte_idx in range(8):
        byte_val = b[byte_idx]
        
        # Обрабатываем каждый бит в байте (MSB-first)
        for bit_in_byte in range(8):
            # Проверяем бит (MSB-first нумерация)
            if byte_val & (1 << (7 - bit_in_byte)):
                # Вычисляем глобальный номер бита
                # Байт 0 содержит биты 63-56 (MSB...LSB)
                # Байт 1 содержит биты 55-48
                # ...
                # Байт 7 содержит биты 7-0
                global_bit = 63 - (byte_idx * 8 + bit_in_byte)
                
                # По формуле RFC: если бит b_i установлен, XOR'им строку A[63-i]
                row_idx = 63 - global_bit
                
                # XOR с соответствующей строкой матрицы
                row = int.from_bytes(A_MATRIX[row_idx], byteorder='big')
                result ^= row
    
    return result.to_bytes(8, byteorder='big')


def S(a: bytes) -> bytes:
    """
    Нелинейное преобразование S: V_512 -> V_512
    
    Применяет подстановку π к каждому байту.
    
    Args:
        a: 64 байта входных данных
        
    Returns:
        64 байта выходных данных
    """
    assert len(a) == 64, f"S требует 64 байта, получено {len(a)}"
    return bytes(PI[byte] for byte in a)


def P(a: bytes) -> bytes:
    """
    Перестановка байтов P: V_512 -> V_512
    
    Применяет перестановку τ к байтам вектора.
    
    Args:
        a: 64 байта входных данных
        
    Returns:
        64 байта выходных данных с переставленными байтами
    """
    assert len(a) == 64, f"P требует 64 байта, получено {len(a)}"
    return bytes(a[TAU[i]] for i in range(64))


def L(a: bytes) -> bytes:
    """
    Линейное преобразование L: V_512 -> V_512
    
    Применяет преобразование l к каждому 8-байтовому блоку.
    
    L(a) = L(a_7||...||a_0) = l(a_7)||...||l(a_0)
    
    где a_7, ..., a_0 - это 8 блоков по 8 байт каждый.
    
    Args:
        a: 64 байта входных данных
        
    Returns:
        64 байта выходных данных
    """
    assert len(a) == 64, f"L требует 64 байта, получено {len(a)}"
    
    # Разбиваем на 8 блоков по 8 байт
    result = bytearray()
    for i in range(8):
        block_start = i * 8
        block_end = block_start + 8
        block = a[block_start:block_end]
        result.extend(l(block))
    
    return bytes(result)


def X(k: bytes, a: bytes) -> bytes:
    """
    XOR преобразование X[k]: V_512 -> V_512
    
    X[k](a) = k ⊕ a
    
    Args:
        k: 64 байта ключа
        a: 64 байта данных
        
    Returns:
        64 байта результата XOR
    """
    assert len(k) == 64, f"X требует ключ 64 байта, получено {len(k)}"
    assert len(a) == 64, f"X требует данные 64 байта, получено {len(a)}"
    
    return bytes(k[i] ^ a[i] for i in range(64))


# Композиции преобразований
def LPS(a: bytes) -> bytes:
    """Композиция L ∘ P ∘ S"""
    return L(P(S(a)))


def LPSX(k: bytes, a: bytes) -> bytes:
    """Композиция L ∘ P ∘ S ∘ X[k]"""
    return LPS(X(k, a))