# Cryptographic Application 2.1

A Windows-friendly desktop application for hybrid file encryption and safer RSA key management. The desktop interface uses a premium graphite theme with a compact navigation rail, focused workspace pages and clear key-management controls.

## Features

- RSA-3072 key profiles (RSA-4096 is supported by the engine).
- Passphrase-protected PKCS#8 private keys using scrypt and AES-128-CBC protection provided by PyCryptodome.
- Public/private key separation and SHA-256 public-key fingerprints.
- Import public keys and export public keys or passphrase-protected private-key backups.
- Key profile view with key size, private-key availability and SHA-256 fingerprint.
- Premium dark interface with overview, encryption, decryption and key-management pages.
- Two-step confirmation before deleting a key profile, with an explicit private-key recovery warning.
- Hybrid encryption: AES-256-GCM for file contents and RSA-OAEP with SHA-256 for the AES key.
- Authenticated integrity verification; tampered or truncated files are rejected and partial plaintext is removed.
- Existing output files are not overwritten.
- Activity log records event types and outcomes only, not file paths, passphrases, keys or file contents.

## Requirements

- Windows 10/11
- Python 3.10 or newer

## Setup

Open PowerShell in this project folder and run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

If PowerShell blocks activation, run the app without activating the environment:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

## Tests

```powershell
python -m unittest discover -s tests -v
```

## Key storage

Profiles are stored under `%APPDATA%\CryptographicApplication`. Private keys are encrypted with a passphrase. Export a protected private-key backup and store it separately. If a private key and its backup are lost, files encrypted to that key cannot be recovered.

## Encrypted file format

Files use the `.cap` extension. The format includes a versioned header, wrapped AES key, AES-GCM ciphertext and authentication tag. The header and wrapped key are authenticated as associated data. AES-GCM authenticates the encrypted content before the decrypted file is moved into its final location.

## Important security notes

- This is a local file-encryption tool, not a replacement for a managed enterprise key-management system.
- Protect your Windows account and device. The application does not currently integrate with TPM, Windows Hello, a hardware security module or cloud key vault.
- The app currently encrypts individual files. Recursive folder encryption, drag-and-drop, cancellation and batch processing are not part of this release.
- Keep private-key backups safe and never share them with recipients.
