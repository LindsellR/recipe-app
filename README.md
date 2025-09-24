# Recipe App
A recipe app built on Django where users can create, edit, and manage recipes with ingredients, instructions, cooking time, and automatic difficulty calculation. Users can also search for recipes, save their favourites, manage their profile, and reset their password.

## Features

- **Recipe Management**
  - Create recipes with name, ingredients, instructions, cooking time, and automatic difficulty calculation.
  - View all recipes in a clean, readable format.
  - Edit and update recipes.
  - Delete recipes.

- **User Interaction**
  - Users can mark recipes as favourites.
  - Users can manage their profile, including updating email, username, and password.
  - Password reset functionality is available via email (development: printed to terminal).

- **Search**
  - Search recipes by ingredients or meal type(breakfast, lunch, dinner, drink, snacks)
  - Displays recipes matching selected ingredients or meal type

  **Advanced Search**
  - Search by recipe name, ingredients, difficulty, meal type, or max cooking time.

- **About Me Page**
  - Includes a headshot, biography, and a link to a personal portfolio site.

- **Responsive Design**
  - Header, forms, recipe listings, and pages are responsive for mobile and desktop.

- **Authentication**
  - Uses Django’s built-in User model for sign-up, login, logout, and password management.

## Project Structure
```

Recipe_App/
├── recipe\_app/      # Project app
├── recipes/         # Recipe app containing Recipe model, views, static files, charts
├── users/           # Handles user profiles, authentication, and favourites
├── media/           # Stores uploaded media (profile pictures, recipe images, etc.)
├── templates/       # Global templates (base.html, auth/, registration/)
├── manage.py        # Django management script
├── db.sqlite3       # SQLite database
└── ...

````

## Models

**Recipe**
- `name` (CharField, max_length=50)
- `ingredients` (TextField, comma-separated)
- `instructions` (TextField)
- `cooking_time` (PositiveIntegerField, in minutes)
- `difficulty` (CharField, max_length=20, auto-calculated)
- `meal_type` (ChoiceField: Breakfast, Lunch, Dinner, Snack, Drink, Dessert)

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

* Recipe creation, editing, and deletion
* Favourite creation and removal
* Profile updates (email, username, password)
* Password reset
* Form validations

## Usage

* Sign up, login, and manage your user profile.
* Add, edit, and delete recipes.
* Mark recipes as favourites.
* Search recipes by ingredients.
* Visit the About Me page to see biography and portfolio link.

## Notes

* The app currently uses **SQLite** for simplicity in development.
* Media uploads (images) are stored in the `media/` folder.
* Static files for the recipes app are stored in `recipes/static/`.
* The app uses Django’s built-in User model; no custom user model is required.
* Email password reset in development prints the reset link to the terminal.
* The `.gitignore` is configured to exclude temporary files, database files, and Python environment directories.

```

