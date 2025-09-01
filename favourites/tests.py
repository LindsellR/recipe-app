from django.test import TestCase
from django.contrib.auth.models import User
from .models import Recipe, Favourite

#create your test here

class RecipeModelTest(TestCase):

    def setUp(self):
        self.recipe = Recipe.objects.create(
            name="Pasta",
            ingredients="pasta, tomato, garlic",
            cooking_time=20,
            difficulty="Intermediate",
            description="A simple pasta dish",
            instructions="Boil pasta, add sauce."
        )
        self.user = User.objects.create_user(username="tester", password="pass123")

    def test_recipe_str(self):
        self.assertEqual(
            str(self.recipe),
            "Pasta | Ingredients: pasta, tomato, garlic | Time: 20 min | Difficulty: Intermediate"
        )

    def test_favourite_creation(self):
        fav = Favourite.objects.create(user=self.user, recipe=self.recipe)
        self.assertEqual(str(fav), "tester → Pasta")
        self.assertEqual(fav.user.username, "tester")
        self.assertEqual(fav.recipe.name, "Pasta")

