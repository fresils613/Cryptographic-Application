"""Hybrid file encryption: RSA-OAEP (SHA-256) + AES-256-GCM."""
from __future__ import annotations

import json
import os
import struct
from pathlib import Path

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

MAGIC = b"CAP21\x00"
VERSION = 1
_HEADER = struct.Struct(">6sB H 16s 12s Q")
CHUNK_SIZE = 1024 * 1024


class CryptoFileError(Exception):
    """Raised when an encrypted file is invalid or cannot be processed."""


def generate_key_pair(bits: int = 3072):
    if bits not in (3072, 4096):
        raise ValueError("RSA key size must be 3072 or 4096 bits.")
    return RSA.generate(bits)


def fingerprint(public_key: RSA.RsaKey) -> str:
    digest = SHA256.new(public_key.public_key().export_key(format="DER")).hexdigest().upper()
    return ":".join(digest[i:i + 4] for i in range(0, len(digest), 4))


def encrypt_file(source: Path, destination: Path, recipient_public_key: RSA.RsaKey) -> None:
    source, destination = Path(source), Path(destination)
    if not source.is_file():
        raise FileNotFoundError(source)
    if destination.exists():
        raise FileExistsError(f"Output already exists: {destination}")
    aes_key = get_random_bytes(32)
    nonce = get_random_bytes(12)
    wrapped_key = PKCS1_OAEP.new(recipient_public_key.public_key(), hashAlgo=SHA256).encrypt(aes_key)
    if len(wrapped_key) > 65535:
        raise ValueError("Recipient key is not supported.")
    plaintext_size = source.stat().st_size
    header = _HEADER.pack(MAGIC, VERSION, len(wrapped_key), get_random_bytes(16), nonce, plaintext_size)
    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce, mac_len=16)
    cipher.update(header + wrapped_key)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temp = destination.with_name(destination.name + ".partial")
    try:
        with source.open("rb") as src, temp.open("xb") as out:
            out.write(header)
            out.write(wrapped_key)
            while True:
                chunk = src.read(CHUNK_SIZE)
                if not chunk:
                    break
                out.write(cipher.encrypt(chunk))
            out.write(cipher.digest())
        os.replace(temp, destination)
    except Exception:
        temp.unlink(missing_ok=True)
        raise
    finally:
        aes_key = b"\x00" * len(aes_key)


def decrypt_file(source: Path, destination: Path, recipient_private_key: RSA.RsaKey) -> None:
    source, destination = Path(source), Path(destination)
    if not source.is_file():
        raise FileNotFoundError(source)
    if destination.exists():
        raise FileExistsError(f"Output already exists: {destination}")
    temp = destination.with_name(destination.name + ".partial")
    try:
        with source.open("rb") as src:
            raw_header = src.read(_HEADER.size)
            if len(raw_header) != _HEADER.size:
                raise CryptoFileError("The encrypted file is incomplete.")
            magic, version, wrapped_len, _file_id, nonce, expected_size = _HEADER.unpack(raw_header)
            if magic != MAGIC or version != VERSION or wrapped_len < 1:
                raise CryptoFileError("This file is not a supported Cryptographic Application file.")
            wrapped_key = src.read(wrapped_len)
            if len(wrapped_key) != wrapped_len:
                raise CryptoFileError("The encrypted file header is incomplete.")
            try:
                aes_key = PKCS1_OAEP.new(recipient_private_key, hashAlgo=SHA256).decrypt(wrapped_key)
            except ValueError as exc:
                raise CryptoFileError("This private key cannot decrypt the file.") from exc
            cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce, mac_len=16)
            cipher.update(raw_header + wrapped_key)
            # The final 16 bytes are the GCM authentication tag.
            remaining = source.stat().st_size - _HEADER.size - wrapped_len
            if remaining < 16:
                raise CryptoFileError("The encrypted file is truncated.")
            ciphertext_remaining = remaining - 16
            with temp.open("xb") as out:
                while ciphertext_remaining:
                    block = src.read(min(CHUNK_SIZE, ciphertext_remaining))
                    if not block:
                        raise CryptoFileError("The encrypted file is truncated.")
                    ciphertext_remaining -= len(block)
                    out.write(cipher.decrypt(block))
                tag = src.read(16)
                if len(tag) != 16 or src.read(1):
                    raise CryptoFileError("The encrypted file has an invalid ending.")
                try:
                    cipher.verify(tag)
                except ValueError as exc:
                    raise CryptoFileError("Integrity check failed. The file may have been modified or the key is incorrect.") from exc
            if temp.stat().st_size != expected_size:
                raise CryptoFileError("The decrypted file size does not match the original file.")
        os.replace(temp, destination)
    except Exception:
        temp.unlink(missing_ok=True)
        raise
