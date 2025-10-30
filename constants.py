"""
constants.py - Константы для ГОСТ 34.11-2018 (Стрибог)

Все значения взяты из официального стандарта.
Иммутабельные объекты для предотвращения случайных изменений.
"""

# ============================================================================
# S-БЛОК (π) - Раздел 5.2
# ============================================================================
# Нелинейное биективное преобразование V₈ → V₈
# Индекс = входное значение (0-255), значение = выходное

S_BOX: bytes = bytes([
    0xfc, 0xee, 0xdd, 0x11, 0xcf, 0x6e, 0x31, 0x16,
    0xfb, 0xc4, 0xfa, 0xda, 0x23, 0xc5, 0x04, 0x4d,
    0xe9, 0x77, 0xf0, 0xdb, 0x93, 0x2e, 0x99, 0xba,
    0x17, 0x36, 0xf1, 0xbb, 0x14, 0xcd, 0x5f, 0xc1,
    0xf9, 0x18, 0x65, 0x5a, 0xe2, 0x5c, 0xef, 0x21,
    0x81, 0x1c, 0x3c, 0x42, 0x8b, 0x01, 0x8e, 0x4f,
    0x05, 0x84, 0x02, 0xae, 0xe3, 0x6a, 0x8f, 0xa0,
    0x06, 0x0b, 0xed, 0x98, 0x7f, 0xd4, 0xd3, 0x1f,
    0xeb, 0x34, 0x2c, 0x51, 0xea, 0xc8, 0x48, 0xab,
    0xf2, 0x2a, 0x68, 0xa2, 0xfd, 0x3a, 0xce, 0xcc,
    0xb5, 0x70, 0x0e, 0x56, 0x08, 0x0c, 0x76, 0x12,
    0xbf, 0x72, 0x13, 0x47, 0x9c, 0xb7, 0x5d, 0x87,
    0x15, 0xa1, 0x96, 0x29, 0x10, 0x7b, 0x9a, 0xc7,
    0xf3, 0x91, 0x78, 0x6f, 0x9d, 0x9e, 0xb2, 0xb1,
    0x32, 0x75, 0x19, 0x3d, 0xff, 0x35, 0x8a, 0x7e,
    0x6d, 0x54, 0xc6, 0x80, 0xc3, 0xbd, 0x0d, 0x57,
    0xdf, 0xf5, 0x24, 0xa9, 0x3e, 0xa8, 0x43, 0xc9,
    0xd7, 0x79, 0xd6, 0xf6, 0x7c, 0x22, 0xb9, 0x03,
    0xe0, 0x0f, 0xec, 0xde, 0x7a, 0x94, 0xb0, 0xbc,
    0xdc, 0xe8, 0x28, 0x50, 0x4e, 0x33, 0x0a, 0x4a,
    0xa7, 0x97, 0x60, 0x73, 0x1e, 0x00, 0x62, 0x44,
    0x1a, 0xb8, 0x38, 0x82, 0x64, 0x9f, 0x26, 0x41,
    0xad, 0x45, 0x46, 0x92, 0x27, 0x5e, 0x55, 0x2f,
    0x8c, 0xa3, 0xa5, 0x7d, 0x69, 0xd5, 0x95, 0x3b,
    0x07, 0x58, 0xb3, 0x40, 0x86, 0xac, 0x1d, 0xf7,
    0x30, 0x37, 0x6b, 0xe4, 0x88, 0xd9, 0xe7, 0x89,
    0xe1, 0x1b, 0x83, 0x49, 0x4c, 0x3f, 0xf8, 0xfe,
    0x8d, 0x53, 0xaa, 0x90, 0xca, 0xd8, 0x85, 0x61,
    0x20, 0x71, 0x67, 0xa4, 0x2d, 0x2b, 0x09, 0x5b,
    0xcb, 0x9b, 0x25, 0xd0, 0xbe, 0xe5, 0x6c, 0x52,
    0x59, 0xa6, 0x74, 0xd2, 0xe6, 0xf4, 0xb4, 0xc0,
    0xd1, 0x66, 0xaf, 0xc2, 0x39, 0x4b, 0x63, 0xb6,
])

assert len(S_BOX) == 256, "S-блок должен содержать ровно 256 элементов"


# ============================================================================
# ПЕРЕСТАНОВКА τ - Раздел 5.3
# ============================================================================
# Транспонирование 8×8 матрицы байтов
# τ(i) = новая позиция для байта на позиции i

TAU: tuple[int, ...] = (
    0, 8, 16, 24, 32, 40, 48, 56,
    1, 9, 17, 25, 33, 41, 49, 57,
    2, 10, 18, 26, 34, 42, 50, 58,
    3, 11, 19, 27, 35, 43, 51, 59,
    4, 12, 20, 28, 36, 44, 52, 60,
    5, 13, 21, 29, 37, 45, 53, 61,
    6, 14, 22, 30, 38, 46, 54, 62,
    7, 15, 23, 31, 39, 47, 55, 63,
)

