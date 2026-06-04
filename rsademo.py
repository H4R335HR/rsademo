#!/usr/bin/env python3
"""
RSA Demo - step-by-step, with optional user-supplied values.

Mirrors the classic worked example:
    p = 157, q = 199, e = 163, message x = 13

Run it and press Enter at each prompt to accept the default in [brackets],
or type your own values to experiment.
"""

from math import gcd


# ----------------------------------------------------------------------
# Math helpers
# ----------------------------------------------------------------------
def is_prime(num: int) -> bool:
    """Simple primality test (fine for demo-sized numbers)."""
    if num < 2:
        return False
    if num % 2 == 0:
        return num == 2
    i = 3
    while i * i <= num:
        if num % i == 0:
            return False
        i += 2
    return True


def mod_inverse(e: int, phi: int) -> int:
    """Find d such that (e * d) % phi == 1, via the extended Euclidean algorithm."""
    old_r, r = e, phi
    old_s, s = 1, 0
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
    if old_r != 1:
        raise ValueError(f"e = {e} has no inverse mod {phi} (they are not coprime).")
    return old_s % phi


# ----------------------------------------------------------------------
# Input helpers
# ----------------------------------------------------------------------
def ask_int(prompt: str, default: int) -> int:
    """Prompt for an integer, falling back to a default on empty input."""
    while True:
        raw = input(f"{prompt} [{default}]: ").strip()
        if raw == "":
            return default
        try:
            return int(raw)
        except ValueError:
            print("  Please enter a whole number.")


def ask_prime(prompt: str, default: int) -> int:
    """Prompt for a prime, re-asking until a prime is given."""
    while True:
        value = ask_int(prompt, default)
        if is_prime(value):
            return value
        print(f"  {value} is not prime. Try again.")


def line():
    print("-" * 60)


# ----------------------------------------------------------------------
# Main demo
# ----------------------------------------------------------------------
def main():
    print("=" * 60)
    print(" RSA STEP-BY-STEP DEMO")
    print("=" * 60)
    print("Press Enter to accept the [default] or type your own value.\n")

    # --- Step 1: two primes ------------------------------------------
    print("STEP 1 - Choose two prime numbers")
    p = ask_prime("  p", 157)
    q = ask_prime("  q", 199)
    if p == q:
        print("\n  Note: p and q should be different primes for real RSA.")
    line()

    # --- Step 2: modulus n -------------------------------------------
    n = p * q
    print("STEP 2 - Multiply them to get the modulus n")
    print(f"  n = p * q = {p} * {q} = {n}")
    line()

    # --- Step 3: totient phi -----------------------------------------
    phi = (p - 1) * (q - 1)
    print("STEP 3 - Compute the helper number phi (Euler's totient)")
    print(f"  phi = (p-1)*(q-1) = {p-1} * {q-1} = {phi}")
    line()

    # --- Step 4: public exponent e -----------------------------------
    print("STEP 4 - Choose the public exponent e (must be coprime to phi)")
    while True:
        e = ask_int("  e", 163)
        g = gcd(e, phi)
        if 1 < e < phi and g == 1:
            break
        if g != 1:
            print(f"  gcd(e, phi) = {g}, but it must be 1. Pick another e.")
        else:
            print(f"  e must satisfy 1 < e < {phi}. Pick another e.")
    line()

    # --- Step 5: private exponent d ----------------------------------
    d = mod_inverse(e, phi)
    print("STEP 5 - Compute the private exponent d (the inverse of e mod phi)")
    print(f"  d = {d}")
    print(f"  Check: e * d = {e} * {d} = {e*d}")
    print(f"         (e * d) mod phi = {(e*d) % phi}   <- must be 1")
    line()

    # --- Step 6: the keys --------------------------------------------
    print("STEP 6 - The key pair is ready")
    print(f"  PUBLIC  key (shared)  : (n, e) = ({n}, {e})")
    print(f"  PRIVATE key (secret)  : (n, d) = ({n}, {d})")
    line()

    # --- Step 7: encrypt ---------------------------------------------
    print("STEP 7 - Alice encrypts a message using the PUBLIC key")
    while True:
        x = ask_int("  message x (a number smaller than n)", 13)
        if 0 <= x < n:
            break
        print(f"  x must be between 0 and {n-1} for this to work.")
    y = pow(x, e, n)
    print(f"  y = x^e mod n = {x}^{e} mod {n} = {y}")
    print(f"  Alice sends: {y}")
    line()

    # --- Step 8: decrypt ---------------------------------------------
    print("STEP 8 - Bob decrypts using the PRIVATE key")
    recovered = pow(y, d, n)
    print(f"  x = y^d mod n = {y}^{d} mod {n} = {recovered}")
    line()

    # --- Result ------------------------------------------------------
    print("RESULT")
    if recovered == x:
        print(f"  SUCCESS: Bob recovered the original message ({recovered}).")
    else:
        print(f"  Mismatch: sent {x}, recovered {recovered}.")
    print()
    print("Why it works: e and d are inverses mod phi, so applying e then d")
    print("cancels out. Security: finding d needs phi, which needs factoring n")
    print(f"back into {p} x {q} - trivial here, infeasible for huge primes.")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nExited.")
