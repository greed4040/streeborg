# GOST 34.11-2018 (Streebog) Hash Function

Pure Python implementation of the Russian Federal standard hash function GOST 34.11-2018 (Streebog).

## Features

- ✅ Fully compliant with RFC 6986 (GOST R 34.11-2012) and GOST 34.11-2018
- ✅ Supports both 512-bit and 256-bit hash outputs
- ✅ Pure Python implementation (no external dependencies)
- ✅ Verified against official test vectors

## Installation

```bash
git clone https://github.com/yourusername/streebog.git
cd streebog
pip install -r requirements.txt
```

## Usage

```python
from streebog import hash_512, hash_256

# Calculate 512-bit hash
message = b"Hello, World!"
hash_512_result = hash_512(message)
print(hash_512_result.hex())

# Calculate 256-bit hash
hash_256_result = hash_256(message)
print(hash_256_result.hex())
```

## Project Structure

```
streebog/
├── constants_fixed.py    # Constants and matrices (A, C, Pi, Tau)
├── primitives_fixed.py   # Basic transformations (l, L, S, P, LPS)
├── compression.py        # Compression function g_N
├── streebog.py          # Main hash functions
└── utils.py             # Helper functions
```

## Testing

```bash
# Run basic tests
python test_fixed.py

# Run full hash tests against RFC 6986 vectors
python test_final_hash.py
```

Expected output:
```
✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ!
✅ Реализация соответствует RFC 6986 (ГОСТ 34.11-2018)
```

## Algorithm Overview

GOST 34.11-2018 uses the following transformations:

- **S** - Nonlinear substitution (Pi S-box)
- **P** - Byte permutation (Tau)
- **L** - Linear transformation over GF(2) using matrix A
- **E** - 13-round encryption-like function
- **g_N** - Compression function

## Test Vectors

Verified against RFC 6986 Example 10.1:

**Input:** `M1 = 323130393837363534333231303938373635343332313039383736353433323130393837363534333231303938373635343332313039383736353433323130`

**512-bit hash:** `486f64c1917879417fef082b3381a4e211c324f074654c38823a7b76f830ad00fa1fbae42b1285c0352f227524bc9ab16254288dd6863dccd5b9f54a1ad0541b`

**256-bit hash:** `00557be5e584fd52a449b16b0251d05d27f94ab76cbaa6da890b59d8ef1e159d`

## References

- [RFC 6986](https://datatracker.ietf.org/doc/html/rfc6986) - GOST R 34.11-2012: Hash Function
- [GOST 34.11-2018](https://protect.gost.ru/) - Official standard (in Russian)
- [Streebog.net](https://www.streebog.net/) - Reference information

## License

MIT License

## Contributing

Contributions are welcome! Please ensure all tests pass before submitting a pull request.

## Notes

- Matrix A is sourced from RFC 6986 to ensure correctness
- MSB-first bit ordering is used as specified in the standard
- Compatible with GOST R 34.11-2012 and GOST 34.11-2018
