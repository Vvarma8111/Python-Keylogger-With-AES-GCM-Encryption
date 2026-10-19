#!/usr/bin/env python3
"""
AES-256-GCM file encrypt/decrypt using a default hard-coded password.

Default password: "Varma@8135"

Usage examples:
  # Encrypt using the built-in password (default)
  python3 aes_file_encrypt_decrypt_with_default_password.py encrypt -i vv.txt -o vv.txt.enc

  # Decrypt using the built-in password (default)
  python3 aes_file_encrypt_decrypt_with_default_password.py decrypt -i vv.txt.enc -o vv_decrypted.txt

  # Encrypt using an explicit password (overrides the built-in)
  python3 aes_file_encrypt_decrypt_with_default_password.py encrypt -i vv.txt -o vv.txt.enc --password MySecret123

  # Decrypt using an explicit password
  python3 aes_file_encrypt_decrypt_with_default_password.py decrypt -i vv.txt.enc -o vv_decrypted.txt --password MySecret123

  # Encrypt/decrypt with a raw 256-bit key (hex, 64 hex chars)
  python3 aes_file_encrypt_decrypt_with_default_password.py encrypt -i vv.txt -o vv.txt.enc --key 0123... (64 hex chars)

Notes:
 - Requires: pip3 install cryptography
 - The encrypted file format: [MAGIC(8)][MODE(1)][SALT?(16 if PBKDF2)][NONCE(12)][CIPHERTEXT+TAG]
 - MODE: 1 = password-derived (PBKDF2), 2 = raw key supplied
"""
import argparse
import os
import sys
import binascii

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# ====== Config / Defaults ======
DEFAULT_PASSWORD = "Varma@8135"   # <--- hard-coded default password per your request
MAGIC = b'AESGCMv1'               # 8 bytes
MODE_PBKDF2 = 1
MODE_RAWKEY = 2
SALT_SIZE = 16
NONCE_SIZE = 12
KEY_SIZE = 32                     # 256-bit AES key
KDF_ITERATIONS = 390_000

# ====== Helpers ======
def derive_key_from_password(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=KDF_ITERATIONS,
    )
    return kdf.derive(password.encode('utf-8'))

def parse_raw_key_hex(hexstr: str) -> bytes:
    try:
        key = binascii.unhexlify(hexstr)
    except Exception:
        raise ValueError('Invalid hex for raw key')
    if len(key) != KEY_SIZE:
        raise ValueError(f'Raw key must be {KEY_SIZE} bytes (64 hex chars)')
    return key

# ====== Encrypt / Decrypt ======
def encrypt_file(in_path: str, out_path: str, password: str = None, raw_key_hex: str = None) -> None:
    if raw_key_hex:
        mode = MODE_RAWKEY
        key = parse_raw_key_hex(raw_key_hex)
        salt = None
    else:
        mode = MODE_PBKDF2
        if password is None:
            password = DEFAULT_PASSWORD
        salt = os.urandom(SALT_SIZE)
        key = derive_key_from_password(password, salt)

    aesgcm = AESGCM(key)
    nonce = os.urandom(NONCE_SIZE)

    with open(in_path, 'rb') as f:
        plaintext = f.read()

    ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data=None)

    with open(out_path, 'wb') as f:
        f.write(MAGIC)
        f.write(bytes([mode]))
        if mode == MODE_PBKDF2:
            f.write(salt)
        f.write(nonce)
        f.write(ciphertext)

    print(f'Encrypted {in_path} -> {out_path} (mode={mode})')

def decrypt_file(in_path: str, out_path: str, password: str = None, raw_key_hex: str = None) -> None:
    with open(in_path, 'rb') as f:
        magic = f.read(len(MAGIC))
        if magic != MAGIC:
            raise ValueError('Bad file format (magic mismatch)')
        mode_byte = f.read(1)
        if not mode_byte:
            raise ValueError('Bad file format (no mode)')
        mode = mode_byte[0]

        if mode == MODE_PBKDF2:
            salt = f.read(SALT_SIZE)
            if len(salt) != SALT_SIZE:
                raise ValueError('Bad file format (salt missing)')
            nonce = f.read(NONCE_SIZE)
            ciphertext = f.read()
            if password is None:
                password = DEFAULT_PASSWORD
            key = derive_key_from_password(password, salt)
        elif mode == MODE_RAWKEY:
            nonce = f.read(NONCE_SIZE)
            ciphertext = f.read()
            if raw_key_hex is None:
                raise ValueError('Raw key hex required to decrypt this file')
            key = parse_raw_key_hex(raw_key_hex)
        else:
            raise ValueError('Unsupported file mode')

    aesgcm = AESGCM(key)
    try:
        plaintext = aesgcm.decrypt(nonce, ciphertext, associated_data=None)
    except Exception as e:
        raise ValueError('Decryption failed (wrong key/password or corrupted file)') from e

    with open(out_path, 'wb') as f:
        f.write(plaintext)

    print(f'Decrypted {in_path} -> {out_path} (mode={mode})')

# ====== CLI ======
def main():
    parser = argparse.ArgumentParser(description='AES-256-GCM file encrypt/decrypt (default password included)')
    sub = parser.add_subparsers(dest='cmd', required=True)

    p_enc = sub.add_parser('encrypt', help='Encrypt a file')
    p_enc.add_argument('-i', '--infile', required=True)
    p_enc.add_argument('-o', '--outfile', required=True)
    p_enc.add_argument('--key', help='Raw 256-bit key in hex (64 hex chars). If provided, overrides password mode.')
    p_enc.add_argument('--password', help='Password to use (overrides built-in default). If omitted, built-in default is used.')

    p_dec = sub.add_parser('decrypt', help='Decrypt a file')
    p_dec.add_argument('-i', '--infile', required=True)
    p_dec.add_argument('-o', '--outfile', required=True)
    p_dec.add_argument('--key', help='Raw 256-bit key in hex (64 hex chars). If file was encrypted with password mode, omit this to use the password (default or --password).')
    p_dec.add_argument('--password', help='Password to use (overrides built-in default). If omitted and file was encrypted with password mode, built-in default is used.')

    args = parser.parse_args()

    if args.cmd == 'encrypt':
        encrypt_file(args.infile, args.outfile, password=args.password, raw_key_hex=args.key)
    elif args.cmd == 'decrypt':
        decrypt_file(args.infile, args.outfile, password=args.password, raw_key_hex=args.key)

if __name__ == '__main__':
    main()