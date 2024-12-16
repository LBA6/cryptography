# cryptography
Project for Cryptography and Data Security Technologies

The ElGamal encryption system is an asymmetric key encryption algorithm based on the Diffie-Hellman key exchange. It operates on the principles of discrete logarithms in multiplicative groups of integers modulo a prime. Here's an explanation of the key principles:
1. Key Generation:
- A large prime number q is chosen.
- A generator g of the multiplicative group of integers modulo q is selected.
- A private key a is randomly chosen.
- The public key is calculated as h = g^a mod q.

2. Encryption:
- To encrypt a message m, the sender:
  - Chooses a random ephemeral key k.
  - Computes p = g^k mod q (the public ephemeral key).
  - Computes s = h^k mod q (the shared secret).
  - Encrypts the message as c = m * s mod q.
- The ciphertext consists of the pair (p, c).

3.Decryption:
- To decrypt, the receiver:
  - Uses their private key a to compute s = p^a mod q.
  - Recovers the message by calculating m = c * s^(-1) mod q.

The security of ElGamal relies on the difficulty of the Discrete Logarithm Problem. Even if an attacker knows g, h, and p, it's computationally infeasible to determine k or a, which are needed to derive the shared secret s.
