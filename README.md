# Foodganizer

A Django‑based meal planner with detailed nutrient information.  

## Overview

This project lets you:

- Generate a shopping list from your selected recipes.
- Get meal suggestions based on just what you have in your fridge. 
- Track dietary and nutrient information for each meal in all measurement units. 

## Tech Stack

- Python 🐍
- Django 
- HTML, CSS and a sprinkle of JS.
- PostgreSQL 


[AI & Tools Used](/docs/ai_tools.md)


### 📄 Forms & Views

- CRUD for recipes and fridge items
- Custom validations and user‑friendly errors
- Confirmation before deleting objects
- Views handle GET/POST and redirects after successful submissions

### 🧾 Templates

- At least **10 pages** with dynamic data
- Base template + reusable partials
- Navigation & footer on all pages
- Custom 404 error page

## 🛠 Installation

**Requirements:**

- Python 3.11+  
- PostgreSQL  
- Virtual environment tool (recommended)  

**Steps:**

```bash
git clone https://github.com/YoanaBast/healthy_meals.git
cd healthy_meals

python -m venv venv
source venv/bin/activate   # on Linux/Mac
venv\Scripts\activate      # on Windows

pip install -r requirements.txt
