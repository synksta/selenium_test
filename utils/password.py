import string
import random


def generate_random_password(self, length=12):
    """Генерация случайного пароля."""
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for i in range(length))
