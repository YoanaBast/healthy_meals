### AI used:

- v0:
  - Prototyped the UI in the very beginning. I've changed a lot, this is the original it provided: 
  
- ChatGPT:
  - Provided a JSON file and prompted to mirror the data and add more to it.
  - Made it generate some basic CSS and templates, then I modified them to my liking. 
  - Got assistance with the JS
  
- ClickUp Brain:
- Generated images:

<img src="./documented_files/tomato.png" alt="Tomato" width="200" />

### Other tools used:

Relationships include:

- **Many‑to‑one**: Ingredient → Category, IngredientMeasurementUnit → Ingredient/Unit, Recipe → Category, Fridge → Ingredient/Unit/UserFridge  
- **Many‑to‑many**: Ingredient ↔ DietaryTag, Recipe ↔ Ingredient (through `RecipeIngredient`)