from django.db import models
from django.contrib.auth.models import User
from recipes.models import Recipe

# create your models here


class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favourites")
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="favourited_by"
    )
    pic = models.ImageField(upload_to="favourites", default="no_picture.jpg")

    class Meta:
        unique_together = ("user", "recipe")  # Prevent duplicate favourites
        verbose_name = "Favourite"
        verbose_name_plural = "Favourites"

    def __str__(self):
        return f"{self.user.username} → {self.recipe.name}"
