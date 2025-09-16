from django.test import TestCase
from django.urls import reverse
from .models import Recipe
from .forms import RecipeForm, RecipeSearchForm, AdvancedSearchForm


# ----------------- Views -----------------

class RecipeViewsTest(TestCase):
    def setUp(self):
        self.recipe1 = Recipe.objects.create(
            name="Spaghetti Bolognese",
            description="Classic Italian pasta dish",
            ingredients="Pasta, Meat, Tomato",
            instructions="Cook pasta. Make sauce. Mix.",
            prep_time=15,
            cooking_time=30
        )
        self.recipe2 = Recipe.objects.create(
            name="Pancakes",
            description="Fluffy breakfast pancakes",
            ingredients="Flour, Eggs, Milk",
            instructions="Mix and fry",
            prep_time=10,
            cooking_time=5
        )

    def test_recipe_list_view(self):
        response = self.client.get(reverse("recipes:recipe_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/main.html")
        self.assertContains(response, "Spaghetti Bolognese")
        self.assertContains(response, "Pancakes")

    def test_recipe_detail_view_valid(self):
        response = self.client.get(reverse("recipes:recipe_detail", args=[self.recipe1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Spaghetti Bolognese")

    def test_recipe_detail_view_invalid(self):
        response = self.client.get(reverse("recipes:recipe_detail", args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_search_results_found(self):
        response = self.client.get(reverse("recipes:search_recipes"), {"q": "Flour"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/main.html")
        self.assertContains(response, "Pancakes")
        self.assertNotContains(response, "Spaghetti Bolognese")

    def test_search_results_not_found(self):
        response = self.client.get(reverse("recipes:search_recipes"), {"q": "Sushi"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No recipes available.")


# ----------------- Models -----------------

class RecipeModelTest(TestCase):
    def setUp(self):
        self.recipe = Recipe.objects.create(
            name="Spaghetti Bolognese",
            ingredients="Pasta, Meat, Tomato",
            instructions="Cook pasta. Make sauce. Mix.",
            prep_time=15,
            cooking_time=30
        )

    def test_str_method(self):
        expected = (
            "Spaghetti Bolognese | Meal: Dinner | Ingredients: Pasta, Meat, Tomato | "
            f"Time: {self.recipe.cooking_time} min | Difficulty: {self.recipe.difficulty}"
        )
        self.assertEqual(str(self.recipe), expected)

    def test_name_max_length(self):
        max_length = self.recipe._meta.get_field("name").max_length
        self.assertEqual(max_length, 50)

    def test_difficulty_max_length(self):
        max_length = self.recipe._meta.get_field("difficulty").max_length
        self.assertEqual(max_length, 20)


# ----------------- Difficulty -----------------

class DifficultyCalculationTest(TestCase):
    def test_easy(self):
        recipe = Recipe.objects.create(name="Fruit Salad", ingredients="apple, banana", cooking_time=0)
        self.assertEqual(recipe.difficulty, "Easy")

    def test_medium(self):
        recipe = Recipe.objects.create(name="Smoothie", ingredients="banana, milk, yogurt, honey", cooking_time=5)
        self.assertEqual(recipe.difficulty, "Medium")

    def test_intermediate(self):
        recipe = Recipe.objects.create(name="Soup", ingredients="water, carrot", cooking_time=15)
        self.assertEqual(recipe.difficulty, "Intermediate")

    def test_hard(self):
        recipe = Recipe.objects.create(name="Feast", ingredients="chicken, rice, carrots, peas", cooking_time=20)
        self.assertEqual(recipe.difficulty, "Hard")

    def test_empty_ingredients(self):
        recipe = Recipe.objects.create(name="Mystery Dish", ingredients="", cooking_time=5)
        self.assertIn("None listed", str(recipe))


# ----------------- Forms -----------------

class RecipeFormTest(TestCase):
    def test_valid_form(self):
        form = RecipeForm(data={
            "name": "Omelette",
            "ingredients": "Eggs, butter",
            "instructions": "Whisk and fry",
            "meal_type": "breakfast",
            "difficulty": "easy",
            "cooking_time": 5,
        })
        self.assertTrue(form.is_valid())

    def test_invalid_missing_name(self):
        form = RecipeForm(data={
            "ingredients": "Eggs",
            "instructions": "Cook",
            "meal_type": "breakfast",
            "difficulty": "easy",
            "cooking_time": 5,
        })
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_name_max_length(self):
        form = RecipeForm(data={
            "name": "X" * 51,
            "ingredients": "Eggs",
            "instructions": "Cook",
            "meal_type": "lunch",
            "difficulty": "easy",
            "cooking_time": 10,
        })
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)


class RecipeSearchFormTest(TestCase):
    def test_empty_is_valid(self):
        form = RecipeSearchForm(data={})
        self.assertTrue(form.is_valid())

    def test_with_title(self):
        form = RecipeSearchForm(data={"title": "Pasta"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["title"], "Pasta")


class AdvancedSearchFormTest(TestCase):
    def test_valid_form(self):
        form = AdvancedSearchForm(data={
            "name": "Cake",
            "ingredient": "Flour",
            "meal_type": "dessert",
            "difficulty": "medium",
            "max_cooking_time": 60,
        })
        self.assertTrue(form.is_valid())

    def test_invalid_max_cooking_time(self):
        form = AdvancedSearchForm(data={"max_cooking_time": "not_a_number"})
        self.assertFalse(form.is_valid())
        self.assertIn("max_cooking_time", form.errors)
