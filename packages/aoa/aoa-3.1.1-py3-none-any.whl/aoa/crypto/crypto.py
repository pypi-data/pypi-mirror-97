import base64, secrets

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

backend = default_backend()


default_conf = {
    "iterations": 65536,
    "bytes_key_length": 32,
    "bytes_salt_length": 16,
    "bytes_iv_length": 16,
    "bytes_auth_tag_length": 16
}


def _derive_key(password, salt, iterations, length):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=length, salt=salt,
        iterations=iterations, backend=backend)
    return kdf.derive(password)


def aes_gcm_encrypt(message: str, password: str, conf: dict = default_conf) -> str:
    """

    :param message: the text to encrypt
    :param password: the token/key to use for decryption (no spaces allowed)
    :param conf: if not specified will use the default conf of
            default_conf = {
                "iterations": 65536,
                "bytes_key_length": 32,
                "bytes_salt_length": 16,
                "bytes_iv_length": 16,
                "bytes_auth_tag_length": 16
            }
    :return: the encrypted message
    """
    auth_tag = secrets.token_bytes(conf["bytes_auth_tag_length"])
    iv = secrets.token_bytes(conf["bytes_iv_length"])
    salt = secrets.token_bytes(conf["bytes_salt_length"])
    key = _derive_key(password.encode(), salt, conf["iterations"], conf["bytes_key_length"])
    algorithm = algorithms.AES(key)
    cipher = Cipher(algorithm, modes.GCM(iv), backend=backend)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message.encode())

    return base64.urlsafe_b64encode(iv + salt + ciphertext + auth_tag).decode('utf-8')


def aes_gcm_decrypt(message: str, password: str, conf: dict = default_conf) -> str:
    """
    Decrypt text which was previously encrypted by the AOA core for e.g connection credentials. It is AES 256 bit HMAC

    :param message: the text to decrypt
    :param password: the token/key to use for decryption
    :param conf: if not specified will use the default conf of
            default_conf = {
                "iterations": 65536,
                "bytes_key_length": 32,
                "bytes_salt_length": 16,
                "bytes_iv_length": 16,
                "bytes_auth_tag_length": 16
            }
    :return: decrypted text
    """
    data = base64.urlsafe_b64decode(message.encode())
    (iv, salt, ciphertext, auth_tag) = data[:conf["bytes_iv_length"]], \
                                       data[conf["bytes_iv_length"] : conf["bytes_iv_length"] + conf["bytes_salt_length"]], \
                                       data[conf["bytes_iv_length"] + conf["bytes_salt_length"] : -conf["bytes_auth_tag_length"]], \
                                       data[-conf["bytes_auth_tag_length"]:]
    key = _derive_key(password.encode(), salt, iterations=conf["iterations"], length=conf["bytes_key_length"])
    algorithm = algorithms.AES(key)
    cipher = Cipher(algorithm, modes.GCM(iv, salt), backend=backend)
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(ciphertext)

    return decrypted.decode('utf-8')
