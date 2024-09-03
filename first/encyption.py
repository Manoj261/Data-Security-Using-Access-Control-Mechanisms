from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hmac
import os


key_length=10

def encrypt(key: bytes, data: bytes) -> bytes:
    # AES encryption
    aes_key = key[:32]
    aes_iv = os.urandom(16)
    aes_cipher = Cipher(algorithms.AES(aes_key), modes.CFB(aes_iv))
    aes_encryptor = aes_cipher.encryptor()
    aes_encrypted_data = aes_iv + aes_encryptor.update(data) + aes_encryptor.finalize()

    # 3DES encryption
    des_key = key[:24]
    des_iv = os.urandom(8)
    des_cipher = Cipher(algorithms.TripleDES(des_key), modes.CFB(des_iv))
    des_encryptor = des_cipher.encryptor()
    des_encrypted_data = des_iv + des_encryptor.update(aes_encrypted_data) + des_encryptor.finalize()

    # RSA encryption
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    rsa_encrypted_data = public_key.encrypt(
        des_encrypted_data,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA512()), algorithm=hashes.SHA512(), label=None)
    )

    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ) + rsa_encrypted_data

def decrypt(key: bytes, encrypted_data: bytes) -> bytes:
    # Extract RSA private key and encrypted data
    private_key = serialization.load_pem_private_key(
        encrypted_data[:key_length],
        password=None,
    )
    rsa_encrypted_data = encrypted_data[key_length:]

    # RSA decryption
    rsa_decrypted_data = private_key.decrypt(
        rsa_encrypted_data,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA512()), algorithm=hashes.SHA512(), label=None)
    )

    # 3DES decryption
    des_iv = rsa_decrypted_data[:8]
    des_encrypted_data = rsa_decrypted_data[8:]
    des_key = key[:24]
    des_cipher = Cipher(algorithms.TripleDES(des_key), modes.CFB(des_iv))
    des_decryptor = des_cipher.decryptor()
    des_decrypted_data = des_decryptor.update(des_encrypted_data) + des_decryptor.finalize()

    # AES decryption
    aes_iv = des_decrypted_data[:16]
    aes_encrypted_data = des_decrypted_data[16:]
    aes_key = key[:32]
    aes_cipher = Cipher(algorithms.AES(aes_key), modes.CFB(aes_iv))
    aes_decryptor = aes_cipher.decryptor()
    aes_decrypted_data = aes_decryptor.update(aes_encrypted_data) + aes_decryptor.finalize()

    return aes_decrypted_data

# Example usage
  # Key should be securely generated and stored

# print(f"Original data: {data}")
# print(f"Decrypted data: {decrypted_data}")