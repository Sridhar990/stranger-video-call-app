import re


def validate_password(password: str) -> str:

    if not re.search(r"[A-Z]", password):
        raise ValueError(
            "Password must contain at least one uppercase letter."
        )

    if not re.search(r"[a-z]", password):
        raise ValueError(
            "Password must contain at least one lowercase letter."
        )

    if not re.search(r"\d", password):
        raise ValueError(
            "Password must contain at least one number."
        )

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValueError(
            "Password must contain at least one special character."
        )

    if re.search(r"\s", password):
        raise ValueError(
            "Password cannot contain spaces."
        )

    return password