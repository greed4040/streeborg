#!/usr/bin/env python3
"""
Полный тест хэш-функции на тест-векторе M1 из RFC 6986
"""
#import sys
#sys.path.insert(0, '/mnt/user-data/outputs')

# Замените импорты на ваши файлы
from constants import IV_512, IV_256
from primitives import LPS, X, S, P, L

# Тест-вектор M1 из RFC 6986 (пример 10.1, стр. 13)
M1 = bytes.fromhex(
    "323130393837363534333231303938373635343332313039383736353433323130"
    "393837363534333231303938373635343332313039383736353433323130"
)

# Ожидаемые результаты из RFC 6986
EXPECTED_512 = bytes.fromhex(
    "486f64c1917879417fef082b3381a4e211c324f074654c38823a7b76f830ad00"
    "fa1fbae42b1285c0352f227524bc9ab16254288dd6863dccd5b9f54a1ad0541b"
)

EXPECTED_256 = bytes.fromhex(
    "00557be5e584fd52a449b16b0251d05d27f94ab76cbaa6da890b59d8ef1e159d"
)

print("="*70)
print("ТЕСТ ПОЛНОЙ ХЭШ-ФУНКЦИИ ГОСТ 34.11-2018")
print("="*70)
print(f"\nM1 (первые 32 байта): {M1[:32].hex()}")
print(f"Длина: {len(M1)} байт = {len(M1)*8} бит")

# КРИТИЧЕСКИЙ ТЕСТ: LPS(0^512) должен дать K из примера
print("\n" + "="*70)
print("ТЕСТ LPS(0^512) - первый шаг из RFC 6986")
print("="*70)

h_xor_n = bytes(64)  # 0^512
result_lps = LPS(h_xor_n)

# Из RFC 6986, стр. 13: после L должно быть
expected_k = bytes.fromhex("b383fc2eced4a574") * 8

print(f"\nПосле S(0^512):  {'fc' * 64}")
print(f"После P:         {'fc' * 64}  (все байты одинаковы)")
print(f"После L (K[1]):  {result_lps[:16].hex()}...")
print(f"Ожидалось:       {expected_k[:16].hex()}...")
print(f"Статус: {'✓ PASS' if result_lps == expected_k else '✗ FAIL'}")

if result_lps != expected_k:
    print("\n⚠️  ОШИБКА: LPS не работает правильно!")
    print("   Проверьте S, P, L преобразования")
    sys.exit(1)

print("\n✓ LPS работает правильно!")
print("\n" + "="*70)
print("ДЛЯ ПОЛНОГО ТЕСТА НУЖНЫ:")
print("="*70)
print("1. compression.py - функция сжатия g_N")
print("2. streebog.py - основная функция hash_512/hash_256")
print("3. utils.py - вспомогательные функции")

print("\nзапустить полный тест хэша:")
print("  from streebog import hash_512")
print("  result = hash_512(M1)")
print(f"  expected = {EXPECTED_512.hex()[:32]}...")