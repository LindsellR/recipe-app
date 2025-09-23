from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from recipes.models import Recipe
from users.models import Favourite
from .forms import UserProfileForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core import mail


class FavouritesViewTest(TestCase):
    def setUp(self):
        # create user + login
        self.user = User.objects.create_user(username="tester", password="secret")
        self.client.login(username="tester", password="secret")

        # create recipe
        self.recipe = Recipe.objects.create(
            name="Pasta",
            ingredients="Noodles, sauce",
            instructions="Cook and eat",
            cooking_time=10,
        )

    def test_add_favourite(self):
        response = self.client.get(reverse("users:add_favourite", args=[self.recipe.id]))
        self.assertRedirects(response, reverse("recipes:recipe_list"))
        self.assertTrue(Favourite.objects.filter(user=self.user, recipe=self.recipe).exists())

    def test_remove_favourite(self):
        Favourite.objects.create(user=self.user, recipe=self.recipe)
        response = self.client.get(reverse("users:remove_favourite", args=[self.recipe.id]))
        self.assertRedirects(response, reverse("recipes:recipe_list"))
        self.assertFalse(Favourite.objects.filter(user=self.user, recipe=self.recipe).exists())

    def test_user_favourites_list(self):
        Favourite.objects.create(user=self.user, recipe=self.recipe)
        response = self.client.get(reverse("users:user_favourites"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pasta")


class UserProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="secret", email="old@mail.com")
        self.client.login(username="tester", password="secret")

    def test_update_email_only(self):
        response = self.client.post(reverse("users:edit_profile"), {
            "username": "tester",
            "email": "new@mail.com",
            "password": "",
        })
        self.assertRedirects(response, reverse("users:profile"), fetch_redirect_response=False)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "new@mail.com")

    def test_update_password(self):
        response = self.client.post(reverse("users:edit_profile"), {
            "username": "tester",
            "email": "old@mail.com",
            "password": "newpass123",
        })
        self.assertRedirects(response, reverse("users:profile"), fetch_redirect_response=False)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpass123"))


class UserRecipesTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="chef", password="secret")
        self.client.login(username="chef", password="secret")

    def test_add_recipe(self):
        response = self.client.post(reverse("users:add_recipe"), {
            "name": "Omelette",
            "ingredients": "Eggs, butter",
            "instructions": "Whisk and fry",
            "cooking_time": 5,
            "meal_type": "breakfast"
        })
        
        self.assertRedirects(response, reverse("users:my_recipes"))
        self.assertTrue(Recipe.objects.filter(name="Omelette", created_by=self.user).exists())

    def test_edit_recipe(self):
        recipe = Recipe.objects.create(name="Toast", ingredients="Bread", instructions="Toast it", cooking_time=2, created_by=self.user)
        response = self.client.post(reverse("users:edit_recipe", args=[recipe.id]), {
            "name": "French Toast",
            "ingredients": "Bread, eggs",
            "instructions": "Dip and fry",
            "cooking_time": 10,
            "meal_type": "breakfast"
        })
       
        self.assertRedirects(response, reverse("users:my_recipes"))
        recipe.refresh_from_db()
        self.assertEqual(recipe.name, "French Toast")

    def test_delete_recipe(self):
        recipe = Recipe.objects.create(name="Soup", ingredients="Water", instructions="Boil", cooking_time=15, created_by=self.user)
        response = self.client.post(reverse("users:delete_recipe", args=[recipe.id]))
        self.assertRedirects(response, reverse("users:my_recipes"))
        self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())

class UserProfileFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="oldpassword",
            email="old@example.com"
        )

    def test_form_valid_without_password_change(self):
        form = UserProfileForm(
            data={"username": "testuser", "email": "new@example.com", "password": ""},
            instance=self.user
        )
        self.assertTrue(form.is_valid())
        updated_user = form.save()
        self.assertEqual(updated_user.email, "new@example.com")
        # Password should remain unchanged
        self.assertTrue(updated_user.check_password("oldpassword"))

    def test_form_valid_with_password_change(self):
        form = UserProfileForm(
            data={"username": "testuser", "email": "updated@example.com", "password": "newpassword123"},
            instance=self.user
        )
        self.assertTrue(form.is_valid())
        updated_user = form.save()
        self.assertEqual(updated_user.email, "updated@example.com")
        # Password should now be the new one
        self.assertTrue(updated_user.check_password("newpassword123"))

    def test_invalid_without_username(self):
        form = UserProfileForm(
            data={"username": "", "email": "x@example.com", "password": ""},
            instance=self.user
        )
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_email_optional(self):
        form = UserProfileForm(
            data={"username": "testuser", "email": "", "password": ""},
            instance=self.user
        )
        self.assertTrue(form.is_valid())
        updated_user = form.save()
        # Email can be blank
        self.assertEqual(updated_user.email, "")

class UserProfileFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="old@example.com", password="oldpassword"
        )

    def test_valid_form_with_updated_username_and_email(self):
        form_data = {
            "username": "newusername",
            "email": "new@example.com",
            "password": ""  # leave blank to keep current password
        }
        form = UserProfileForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
        updated_user = form.save(commit=False)
        self.assertEqual(updated_user.username, "newusername")
        self.assertEqual(updated_user.email, "new@example.com")

    def test_valid_form_with_new_password(self):
        form_data = {
            "username": "testuser",
            "email": "old@example.com",
            "password": "newsecurepassword123"
        }
        form = UserProfileForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
        updated_user = form.save(commit=False)
        # The raw password won't be visible; check via set_password hashing
        updated_user.set_password(form.cleaned_data["password"])
        self.assertTrue(updated_user.check_password("newsecurepassword123"))

    def test_invalid_form_missing_username(self):
        form_data = {
            "username": "",
            "email": "new@example.com",
            "password": ""
        }
        form = UserProfileForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_invalid_form_invalid_email(self):
        form_data = {
            "username": "testuser",
            "email": "not-an-email",
            "password": ""
        }
        form = UserProfileForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

class SignupViewTest(TestCase):
    def test_signup_valid(self):
        response = self.client.post(reverse("signup"), {
            "username": "newuser",
            "email": "new@example.com",
            "password": "securepass123",
            "password_confirm": "securepass123",
        })
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_signup_password_mismatch(self):
        response = self.client.post(reverse("signup"), {
            "username": "newuser",
            "email": "new@example.com",
            "password": "securepass123",
            "password_confirm": "wrongpass",
        })
        self.assertEqual(response.status_code, 200)  # stays on page
        self.assertContains(response, "Passwords do not match.")
        self.assertFalse(User.objects.filter(username="newuser").exists())

    def test_signup_invalid_email(self):
        response = self.client.post(reverse("signup"), {
            "username": "newuser",
            "email": "invalid-email",
            "password": "securepass123",
            "password_confirm": "securepass123",
        })
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertFormError(form, "email", "Enter a valid email address.")


class LoginViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="secret")

    def test_login_valid(self):
        response = self.client.post(reverse("login"), {
            "username": "tester",
            "password": "secret",
        })
        self.assertEqual(response.status_code, 302)  # redirect after login
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_invalid(self):
        response = self.client.post(reverse("login"), {
            "username": "tester",
            "password": "wrongpass",
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertContains(response, "Please enter a correct username and password")

class PasswordValidationTest(TestCase):
    def test_short_password_invalid(self):
        with self.assertRaises(ValidationError):
            validate_password("123")

    def test_common_password_invalid(self):
        with self.assertRaises(ValidationError):
            validate_password("password")

    def test_numeric_only_invalid(self):
        with self.assertRaises(ValidationError):
            validate_password("12345678")

    def test_valid_password(self):
        try:
            validate_password("GoodPassword123")
        except ValidationError:
            self.fail("Valid password raised ValidationError unexpectedly!")


class PasswordResetFlowTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tester", email="tester@example.com", password="secret"
        )

    def test_password_reset_email_sent(self):
        response = self.client.post(reverse("password_reset"), {
            "email": "tester@example.com"
        })
        self.assertRedirects(response, reverse("password_reset_done"))
        self.assertEqual(len(mail.outbox), 1)  # one email should be sent
        self.assertIn("tester@example.com", mail.outbox[0].to)

    def test_password_reset_invalid_email(self):
        response = self.client.post(reverse("password_reset"), {
            "email": "nobody@example.com"
        })
        self.assertRedirects(response, reverse("password_reset_done"))
        self.assertEqual(len(mail.outbox), 0)  # no email sent
