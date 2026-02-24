# Example .env for Local Setup

Replace placeholders with your local credentials: your_db_name, your_db_user, your_db_password (SECRET_KEY will be already available)

```text
# Database configuration
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=127.0.0.1
DB_PORT=5432

# Django secret key
# Can be any random string for local testing
SECRET_KEY=django-insecure-default-for-local