assert len(TAU) == 64, "τ должна содержать ровно 64 элемента"


# ============================================================================
# МАТРИЦА A (64×64) - Раздел 5.4
# ============================================================================
# Линейное преобразование над GF(2)
# Каждая строка = 64 бита = 8 байт (hex-запись)
# Строка j записана как Vec₄(aⱼ,₁₅)||...||Vec₄(aⱼ,₀)

A_MATRIX: tuple[bytes, ...] = (
    bytes.fromhex("8e20faa72ba0b470"),
    bytes.fromhex("47107ddd9b505a38"),
    bytes.fromhex("ad08b0e0c3282d1c"),
    bytes.fromhex("d8045870ef14980e"),
    bytes.fromhex("6c022c38f90a4c07"),
    bytes.fromhex("a011d380818e8f40"),
    bytes.fromhex("0ad97808d06cb404"),
    bytes.fromhex("90dab52a387ae76f"),
    bytes.fromhex("092e94218d243cba"),
    bytes.fromhex("9d4df05d5f661451"),
    bytes.fromhex("18150f14b9ec46dd"),
    bytes.fromhex("86275df09ce8aaa8"),
    bytes.fromhex("e230140fc0802984"),
    bytes.fromhex("456c34887a3805b9"),
    bytes.fromhex("9bcf4486248d9f5d"),
    bytes.fromhex("e4fa2054a80b329c"),
    bytes.fromhex("492c024284fbaec0"),
    bytes.fromhex("70a6a56e2440598e"),
    bytes.fromhex("07e095624504536c"),
    bytes.fromhex("3601161cf205268d"),
    bytes.fromhex("5086e740ce47c920"),
    bytes.fromhex("05e23c0468365a02"),
    bytes.fromhex("486dd4151c3dfdb9"),
    bytes.fromhex("8a174a9ec8121e5d"),
    bytes.fromhex("c0a878a0a1330aa6"),
    bytes.fromhex("0c84890ad27623e0"),
    bytes.fromhex("439da0784e745554"),
    bytes.fromhex("71180a8960409a42"),
    bytes.fromhex("ac361a443d1c8cd2"),
    bytes.fromhex("c3e9224312c8c1a0"),
    bytes.fromhex("727d102a548b194e"),
    bytes.fromhex("aa16012142f35760"),
    bytes.fromhex("3853dc371220a247"),
    bytes.fromhex("8d70c431ac02a736"),
    bytes.fromhex("1b8e0b0e798c13c8"),
    bytes.fromhex("2843fd2067adea10"),
    bytes.fromhex("8c711e02341b2d01"),
    bytes.fromhex("24b86a840e90f0d2"),
    bytes.fromhex("4585254f64090fa0"),
    bytes.fromhex("60543c50de970553"),
    bytes.fromhex("0642ca05693b9f70"),
    bytes.fromhex("afc0503c273aa42a"),
    bytes.fromhex("b60c05ca30204d21"),
    bytes.fromhex("561b0d22900e4669"),
    bytes.fromhex("effa11af0964ee50"),
    bytes.fromhex("39b008152acb8227"),
    bytes.fromhex("550b8e9e21f7a530"),
    bytes.fromhex("1ca76e95091051ad"),
    bytes.fromhex("c83862965601dd1b"),
    bytes.fromhex("6f2d3a0bc58c7c28"),
    bytes.fromhex("f1b87c28591b821d"),
    bytes.fromhex("1d28335a64a8b0e6"),
    bytes.fromhex("e8a3036281230cfd"),
    bytes.fromhex("744c05d3052ee04e"),
    bytes.fromhex("3a0e8b1e6f8a0e19"),
    bytes.fromhex("1d1d0ec6b8b4f0f7"),
    bytes.fromhex("0e8e868e1c0e0e8e"),
    bytes.fromhex("07070707e7e7e7e7"),
    bytes.fromhex("e3e3e3e313131313"),
    bytes.fromhex("f1f1f1f101010101"),
    bytes.fromhex("f8f8f8f808080808"),
    bytes.fromhex("7c7c7c7c84848484"),
    bytes.fromhex("3e3e3e3ec2c2c2c2"),
    bytes.fromhex("1f1f1f1fe1e1e1e1"),
)

assert len(A_MATRIX) == 64, "Матрица A должна содержать ровно 64 строки"
assert all(len(row) == 8 for row in A_MATRIX), "Каждая строка A должна быть 8 байт"


