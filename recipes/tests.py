from django.test import TestCase
from .models import Recipe

#Create your tests here

class RecipeModelTest(TestCase):

    def setUp(self):
        self.recipe = Recipe.objects.create(
            name="Pasta",
            description="A simple pasta dish",
            instructions="Boil pasta, add sauce.",
            ingredients="pasta, tomato, garlic",
            cooking_time=20
        )

    def test_str_method(self):
        self.assertEqual(
            str(self.recipe),
            "Pasta | Ingredients: pasta, tomato, garlic | Time: 20 min | Difficulty: Intermediate"
        )

    def test_name_max_length(self):
        max_length = self.recipe._meta.get_field('name').max_length
        self.assertEqual(max_length, 50)

    def test_difficulty_max_length(self):
        max_length = self.recipe._meta.get_field('difficulty').max_length
        self.assertEqual(max_length, 20)

    def test_calculate_difficulty_easy(self):
        recipe = Recipe.objects.create(
            name="Salad",
            ingredients="lettuce, tomato",
            cooking_time=5
        )
        self.assertEqual(recipe.difficulty, "Easy")

    def test_calculate_difficulty_medium(self):
        recipe = Recipe.objects.create(
            name="Smoothie",
            ingredients="banana, milk, yogurt, honey",
            cooking_time=5
        )
        self.assertEqual(recipe.difficulty, "Medium")

    def test_calculate_difficulty_intermediate(self):
        recipe = Recipe.objects.create(
            name="Soup",
            ingredients="water, carrot",
            cooking_time=15
        )
        self.assertEqual(recipe.difficulty, "Intermediate")

    def test_calculate_difficulty_hard(self):
        recipe = Recipe.objects.create(
            name="Feast",
            ingredients="chicken, rice, carrots, peas",
            cooking_time=20
        )
        self.assertEqual(recipe.difficulty, "Hard")

    def test_empty_ingredients_handled(self):
        recipe = Recipe.objects.create(
            name="Mystery Dish",
            ingredients="",
            cooking_time=5
        )
        self.assertIn("None listed", str(recipe))
