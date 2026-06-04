# RSA Step-by-Step Demo

An interactive, classroom-friendly Python script that walks through the **RSA public-key algorithm** one step at a time. Run it with the built-in textbook example, or plug in your own primes and message to experiment.

No dependencies, no setup — just the Python standard library.

---

## What it does

The script prints all eight stages of RSA with the actual numbers substituted in, so learners can see *how* a key pair is built and *why* decryption recovers the original message:

1. Choose two primes `p` and `q`
2. Compute the modulus `n = p × q`
3. Compute Euler's totient `phi = (p−1)(q−1)`
4. Choose the public exponent `e` (must be coprime to `phi`)
5. Compute the private exponent `d` (the modular inverse of `e`)
6. Assemble the public key `(n, e)` and private key `(n, d)`
7. **Encrypt:** `y = xᵉ mod n`
8. **Decrypt:** `x = yᵈ mod n`

Every value the user enters is validated: non-primes are rejected, a bad `e` is refused with the reason (`gcd(e, phi) ≠ 1`), and the message is bounded below `n`.

---

## Requirements

- Python 3.6 or newer
- Standard library only (`math`) — nothing to install

---

## Usage

```bash
python3 rsademo.py
```

Press **Enter** at any prompt to accept the default in `[brackets]`, or type your own value.

The defaults reproduce the classic worked example: `p = 157`, `q = 199`, `e = 163`, message `x = 13`.

### Example session (using all defaults)

```
STEP 1 - Choose two prime numbers
  p [157]:
  q [199]:
------------------------------------------------------------
STEP 2 - Multiply them to get the modulus n
  n = p * q = 157 * 199 = 31243
------------------------------------------------------------
STEP 3 - Compute the helper number phi (Euler's totient)
  phi = (p-1)*(q-1) = 156 * 198 = 30888
------------------------------------------------------------
STEP 4 - Choose the public exponent e (must be coprime to phi)
  e [163]:
------------------------------------------------------------
STEP 5 - Compute the private exponent d (the inverse of e mod phi)
  d = 379
  Check: e * d = 163 * 379 = 61777
         (e * d) mod phi = 1   <- must be 1
------------------------------------------------------------
STEP 6 - The key pair is ready
  PUBLIC  key (shared)  : (n, e) = (31243, 163)
  PRIVATE key (secret)  : (n, d) = (31243, 379)
------------------------------------------------------------
STEP 7 - Alice encrypts a message using the PUBLIC key
  message x (a number smaller than n) [13]:
  y = x^e mod n = 13^163 mod 31243 = 16341
  Alice sends: 16341
------------------------------------------------------------
STEP 8 - Bob decrypts using the PRIVATE key
  x = y^d mod n = 16341^379 mod 31243 = 13
------------------------------------------------------------
RESULT
  SUCCESS: Bob recovered the original message (13).
```

---

## How RSA works, briefly

The whole scheme rests on a single relationship: `e` and `d` are chosen so that `e × d ≡ 1 (mod phi)`. That makes raising a number to `e` and then to `d` cancel out, modulo `n`:

```
(xᵉ)ᵈ = x^(e·d) = x^(1 + k·phi) = x · (x^phi)ᵏ ≡ x · 1 = x  (mod n)
```

The middle collapse is **Euler's theorem** (`x^phi ≡ 1 mod n`).

**Why it's secure:** to compute the private exponent `d`, an attacker needs `phi`, and to get `phi` they must factor `n` back into `p × q`. With the tiny primes used here that is instant — but with 2048-bit primes it is, as far as is publicly known, computationally infeasible. That asymmetry is the "trapdoor" RSA is built on.

---

## Educational notes & limitations

This is a **teaching tool**, not a secure implementation. In particular:

- The primes are far too small — `n` can be factored instantly.
- It implements *textbook* RSA: no padding (real RSA uses OAEP), which is deterministic and malleable.
- It encrypts a single number below `n`, not arbitrary-length data. Real systems use RSA only to wrap a symmetric key, then encrypt the actual data with that.

Do not use this to protect real secrets.

---

## Possible extensions

A few directions worth adding for the classroom:

- **Attack mode** — factor `n` to derive the private key, demonstrating exactly what breaks when primes are small.
- **Text support** — map characters to numbers so students can encrypt short words.
- **Square-and-multiply trace** — show the fast modular exponentiation steps behind `pow(base, exp, mod)`.

---

## License

Released under the MIT License. Free to use, modify, and share — including in coursework and workshops.
