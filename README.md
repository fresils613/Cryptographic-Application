# Cryptographic Application

A Python-based file encryption and decryption project built around RSA key generation and file/folder workflows. This repository contains the original command-line version of the project.

> **Project status:** Educational project. Review the implementation and test it in a safe environment before using it with important or sensitive files. Do not treat this version as a production-ready file-protection product.

## Features documented in this version

- Generate RSA public and private keys.
- Encrypt and decrypt supported files.
- Encrypt and decrypt folders containing supported files.
- Organise key files separately for different users.

## Requirements

- Python 3
- `pycryptodome`
- `termcolor`

## Installation

Clone or download this repository, open a terminal in the project directory, and install the dependencies:

```powershell
python -m pip install pycryptodome termcolor
```

## Run the application

The original command-line entry point is in the `rsa` directory:

```powershell
cd rsa
python main.py
```

Follow the prompts to generate keys and perform encryption or decryption.

## File and folder limitations

The original README documents support for:

- TXT files
- PDF files
- Word documents

For folder operations, the folder must contain supported files only. Nested folders are not supported by the original implementation. Password-protected documents are also documented as unsupported.

Check the code and test with copies of files before relying on these limitations or workflows.

## Key handling

- Keep private keys separate from public keys.
- Restrict access to private-key files.
- Keep secure backups of private keys.
- Never commit private keys, passwords, or real sensitive data to this repository.

## Security note

This repository represents an earlier implementation of the project. Before using it to protect real data, independently review its key storage, encryption mode, authentication/integrity protection, error handling, and file-handling behaviour. A successful encryption operation alone does not establish that a cryptographic application is secure.

## Development

Contributions and technical feedback are welcome. Please include reproducible steps when reporting issues.