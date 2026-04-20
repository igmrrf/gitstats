from cryptography.fernet import Fernet

from .config import settings


def get_fernet() -> Fernet:
    return Fernet(settings.GITHUB_TOKEN_ENCRYPTION_KEY.encode())


def encrypt_token(token: str) -> str:
    if not token:
        return ""
    f = get_fernet()
    return f.encrypt(token.encode()).decode()


def decrypt_token(encrypted_token: str) -> str:
    if not encrypted_token:
        return ""
    f = get_fernet()
    try:
        return f.decrypt(encrypted_token.encode()).decode()
    except Exception:
        # Fallback to plain token if decryption fails (e.g. during migration)
        return encrypted_token
