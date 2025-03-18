import re


def validated_text_for_digit(text: str) -> bool:
    if re.match(r"^[-0-9]+$", text):
        return True
    return False
