from django.test import TestCase
from django.urls import reverse
from .models import Recipe


class RecipeViewsTest(TestCase):
    def setUp(self):
        # Sample recipes
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


    # List & Detail Views Tests

    def test_recipe_list_view_status_code_and_template(self):
        response = self.client.get(reverse("recipes:recipe_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/main.html")  
        self.assertContains(response, "Spaghetti Bolognese")
        self.assertContains(response, "Pancakes")

    def test_recipe_detail_view_valid_recipe(self):
        response = self.client.get(reverse("recipes:recipe_detail", args=[self.recipe1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Spaghetti Bolognese")
        self.assertContains(response, "Classic Italian pasta dish")

    def test_recipe_detail_view_invalid_recipe(self):
        response = self.client.get(reverse("recipes:recipe_detail", args=[999]))
        self.assertEqual(response.status_code, 404)


    # Search Tests

    def test_search_returns_matching_results(self):
        response = self.client.get(reverse("search:search_recipes"), {"q": "Flour"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/main.html") 
        self.assertContains(response, "Pancakes")
        self.assertNotContains(response, "Spaghetti Bolognese")

    def test_search_no_results(self):
        response = self.client.get(reverse("search:search_recipes"), {"q": "Sushi"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/main.html")  
        self.assertContains(response, "No recipes available.")  


    # Model Tests

    def test_str_method(self):
        recipe = Recipe.objects.get(id=self.recipe1.id)
        expected = (
            "Spaghetti Bolognese | Meal: Dinner | Ingredients: Pasta, Meat, Tomato | "
            f"Time: {recipe.cooking_time} min | Difficulty: {recipe.difficulty}"
        )
        self.assertEqual(str(recipe), expected)

    def test_name_max_length(self):
        max_length = self.recipe1._meta.get_field('name').max_length
        self.assertEqual(max_length, 50)

    def test_difficulty_max_length(self):
        max_length = self.recipe1._meta.get_field('difficulty').max_length
        self.assertEqual(max_length, 20)


    # Difficulty Calculation Tests

    def test_calculate_difficulty_easy(self):
        recipe = Recipe(name="Fruit Salad", ingredients="apple, banana", cooking_time=0)
        recipe.save()
        self.assertEqual(recipe.difficulty, "Easy")

    def test_calculate_difficulty_medium(self):
        recipe = Recipe(name="Smoothie", ingredients="banana, milk, yogurt, honey", cooking_time=5)
        recipe.save()
        self.assertEqual(recipe.difficulty, "Medium")

    def test_calculate_difficulty_intermediate(self):
        recipe = Recipe(name="Soup", ingredients="water, carrot", cooking_time=15)
        recipe.save()
        self.assertEqual(recipe.difficulty, "Intermediate")

    def test_calculate_difficulty_hard(self):
        recipe = Recipe(name="Feast", ingredients="chicken, rice, carrots, peas", cooking_time=20)
        recipe.save()
        self.assertEqual(recipe.difficulty, "Hard")


    # Edge Case: Empty Ingredients

    def test_empty_ingredients_handled(self):
        recipe = Recipe(name="Mystery Dish", ingredients="", cooking_time=5)
        recipe.save()
        self.assertIn("None listed", str(recipe))
