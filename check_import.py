#!/usr/bin/env python3
"""
Проверка и обновление импортов в файлах
"""
import re
import shutil
from pathlib import Path

files_to_check = ['compression.py', 'streebog.py', 'utils.py']

print("="*70)
print("ПРОВЕРКА ИМПОРТОВ")
print("="*70)

for filename in files_to_check:
    filepath = Path(filename)
    if not filepath.exists():
        print(f"\n❌ {filename} не найден")
        continue
    
    content = filepath.read_text()
    
    # Проверяем импорты
    has_old_constants = 'from constants import' in content
    has_old_primitives = 'from primitives import' in content
    
    print(f"\n📄 {filename}:")
    if has_old_constants:
        print("  ⚠️  Найден: from constants import")
    if has_old_primitives:
        print("  ⚠️  Найден: from primitives import")
    
    if not has_old_constants and not has_old_primitives:
        print("  ✓ Импорты уже обновлены")

print("\n" + "="*70)
print("ВАРИАНТЫ:")
print("="*70)


print("\nзапустить:")
print("   python test_final_hash.py")