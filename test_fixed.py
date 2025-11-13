# test_fixed.py
"""
Финальный тест исправленной реализации ГОСТ 34.11-2018
"""

from primitives import l, L

# Тест из RFC 6986, страница 13
# После S(h ⊕ N) = fcfc...fc (64 байта)
# После L: K = b383fc2eced4a574b383fc2eced4a574... (повторяется 8 раз)

print("="*70)
print("ФИНАЛЬНЫЙ ТЕСТ ИСПРАВЛЕННОЙ РЕАЛИЗАЦИИ")
print("="*70)

# ТЕСТ 1: l(fcfcfcfcfcfcfcfc) = b383fc2eced4a574
test1_input = bytes([0xfc] * 8)
test1_expected = bytes.fromhex("b383fc2eced4a574")
test1_result = l(test1_input)

print(f"\nТЕСТ 1: l(fcfcfcfcfcfcfcfc)")
print(f"  Вход:      {test1_input.hex()}")
print(f"  Результат: {test1_result.hex()}")
print(f"  Ожидалось: {test1_expected.hex()}")
print(f"  Статус:    {'✓ PASS' if test1_result == test1_expected else '✗ FAIL'}")

# ТЕСТ 2: L(fcfc...fc × 64 байта)
test2_input = bytes([0xfc] * 64)
test2_expected = bytes.fromhex("b383fc2eced4a574") * 8
test2_result = L(test2_input)

print(f"\nТЕСТ 2: L(fcfcfcfc... × 64 байта)")
print(f"  Результат (первые 8 байт): {test2_result[:8].hex()}")
print(f"  Ожидалось (первые 8 байт): {test2_expected[:8].hex()}")
print(f"  Статус: {'✓ PASS' if test2_result == test2_expected else '✗ FAIL'}")

# ТЕСТ 3: Проверка, что все 8 блоков одинаковы
all_blocks_same = all(
    test2_result[i*8:(i+1)*8] == test2_result[0:8]
    for i in range(8)
)
print(f"\nТЕСТ 3: Все 8 блоков по 8 байт одинаковы")
print(f"  Статус: {'✓ PASS' if all_blocks_same else '✗ FAIL'}")

# ТЕСТ 4: l(8000000000000000) = A[0]
from constants import A_MATRIX
test4_input = bytes.fromhex("8000000000000000")
test4_expected = A_MATRIX[0]
test4_result = l(test4_input)

print(f"\nТЕСТ 4: l(8000000000000000) = A[0]")
print(f"  Вход:      {test4_input.hex()}")
print(f"  Результат: {test4_result.hex()}")
print(f"  A[0]:      {test4_expected.hex()}")
print(f"  Статус:    {'✓ PASS' if test4_result == test4_expected else '✗ FAIL'}")

print(f"\n{'='*70}")
if all([
    test1_result == test1_expected,
    test2_result == test2_expected,
    all_blocks_same,
    test4_result == test4_expected
]):
    print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ! Реализация исправлена!")
else:
    print("❌ ЕСТЬ ПРОВАЛЕННЫЕ ТЕСТЫ")
print("="*70)