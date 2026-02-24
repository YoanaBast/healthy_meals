import subprocess
from pathlib import Path
# from django.core.management.utils import get_random_secret_key

# Config
env_path = Path(".env")
env_content = f"""DB_NAME=dbname
DB_USER=dbuser
DB_PASSWORD=dbpassword
DB_HOST=127.0.0.1
DB_PORT=5432
SECRET_KEY =django-insecure-testkey1234567890
"""

affirmatives = {
    "yes", "y", "yea", "yeah", "ye", "yep", "sure", "ok", "okay", "aye", "affirmative", "true", "1"
}

minimal_setup = [
    "pip install -r requirements.txt",
    "python manage.py makemigrations",
    "python manage.py migrate",
    "python manage.py collectstatic --noinput"
]


def yes(prompt: str) -> bool:
    return input(prompt).strip().lower() in {x.lower() for x in affirmatives}


def run_commands(cmd_list):
    for cmd in cmd_list:
        print(f"\n\033[1;32mRunning:\033[0m \033[38;5;214m{cmd}\033[0m")
        subprocess.run(cmd, shell=True, check=True)

# .env setup
if not env_path.exists():
    if yes("No .env file found. Create one now? (y/n): "):
        env_path.write_text(env_content)
        print("\033[1;34m.env created. Please update DB_NAME, DB_USER, DB_PASSWORD before continuing.\033[0m")
        input("You may need to reload from disk to see it. Press Enter when done...")
    else:
        print("\033[1;33mNo .env file. Make sure it exists before running setup. It should look like:\033[0m")
        print(env_content)
        exit()

if yes("\033[1;35mReady for minimal setup? (y/n): \033[0m"):
    run_commands(minimal_setup)
    print("\033[1;33mYou can now use \033[0m\033[1;36mpython manage.py runserver\033[0m\033[1;33m to view the app.\033[0m")


else:
    print("\033[1;32mRun\033[0m \033[1;34mpython fast_setup.py\033[0m \033[1;32magain when ready.\033[0m")
