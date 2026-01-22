import subprocess
from pathlib import Path
from django.core.management.utils import get_random_secret_key

# Config
env_path = Path(".env")
env_content = f"""DB_NAME=dbname
DB_USER=dbuser
DB_PASSWORD=dbpassword
DB_HOST=127.0.0.1
DB_PORT=5432
SECRET_KEY={get_random_secret_key()}
"""

affirmatives = {
    "yes", "y", "yea", "yeah", "ye", "yep", "sure", "ok", "okay", "aye", "affirmative", "true", "1"
}

minimal_setup = [
    "pip install -r requirements.txt",
    "python manage.py makemigrations",
    "python manage.py migrate",
]

run_server_cmd = "python manage.py runserver"

populate_dummy_data = [
    "python manage.py populate_ingredients",
    "python manage.py populate_recipes"
]

tests = [
    "python manage.py test ingredients",
]


def yes(prompt: str) -> bool:
    return input(prompt).strip().lower() in {x.lower() for x in affirmatives}


def run_commands(cmd_list):
    for cmd in cmd_list:
        print(f"\n\033[1;32mRunning:\033[0m \033[38;5;214m{cmd}\033[0m")
        if "runserver" in cmd:

            # start server in background
            subprocess.Popen(cmd, shell=True)
            print("\033[1;34mDjango server started in background.\033[0m")
        else:
            subprocess.run(cmd, shell=True, check=True)

if not env_path.exists() and yes("Create .env file? (y/n): "):
    env_path.write_text(env_content)
    print("\033[1;34m.env created in root. Update DB_NAME, DB_USER, DB_PASSWORD.\033[0m")

elif not env_path.exists():
    print("\033[1;33mMake sure .env exists before continuing. It should look like:\033[0m")
    print(env_content)


if yes("\033[1;35mReady for minimal setup? (y/n): \033[0m"):
    run_commands(minimal_setup)

    if yes("\033[1;35mAdd dummy data? (y/n): \033[0m"):
        run_commands(populate_dummy_data)

    # start server last
    print("\033[1;34mStarting Django server...\033[0m")
    subprocess.Popen(run_server_cmd, shell=True)
    print("\033[1;34mDjango server started in background.\033[0m")

else:
    print("\033[1;32mRun\033[0m \033[1;34mpython lazy_setup.py\033[0m \033[1;32magain when ready.\033[0m")
