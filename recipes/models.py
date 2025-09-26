from django.db import models
from django.contrib.auth.models import User


class Recipe(models.Model):
    """
    Recipe model stores all details of a recipe,
    including name, description, ingredients, instructions,
    timings, difficulty, meal type, image, and creator.
    """

    # Choices for the meal_type field
    MEAL_TYPE_CHOICES = [
        ("breakfast", "Breakfast"),
        ("lunch", "Lunch"),
        ("dinner", "Dinner"),
        ("snack", "Snack"),
        ("drink", "Drink"),
        ("dessert", "Dessert"),
    ]

    # --- Core recipe fields ---
    name = models.CharField(max_length=50)
    description = models.TextField(
        blank=True,
        help_text="Short description of the recipe"
    )
    instructions = models.TextField(
        blank=True,
        help_text="Step-by-step cooking instructions"
    )
    ingredients = models.TextField(
        help_text="Comma-separated list of ingredients"
    )

    # --- Timing fields ---
    prep_time = models.PositiveIntegerField(
        help_text="Preparation time in minutes",
        default=5
    )
    cooking_time = models.PositiveIntegerField(
        help_text="Cooking time in minutes"
    )

    # --- Classification fields ---
    difficulty = models.CharField(
        max_length=20,
        blank=True,
        help_text="Automatically calculated when saving"
    )
    meal_type = models.CharField(
        max_length=20,
        choices=MEAL_TYPE_CHOICES,
        default="dinner"
    )

    # --- Media and ownership ---
    pic = models.CharField(
    max_length=100,
    default="no_picture.jpg",
    help_text="Filename of the recipe image in static/recipes/images/"
)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,      # allows NULL for legacy rows
        blank=True,     # allows blank in forms
        related_name="recipes_created"
    )

    def __str__(self):
        """Readable string representation for admin and shell."""
        formatted_ingredients = (
            ", ".join([i.strip() for i in self.ingredients.split(",")])
            if self.ingredients else "None listed"
        )
        return (
            f"{self.name} | "
            f"{self.get_meal_type_display()} | "
            f"Ingredients: {formatted_ingredients} | "
            f"Cook: {self.cooking_time} min | "
            f"Difficulty: {self.difficulty or 'TBD'}"
        )

    # --- Difficulty calculation ---
    def calculate_difficulty(self):
        """
        Automatically determine difficulty based on cooking time
        and number of ingredients.
        """
        num_ingredients = (
            len([i.strip() for i in self.ingredients.split(",") if i.strip()])
            if self.ingredients else 0
        )

        if self.cooking_time == 0:
            # No-cook recipes
            self.difficulty = "easy" if num_ingredients < 4 else "medium"
        elif self.cooking_time < 10:
            self.difficulty = "easy" if num_ingredients < 4 else "medium"
        elif self.cooking_time >= 10:
            self.difficulty = "medium" if num_ingredients < 4 else "hard"

    def save(self, *args, **kwargs):
        """
        Override save() to automatically calculate difficulty
        before saving to the database.
        """
        self.calculate_difficulty()
        super().save(*args, **kwargs)
