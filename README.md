# Cryptography project
Project for Cryptography and Data Security Technologies

# ElGamal Encryption

This is a Python implementation of the ElGamal encryption system, an asymmetric key encryption algorithm based on the Diffie-Hellman key exchange and the Discrete Logarithm Problem.

## Key Components

1. **Key Generation**
   - Large prime number `q`
   - Generator `g` of the multiplicative group of integers modulo `q`
   - Private key `key`
   - Public key `h = g^key mod q`

2. **Encryption**
   - Ephemeral key `k`
   - Public ephemeral key `p = g^k mod q`
   - Shared secret `s = h^k mod q`
   - Ciphertext `c = m * s mod q`

3. **Decryption**
   - Shared secret `s = p^key mod q`
   - Plaintext `m = c * s^(-1) mod q`

## Usage

import random
from math import pow

### Function to calculate the Greatest Common Divisor (GCD) using the Euclidean algorithm
```python
def gcd(x, y):
    if x < y:
        return gcd(y, x)
    elif x % y == 0:
        return y
    else:
        return gcd(y, x % y)
```

### Function to generate a random key that is coprime with prime_nb
```python
def gen_key(prime_nb):
    key = random.randint(2, prime_nb - 1)
    while gcd(prime_nb, key) != 1:
        key = random.randint(2, prime_nb - 1)
    return key
```

### Function to encrypt the message
```python
def encrypt(msg, prime_nb, dest_pub_key, gen):
    key = gen_key(prime_nb)  # Ephemeral private key
    shared_secret = pow(dest_pub_key, key, prime_nb)  # Shared secret
    pub_key = pow(gen, key, prime_nb)  # Public ephemeral key

    enc_msg = [(ord(char) * shared_secret) % prime_nb for char in msg]  # Encrypt each character
    return enc_msg, pub_key
```

### Function to decrypt the message
```python
def decrypt(enc_msg, pub_key, priv_key, prime_nb):
    shared_secret = pow(pub_key, priv_key, prime_nb)  # Shared secret
    s_inv = pow(shared_secret, -1, prime_nb)  # Modular inverse of shared secret

    dec_msg = [chr((char * s_inv) % prime_nb) for char in enc_msg]  # Decrypt each character
    return dec_msg
```

### Main execution
```python
# Shared prime and generator for both users
prime_nb = number.getPrime(1024)  # Large prime number
gen = random.randint(2, prime_nb - 1)  # Generator of the multiplicative group

# User 1 keys
U1_priv_key = gen_key(prime_nb)  # Private key
U1_pub_key = pow(gen, U1_priv_key, prime_nb)  # Public key

# User 2 keys
U2_priv_key = gen_key(prime_nb)  # Private key
U2_pub_key = pow(gen, U2_priv_key, prime_nb)  # Public key

# User 1 sends a message to User 2
msg = input("User 1: Enter your message: ")
enc_msg, pub_key = encrypt(msg, prime_nb, U2_pub_key, gen)

print("\nEncrypted message (sent to User 2):", enc_msg)

# User 2 decrypts the message
dec_msg = decrypt(enc_msg, pub_key, U2_priv_key, prime_nb)
plaintext = ''.join(dec_msg)

print("User 2: Decrypted message:", plaintext)
```
