import tempfile
import unittest
from pathlib import Path

from Crypto.PublicKey import RSA
from cryptographic_app.crypto_engine import CryptoFileError, decrypt_file, encrypt_file


class CryptoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.key = RSA.generate(3072)

    def test_round_trip(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); source = root / "sample.txt"; encrypted = root / "sample.txt.cap"; output = root / "restored.txt"
            source.write_bytes(b"PacketScope is not this project.\x00" * 1000)
            encrypt_file(source, encrypted, self.key.public_key())
            decrypt_file(encrypted, output, self.key)
            self.assertEqual(source.read_bytes(), output.read_bytes())

    def test_tamper_detected_and_no_output_left(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); source = root / "sample.txt"; encrypted = root / "sample.txt.cap"; output = root / "restored.txt"
            source.write_bytes(b"important data")
            encrypt_file(source, encrypted, self.key.public_key())
            data = bytearray(encrypted.read_bytes()); data[-20] ^= 1; encrypted.write_bytes(data)
            with self.assertRaises(CryptoFileError): decrypt_file(encrypted, output, self.key)
            self.assertFalse(output.exists())

    def test_wrong_key_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); source = root / "sample.txt"; encrypted = root / "sample.txt.cap"; output = root / "restored.txt"
            source.write_bytes(b"data")
            encrypt_file(source, encrypted, self.key.public_key())
            other = RSA.generate(3072)
            with self.assertRaises(CryptoFileError): decrypt_file(encrypted, output, other)


if __name__ == "__main__": unittest.main()