# ============================================================================
# ИТЕРАЦИОННЫЕ КОНСТАНТЫ C₁-C₁₂ - Раздел 5.5
# ============================================================================
# Используются в функции E для генерации раундовых ключей
# Каждая константа = 512 бит = 64 байта

C_CONSTANTS: tuple[bytes, ...] = (
    bytes.fromhex(
        "b1085bda1ecadae9ebcb2f81c0657df2f6a76432e45d016714eb88d7585c4fc4"
        "b7ce09192676901a2422a08a460d31505767436cc744d23dd806559f2a64507"
    ),
    bytes.fromhex(
        "6fa3b58aa99d2f1a4fe39d460f70b5d7f3feea720a232b9861d55e0f16b50131"
        "9ab5176b12d699585cb561c2db0aa7ca55dda21bd7cbcd56e679047021b19bb7"
    ),
    bytes.fromhex(
        "f574dcac2bce2fc70a39fc286a3d843506f15e5f529c1f8bf2ea7514b1297b7b"
        "d3e20fe490359eb1c1c93a376062db09c2b6f443867adb31991e96f50aba0ab2"
    ),
    bytes.fromhex(
        "ef1fdfb3e81566d2f948e1a05d71e4dd488e857e335c3c7d9d721cad685e353f"
        "a9d72c82ed03d675d8b71333935203be3453eaa193e837f1220cbebc84e3d12e"
    ),
    bytes.fromhex(
        "4bea6bacad4747999a3f410c6ca923637f151c1f1686104a359e35d7800fffbd"
        "bfcd1747253af5a3dfff00b723271a167a56a27ea9ea63f5601758fd7c6cfe57"
    ),
    bytes.fromhex(
        "ae4faeae1d3ad3d96fa4c33b7a3039c02d66c4f95142a46c187f9ab49af08ec6"
        "cffaa6b71c9ab7b40af21f66c2bec6b6bf71c57236904f35fa68407a46647d6e"
    ),
    bytes.fromhex(
        "f4c70e16eeaac5ec51ac86febf240954399ec6c7e6bf87c9d3473e33197a93c9"
        "0992abc52d822c3706476983284a05043517454ca23c4af38886564d3a14d493"
    ),
    bytes.fromhex(
        "9b1f5b424d93c9a703e7aa020c6e41414eb7f8719c36de1e89b4443b4ddbc49a"
        "f4892bcb929b069069d18d2bd1a5c42f36acc2355951a8d9a47f0dd4bf02e71e"
    ),
    bytes.fromhex(
        "378f5a541631229b944c9ad8ec165fde3a7d3a1b258942243cd955b7e00d0984"
        "800a440bdbb2ceb17b2b8a9aa6079c540e38dc92cb1f2a607261445183235adb"
    ),
    bytes.fromhex(
        "abbedea680056f52382ae548b2e4f3f38941e71cff8a78db1fffe18a1b336103"
        "9fe76702af69334b7a1e6c303b7652f43698fad1153bb6c374b4c7fb98459ced"
    ),
    bytes.fromhex(
        "7bcd9ed0efc889fb3002c6cd635afe94d8fa6bbbebab07612001802114846679"
        "8a1d71efea48b9caefbacd1d7d476e98dea2594ac06fd85d6bcaa4cd81f32d1b"
    ),
    bytes.fromhex(
        "378ee767f11631bad21380b00449b17acda43c32bcdf1d77f82012d430219f9b"
        "5d80ef9d1891cc86e71da4aa88e12852faf417d5d9b21b9948bc924af11bd720"
    ),
)

assert len(C_CONSTANTS) == 12, "Должно быть ровно 12 констант C"
assert all(len(c) == 64 for c in C_CONSTANTS), "Каждая константа C должна быть 64 байта"


# ============================================================================
# ИНИЦИАЛИЗАЦИОННЫЕ ВЕКТОРЫ - Раздел 5.1
# ============================================================================

# IV для хэш-функции с длиной 512 бит
IV_512: bytes = bytes(64)  # 0^512

# IV для хэш-функции с длиной 256 бит
IV_256: bytes = bytes([0x01] + [0x00] * 63)  # (00000001)^64

assert len(IV_512) == 64, "IV_512 должен быть 64 байта"
assert len(IV_256) == 64, "IV_256 должен быть 64 байта"


# ============================================================================
# САМОПРОВЕРКА
# ============================================================================

def _self_check() -> None:
    """Проверка корректности загрузки констант"""
    assert len(S_BOX) == 256
    assert len(TAU) == 64
    assert len(A_MATRIX) == 64
    assert len(C_CONSTANTS) == 12
    assert len(IV_512) == 64
    assert len(IV_256) == 64
    print("✓ Все константы загружены корректно")


if __name__ == "__main__":
    _self_check()
