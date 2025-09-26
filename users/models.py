from django.db import models
from django.contrib.auth.models import User
from recipes.models import Recipe


class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favourites")
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="favourited_by"
    )
    pic = models.CharField(
        max_length=100,
        default="no_picture.jpg",
        help_text="Filename of the favourite recipe image in static/recipes/images/"
    )

    class Meta:
        unique_together = ("user", "recipe")
        verbose_name = "Favourite"
        verbose_name_plural = "Favourites"

    def __str__(self):
        return f"{self.user.username} → {self.recipe.name}"
