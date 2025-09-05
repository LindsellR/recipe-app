from django.db import models

# Create your models here.


class Recipe(models.Model):
    MEAL_TYPE_CHOICES = [
        ("breakfast", "Breakfast"),
        ("lunch", "Lunch"),
        ("dinner", "Dinner"),
        ("snack", "Snack"),
        ("drink", "Drink"),
        ("dessert", "Dessert"),
    ]

    name = models.CharField(max_length=50)
    description = models.TextField(
        blank=True, help_text="Short description of the recipe"
    )
    instructions = models.TextField(
        blank=True, help_text="Step-by-step cooking instructions"
    )
    ingredients = models.TextField(help_text="Comma-separated list of ingredients")
    prep_time = models.PositiveIntegerField(
        help_text="Preparation time in minutes", default=5
    )
    cooking_time = models.PositiveIntegerField(help_text="Cooking time in minutes")
    difficulty = models.CharField(max_length=20, blank=True)
    meal_type = models.CharField(
        max_length=20, choices=MEAL_TYPE_CHOICES, default="dinner"
    )  # 👈 new field
    pic = models.ImageField(upload_to="recipes", default="no_picture.jpg")

    def __str__(self):
        formatted_ingredients = (
            ", ".join([i.strip() for i in self.ingredients.split(",")])
            if self.ingredients
            else "None listed"
        )
        return (
            f"{self.name} | "
            f"Meal: {self.get_meal_type_display()} | "
            f"Ingredients: {formatted_ingredients} | "
            f"Time: {self.cooking_time} min | "
            f"Difficulty: {self.difficulty}"
        )

    def calculate_difficulty(self):
        """Automatically determine difficulty based on cooking time and number of ingredients."""
        num_ingredients = (
            len([i.strip() for i in self.ingredients.split(",") if i.strip()])
            if self.ingredients
            else 0
        )

        if self.cooking_time == 0:
            # No-cook recipes
            self.difficulty = "Easy" if num_ingredients < 4 else "Medium"
        elif self.cooking_time < 10:
            self.difficulty = "Easy" if num_ingredients < 4 else "Medium"
        elif self.cooking_time >= 10:
            self.difficulty = "Intermediate" if num_ingredients < 4 else "Hard"

    def save(self, *args, **kwargs):
        """Override save to automatically calculate difficulty before saving."""
        self.calculate_difficulty()
        super().save(*args, **kwargs)
