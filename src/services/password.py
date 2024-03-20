import re
import os
import hashlib
from src.constants import PASSWORD_MIN_LENGTH
from src.services.exceptions import PasswordValidationException


class PasswordService:
    @staticmethod
    def validate_password(password: str) -> None:
        if len(password) < PASSWORD_MIN_LENGTH:
            raise PasswordValidationException(
                f"Пароль слишком короткий, требуется минимум {PASSWORD_MIN_LENGTH} символов")
        elif re.search('[0-9]', password) is None:
            raise PasswordValidationException("Пароль должен содержать хотя бы одну цифру")
        elif re.search('[a-zA-Z]', password) is None:
            raise PasswordValidationException("Пароль должен содержать хотя бы одну латинскую букву")

    @staticmethod
    def create_hashed_password_and_salt(password: str) -> tuple[str, str]:
        salt = os.urandom(32)
        encoded_password = password.encode("UTF-8")
        key = hashlib.pbkdf2_hmac('sha256', encoded_password, salt, 100000)
        return key.hex(), salt.hex()

    @staticmethod
    def verify_password(try_password: str, hashed_password: str, salt: str) -> bool:
        encoded_try_password = try_password.encode("UTF-8")
        try_key = hashlib.pbkdf2_hmac('sha256', encoded_try_password, bytes.fromhex(salt), 100000)
        real_key = bytes.fromhex(hashed_password)
        return try_key == real_key
