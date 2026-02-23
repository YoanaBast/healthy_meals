# Example .env for Local Setup

Create a `.env` file in the project root (same level as `manage.py`) and copy this content.  
Replace placeholders with your local credentials.

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