#!/usr/bin/env python3
"""Encrypt data.json -> data.enc.json for the passcode-gated dashboard.

Usage:
    python3 encrypt_data.py <passcode>
    (run from the project root; reads ./data.json, writes ./data.enc.json)

Format: PBKDF2-HMAC-SHA256 (310,000 iterations) -> AES-256-GCM.
The browser decrypts with WebCrypto using the same parameters.
"""
import base64
import json
import os
import sys
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

ITERATIONS = 310_000

def main():
    if len(sys.argv) != 2:
        sys.exit("usage: encrypt_data.py <passcode>")
    passcode = sys.argv[1].encode("utf-8")

    with open("data.json", "rb") as f:
        plaintext = f.read()
    json.loads(plaintext)  # validate JSON before encrypting

    salt = os.urandom(16)
    iv = os.urandom(12)
    key = hashlib.pbkdf2_hmac("sha256", passcode, salt, ITERATIONS, dklen=32)
    ct = AESGCM(key).encrypt(iv, plaintext, None)

    out = {
        "v": 1,
        "kdf": "PBKDF2-SHA256",
        "iter": ITERATIONS,
        "salt": base64.b64encode(salt).decode(),
        "iv": base64.b64encode(iv).decode(),
        "ct": base64.b64encode(ct).decode(),
    }
    with open("data.enc.json", "w") as f:
        json.dump(out, f)
    print(f"OK: encrypted {len(plaintext)} bytes -> data.enc.json")

if __name__ == "__main__":
    main()
