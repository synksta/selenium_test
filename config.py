MAIN_URL = "https://аквасуши.рф/"
TIMEOUT = 10
MAX_RETRIES = 5

# AUTH
LOGIN_URL = "https://аквасуши.рф/login"
AUTH_EMAIL_CORRECT = "synksta@ya.ru"
AUTH_PASSWORD_OLD = "sBFDv9A2XkB2"
AUTH_PASSWORD_CORRECT = "1V16NJkWGz5M"

AUTH_EMAIL_INVALID = "invalid@example.com"
AUTH_PASSWORD_INVALID = "wrongpassword"


def update_config(old_password, new_password):
    with open("config.py", "r") as file:
        lines = file.readlines()

    with open("config.py", "w") as file:
        for line in lines:
            if line.startswith("AUTH_PASSWORD_OLD"):
                file.write(f'AUTH_PASSWORD_OLD = "{old_password}"\n')
            elif line.startswith("AUTH_PASSWORD_CORRECT"):
                file.write(f'AUTH_PASSWORD_CORRECT = "{new_password}"\n')
            else:
                file.write(line)
