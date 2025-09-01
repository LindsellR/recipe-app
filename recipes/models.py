from django.db import models

# Create your models here.

class Recipe(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, help_text="Short description of the recipe")
    instructions = models.TextField(blank=True, help_text="Step-by-step cooking instructions")
    ingredients = models.TextField(help_text="Comma-separated list of ingredients")
    cooking_time = models.PositiveIntegerField(help_text="Cooking time in minutes")
    difficulty = models.CharField(max_length=20, blank=True)

    def __str__(self):
        formatted_ingredients = ", ".join([i.strip() for i in self.ingredients.split(",")]) if self.ingredients else "None listed"
        return f"{self.name} | Ingredients: {formatted_ingredients} | Time: {self.cooking_time} min | Difficulty: {self.difficulty}"

    def calculate_difficulty(self):
        """Automatically determine difficulty based on cooking time and number of ingredients."""
        num_ingredients = len([i.strip() for i in self.ingredients.split(",") if i.strip()]) if self.ingredients else 0

        if self.cooking_time < 10 and num_ingredients < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and num_ingredients >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and num_ingredients < 4:
            self.difficulty = "Intermediate"
        else:
            self.difficulty = "Hard"

    def save(self, *args, **kwargs):
        """Override save to automatically calculate difficulty before saving."""
        self.calculate_difficulty()
        super().save(*args, **kwargs)