from app.core.security import encrypt_token, decrypt_token

def test_token_encryption_decryption():
    token = "ghp_1234567890abcdef"
    encrypted = encrypt_token(token)
    assert encrypted != token
    assert decrypt_token(encrypted) == token

def test_decryption_fallback():
    # Plain token should be returned as-is if decryption fails
    token = "ghp_already_plain"
    assert decrypt_token(token) == token

def test_empty_token():
    assert encrypt_token("") == ""
    assert decrypt_token("") == ""
