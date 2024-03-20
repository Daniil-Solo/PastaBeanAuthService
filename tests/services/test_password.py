import pytest
from src.services.password import PasswordService
from src.services.exceptions import PasswordValidationException


class TestPasswordValidator:
    def test_too_short_password(self):
        bad_password = "123a"
        with pytest.raises(PasswordValidationException):
            PasswordService.validate_password(bad_password)

    def test_only_letters_password(self):
        bad_password = "abcddsfsgsasdef"
        with pytest.raises(PasswordValidationException):
            PasswordService.validate_password(bad_password)

    def test_only_digits_password(self):
        bad_password = "12342351545"
        with pytest.raises(PasswordValidationException):
            PasswordService.validate_password(bad_password)

    def test_good_password(self):
        bad_password = "a1b2c3d4"
        PasswordService.validate_password(bad_password)


class TestPasswordChecking:
    password = "abcdef"
    different_password = "abcde1"

    def test_different_hashes_for_different_passwords(self):
        hashed_password, _ = PasswordService.create_hashed_password_and_salt(self.password)
        hashed_different_password, _ = PasswordService.create_hashed_password_and_salt(self.different_password)
        assert hashed_password != hashed_different_password

    def test_check_wrong_password(self):
        hashed_password, salt = PasswordService.create_hashed_password_and_salt(self.password)
        assert not PasswordService.verify_password(self.different_password, hashed_password, salt)

    def test_check_right_password(self):
        hashed_password, salt = PasswordService.create_hashed_password_and_salt(self.password)
        assert PasswordService.verify_password(self.password, hashed_password, salt)
