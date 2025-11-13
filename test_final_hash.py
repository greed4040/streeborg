#!/usr/bin/env python3
"""
Финальный тест полного хэша на тест-векторах RFC 6986
"""

# ВАЖНО: перед запуском обновите импорты в файлах:
# compression.py, streebog.py, utils.py
# 


try:
    from streebog import hash_512, hash_256
    
    # Тест-вектор M1 из RFC 6986 (пример 10.1)
    M1 = bytes.fromhex(
        "323130393837363534333231303938373635343332313039383736353433323130"
        "393837363534333231303938373635343332313039383736353433323130"
    )
    
    # Ожидаемые результаты
    EXPECTED_512 = bytes.fromhex(
        "486f64c1917879417fef082b3381a4e211c324f074654c38823a7b76f830ad00"
        "fa1fbae42b1285c0352f227524bc9ab16254288dd6863dccd5b9f54a1ad0541b"
    )
    
    EXPECTED_256 = bytes.fromhex(
        "00557be5e584fd52a449b16b0251d05d27f94ab76cbaa6da890b59d8ef1e159d"
    )
    
    print("="*70)
    print("ФИНАЛЬНЫЙ ТЕСТ ХЭША ГОСТ 34.11-2018 (RFC 6986)")
    print("="*70)
    
    # Тест 512 бит
    print("\nТЕСТ 1: hash_512(M1)")
    print(f"M1 = {M1.hex()[:32]}...")
    
    try:
        result_512 = hash_512(M1)
        print(f"\nРезультат: {result_512.hex()}")
        print(f"Ожидалось: {EXPECTED_512.hex()}")
        
        if result_512 == EXPECTED_512:
            print("\n🎉 ✓ PASS - ХЭШИ СОВПАДАЮТ!")
        else:
            print("\n❌ ✗ FAIL - хэши не совпадают")
            # Покажем где различия
            for i in range(min(len(result_512), len(EXPECTED_512))):
                if result_512[i] != EXPECTED_512[i]:
                    print(f"   Первое различие на байте {i}: {result_512[i]:02x} vs {EXPECTED_512[i]:02x}")
                    break

    except Exception as e:
        print(f"\n❌ Ошибка при вычислении hash_512: {e}")
        import traceback
        traceback.print_exc()
    
    # Тест 256 бит
    print("\n" + "="*70)
    print("ТЕСТ 2: hash_256(M1)")
    
    try:
        result_256 = hash_256(M1)
        print(f"\nРезультат: {result_256.hex()}")
        print(f"Ожидалось: {EXPECTED_256.hex()}")
        
        if result_256 == EXPECTED_256:
            print("\n🎉 ✓ PASS - ХЭШИ СОВПАДАЮТ!")
        else:
            print("\n❌ ✗ FAIL - хэши не совпадают")
    except Exception as e:
        print(f"\n❌ Ошибка при вычислении hash_256: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*70)
    print("ИТОГО:")
    print("="*70)
    if result_512 == EXPECTED_512 and result_256 == EXPECTED_256:
        print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
        print("✅ Реализация соответствует RFC 6986 (ГОСТ 34.11-2018)")
    else:
        print("❌ ЕСТЬ ОШИБКИ - проверьте импорты")
    
except ImportError as e:
    print("="*70)
    print("ОШИБКА ИМПОРТА")
    print("="*70)
    print(f"\n{e}\n")
    print("НУЖНО обновить импорты в файлах:")
    print("  • compression.py")
    print("  • streebog.py")
    print("  • utils.py")

