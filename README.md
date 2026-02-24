# Foodganizer
Python | Django | HTML | CSS | JS | PostgreSQL 

- Generate a shopping list from your selected recipes.
- Get meal suggestions based on just what you have in your fridge. 
- Track dietary and nutrient information for each meal in all measurement units. 

## 🛠 Installation

**Requirements:**
- Python 3.11+  
- PostgreSQL  


### 1. Clone the repo

```bash
git clone https://github.com/YoanaBast/healthy_meals.git
cd healthy_meals
```
### 2. Virtual Environment
**Check if a venv already exists:**
- If you created a project in your IDE **before cloning**, it may have already created a virtual environment.
- Look in the project folder for a `venv/` (or similarly named) directory.  
- You can also check the IDE’s Python interpreter settings to see if a venv is active.

**If no venv exists, create one:**
```bash
python -m venv venv
source venv/bin/activate   # on Linux/Mac
venv\Scripts\activate      # on Windows
```

### 2. Setup

#### 2.1 Fast Setup
- You can run the command below to complete the setup:
```bash
python fast_setup.py
```
- This will do the following:
  - create .env if you don't have one 
  - generate and assign a django secret key
  - install requirements
  - makemigrations and migrate
  - collectstatic
- It will also offer you to populate dummy data (it will ask you first)

#### 2.2 Manual Setup
- If you don't want to use the fast setup, you can follow the steps below
    - create a .env file in the root directory (healthy_meals)
    - put [this](docs/creds_example.md) inside and update it with your credentials
    - run this to install requirements:
```bash
    pip install -r requirements.txt
```
- run this to set up your DB:
```bash
    python manage.py makemigrations
    python manage.py migrate
```
- run this to set up the css:
```bash
    python manage.py collectstatic --noinput
```
- You can now run the server to see the empty app:
```bash
    python manage.py runserver
```

#### 2.3 Dummy Data
- You can populate the DB with some dummy data by running this:
```bash
    "python manage.py populate_dummy_data"
```

## Notes:
1. This is developed as uni assignment. To be compliant to the no auth requirement, I have assigned a default user for all logic that needs it. I intend to scale the app and a huge part of my logic will depend on dynamic users. 
   - default user in question: user = User.objects.get(username="default") 
   - No auth requirement: "Authentication and Django User management are explicitly excluded from the following requirements. You are not supposed to implement login, logout, registration, or user-related functionality."



## See Also:
- [AI & Tools Used](docs/ai_tools.md)
- [TO-DO List](docs/to_do.md) 
