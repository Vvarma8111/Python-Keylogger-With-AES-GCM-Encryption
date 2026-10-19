"""AES-GCM encryption for text files.

Requires: pip install cryptography

Import ``encrypt_file`` and ``decrypt_file`` from this module, or run it as a
command-line program.  The password is intentionally fixed as requested.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import os
from pathlib import Path

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


PASSWORD = "Varma@8135"
_MAGIC = b"PYAESGCM1"
_SALT_SIZE = 16
_NONCE_SIZE = 12
_KEY_SIZE = 32


def _key(password: str, salt: bytes) -> bytes:
	return hashlib.pbkdf2_hmac(
		"sha256", password.encode("utf-8"), salt, 600_000, _KEY_SIZE
	)


def encrypt_file(input_file: str | os.PathLike, output_file: str | os.PathLike | None = None,
				 password: str = PASSWORD) -> Path:
	"""Encrypt a UTF-8 text file and return the encrypted file path."""
	source = Path(input_file)
	destination = Path(output_file) if output_file else source.with_suffix(source.suffix + ".enc")
	salt = os.urandom(_SALT_SIZE)
	nonce = os.urandom(_NONCE_SIZE)
	plaintext = source.read_bytes()
	ciphertext = AESGCM(_key(password, salt)).encrypt(nonce, plaintext, _MAGIC)
	destination.write_bytes(_MAGIC + salt + nonce + ciphertext)
	return destination


def decrypt_file(input_file: str | os.PathLike, output_file: str | os.PathLike | None = None,
				 password: str = PASSWORD) -> bool:
	"""Decrypt a file.  On a wrong password, writes unreadable gibberish and returns False."""
	source = Path(input_file)
	destination = Path(output_file) if output_file else source.with_suffix(".txt")
	blob = source.read_bytes()
	try:
		if not blob.startswith(_MAGIC):
			raise InvalidTag
		start = len(_MAGIC)
		salt = blob[start:start + _SALT_SIZE]
		nonce_start = start + _SALT_SIZE
		nonce = blob[nonce_start:nonce_start + _NONCE_SIZE]
		ciphertext = blob[nonce_start + _NONCE_SIZE:]
		plaintext = AESGCM(_key(password, salt)).decrypt(nonce, ciphertext, _MAGIC)
		destination.write_bytes(plaintext)
		return True
	except (InvalidTag, ValueError):
		# GCM deliberately reveals no plaintext when authentication fails.
		gibberish = base64.b64encode(hashlib.sha256(blob).digest() + blob)
		destination.write_bytes(gibberish)
		return False


def main() -> None:
	parser = argparse.ArgumentParser(description="AES-GCM text-file encryption")
	sub = parser.add_subparsers(dest="action", required=True)
	enc = sub.add_parser("encrypt")
	enc.add_argument("input")
	enc.add_argument("output", nargs="?")
	dec = sub.add_parser("decrypt")
	dec.add_argument("input")
	dec.add_argument("output", nargs="?")
	args = parser.parse_args()
	password = input("Password: ")
	if args.action == "encrypt":
		encrypt_file(args.input, args.output, password)
	elif not decrypt_file(args.input, args.output, password):
		print("Incorrect password or corrupted file; gibberish was written.")


if __name__ == "__main__":
	main()




