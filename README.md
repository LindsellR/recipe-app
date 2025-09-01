# recipe-app
A recipe app where users can create and modify recipes containing ingredients, cooking time, and with a diﬃculty parameter automatically calculated by the application. Users can also search for recipes by ingredient.

## Features

- **Recipe Management**
  - Create recipes with name, description, ingredients, cooking time, instructions, and automatic difficulty calculation.
  - View all recipes in a clean, readable format.
  - Edit and update recipes (planned for future versions).

- **User Interaction**
  - Users can mark recipes as favorites and like recipes.
  - Tracks user interactions with recipes.

- **Search**
  - Search recipes based on selected ingredients.
  - Displays recipes matching selected ingredients.

- **Analytics (Planned)**
  - Generate statistics and visualizations based on user interactions and recipes.

- **Authentication**
  - Uses Django’s built-in User model for login, logout, and user management.

## Project Structure
```

src/
├── recipes/        # Recipe app containing Recipe model
├── favourites/     # Tracks user favourites and likes
├── search/         # Search recipes by ingredients
├── analytics/      # Generates statistics from recipes and interactions
├── manage.py       # Django management script
├── db.sqlite3      # SQLite database
└── ...

## Models

```
**Recipe**
- `name` (CharField, max_length=50)
- `description` (TextField)
- `instructions` (TextField)
- `ingredients` (TextField, comma-separated)
- `cooking_time` (PositiveIntegerField, in minutes)
- `difficulty` (CharField, max_length=20, auto-calculated)

**Favourite**
- `user` (ForeignKey to User)
- `recipe` (ForeignKey to Recipe)
- `added_at` (DateTimeField, auto_now_add=True)
- Prevents duplicate favourites with `unique_together`.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/LindsellR/recipe-app.git
cd recipe-app/src
````

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run migrations:

```bash
python manage.py migrate
```

5. Create a superuser for admin access:

```bash
python manage.py createsuperuser
```

6. Start the development server:

```bash
python manage.py runserver
```

Access the site at `http://127.0.0.1:8000/`.

## Testing

Run the Django test suite:

```bash
python manage.py test
```

Includes tests for:

* Recipe model string representation
* Favourite creation and string representation
* Automatic difficulty calculation

## Usage

* Add recipes via the Django admin or future forms.
* Mark recipes as favorites and like recipes.
* Search recipes by ingredients through the search app (coming soon).

## Notes

* The app currently uses **SQLite** as the database for simplicity.
* Django’s built-in User model is used; no custom user model is required.
* The `.gitignore` is configured to exclude temporary files, database files, and Python environment directories.

