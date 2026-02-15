# Project Requirements

## Important Notes
- Authentication and Django User management are **excluded**. Do not implement login, logout, registration, or user-related features.  
- The project must be **downloadable, installable, and runnable** without modifications. After installing dependencies and applying migrations, it should start successfully.  
- Document all environment variables and credentials required for local testing in the README.

---

## Technologies & Framework Requirements
- **Django Framework** (latest stable version)  
  - At least **3 Django apps** with clearly defined responsibilities.  
    - core: homepage, united urls, dummy data automation
    - ingredients: IngredientDietaryTag, IngredientCategory, MeasurementUnit, IngredientMeasurementUnit, Ingredient
    - recipes: RecipeCategory, Recipe, RecipeIngredient
    - planner: UserFridge, Fridge
  - At least **3 database models**:  
    - Models via inheritance or one-to-one relationships count as one.  
    - Include **one many-to-one** and **one many-to-many** relationship.  
      - many-to-one: IngredientMeasurementUnit (.ingredient, .unit), Ingredient (.default_unit, .category), Recipe (.category), Fridge (.user_fridge, .ingredient, .unit)
      - many-to-many: Ingredient (.dietary_tag), Recipe (.ingredients)
- **Forms**  
  - Minimum **3 forms** with proper validations.  
  - Show **user-friendly error messages**.  
  - Customize **labels, placeholders, help texts, and messages**.  
  - Include **read-only or disabled fields** in at least one form.  
  - Exclude unnecessary fields when rendering.  
  - Provide **confirmation before deleting** an object.  
- **Views**  
  - Function-based (FBVs) or class-based (CBVs).  
  - Handle **GET & POST**, validation, saving.  
  - Use **redirects** after successful form submissions.  
- **Templates & Pages**  
  - Minimum **10 pages/templates** using Django Template Engine.  
    - At least **7 pages display dynamic data**.  
    - Implement **CRUD** for at least **2 models**.  
    - Include **all objects, filtered/sorted, single-object pages**.  
    - Use **built-in & custom template filters/tags**.  
    - Custom **404 error page** required.  
    - Base template mandatory (not counted among 10).  
    - Use **template inheritance** and **reusable partials**.  
    - Navigation and footer consistent across pages.  
    - Web page design using **Bootstrap, AI layout, or custom design**.  
- **Navigation**  
  - All pages must be reachable via navigation links.  
  - Avoid orphan pages.  

---

## Database & Tools
- **PostgreSQL** as the database.  
- **GitHub** for version control:  
  - Public repository.  
  - Minimum **3 commits on 3 separate days**.  

---

## Code Quality
- Follow **OOP & clean code best practices**:  
  - Encapsulation, exception handling, inheritance, abstraction, polymorphism.  
  - Strong cohesion, loose coupling.  
  - Consistent, readable naming and formatting.  

---

## Restrictions
- **Do NOT use**:  
  - Ideas, Models, HTML/CSS from workshops, lectures, exercises.  
  - JS modules or SoftUni-related course code.  
  - AI-generated code for core functionality (>60% of project).  
- Focus on **unique, original implementation**.

