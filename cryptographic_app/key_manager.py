"""Local key-profile storage and management."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

from Crypto.PublicKey import RSA

from .crypto_engine import fingerprint, generate_key_pair


def app_data_dir() -> Path:
    import os
    base = Path(os.environ.get("APPDATA", Path.home() / ".config"))
    path = base / "CryptographicApplication"
    path.mkdir(parents=True, exist_ok=True)
    return path


class KeyManager:
    def __init__(self, root: Path | None = None):
        self.root = Path(root) if root else app_data_dir()
        self.root.mkdir(parents=True, exist_ok=True)

    def profiles(self):
        found = []
        for folder in sorted(self.root.iterdir()):
            meta = folder / "profile.json"
            if folder.is_dir() and meta.is_file():
                try:
                    found.append(json.loads(meta.read_text(encoding="utf-8")))
                except (OSError, json.JSONDecodeError):
                    continue
        return found

    def create_profile(self, name: str, passphrase: str, bits: int = 3072):
        clean = name.strip()
        if not clean or len(clean) > 40 or not re.fullmatch(r"[\w .-]+", clean):
            raise ValueError("Use 1–40 letters, numbers, spaces, dots or hyphens for the profile name.")
        if len(passphrase) < 12:
            raise ValueError("Use a passphrase with at least 12 characters.")
        folder = self.root / re.sub(r"[^\w.-]+", "_", clean).strip("._")
        if folder.exists():
            raise FileExistsError("A profile with that name already exists.")
        folder.mkdir(parents=True)
        try:
            key = generate_key_pair(bits)
            private_path = folder / "private_key.pem"
            public_path = folder / "public_key.pem"
            private_path.write_bytes(key.export_key(format="PEM", passphrase=passphrase, pkcs=8, protection="scryptAndAES128-CBC"))
            public_path.write_bytes(key.public_key().export_key(format="PEM"))
            try:
                private_path.chmod(0o600)
            except OSError:
                pass
            record = {
                "name": clean,
                "created_utc": datetime.now(timezone.utc).isoformat(),
                "key_size": key.size_in_bits(),
                "fingerprint": fingerprint(key.public_key()),
                "private_key": private_path.name,
                "public_key": public_path.name,
            }
            (folder / "profile.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
            return record
        except Exception:
            import shutil
            shutil.rmtree(folder, ignore_errors=True)
            raise

    def _folder(self, name: str) -> Path:
        for profile in self.profiles():
            if profile.get("name") == name:
                return self.root / re.sub(r"[^\w.-]+", "_", name).strip("._")
        raise FileNotFoundError("Key profile not found.")

    def load_public(self, name: str):
        folder = self._folder(name)
        return RSA.import_key((folder / "public_key.pem").read_bytes())

    def load_private(self, name: str, passphrase: str):
        folder = self._folder(name)
        try:
            return RSA.import_key((folder / "private_key.pem").read_bytes(), passphrase=passphrase)
        except (ValueError, IndexError) as exc:
            raise ValueError("The passphrase is incorrect or the private key is damaged.") from exc

    def export_public(self, name: str, destination: Path):
        destination = Path(destination)
        if destination.exists():
            raise FileExistsError(destination)
        destination.write_bytes(self.load_public(name).export_key(format="PEM"))

    def export_private(self, name: str, passphrase: str, destination: Path):
        destination = Path(destination)
        if destination.exists():
            raise FileExistsError(destination)
        folder = self._folder(name)
        key = self.load_private(name, passphrase)
        destination.write_bytes(key.export_key(format="PEM", passphrase=passphrase, pkcs=8, protection="scryptAndAES128-CBC"))
        try:
            destination.chmod(0o600)
        except OSError:
            pass

    def import_public(self, name: str, source: Path):
        clean = name.strip()
        if not clean or not re.fullmatch(r"[\w .-]{1,40}", clean):
            raise ValueError("Enter a valid profile name.")
        key = RSA.import_key(Path(source).read_bytes())
        if key.has_private():
            key = key.public_key()
        if key.size_in_bits() < 3072:
            raise ValueError("RSA public keys must be at least 3072 bits.")
        folder = self.root / re.sub(r"[^\w.-]+", "_", clean).strip("._")
        if folder.exists():
            raise FileExistsError("A profile with that name already exists.")
        folder.mkdir(parents=True)
        public_path = folder / "public_key.pem"
        public_path.write_bytes(key.export_key(format="PEM"))
        record = {"name": clean, "created_utc": datetime.now(timezone.utc).isoformat(), "key_size": key.size_in_bits(), "fingerprint": fingerprint(key), "private_key": None, "public_key": public_path.name}
        (folder / "profile.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
        return record

    def delete_profile(self, name: str):
        import shutil
        folder = self._folder(name)
        shutil.rmtree(folder)
