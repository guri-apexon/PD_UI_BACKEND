from app.utilities.security import get_password_hash, verify_password


def test_verify_hash_password():
    pass_str = "test123"
    hash_value = get_password_hash(pass_str)
    assert verify_password(pass_str, hash_value)
    incorrect_str = "test1234"
    assert verify_password(incorrect_str, hash_value) is False
