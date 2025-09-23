# users/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserProfileForm(forms.ModelForm):
    """
    Form for updating user profile details.
    - Username can be changed.
    - Email is optional (but recommended).
    - Password is optional: only update if provided.
    """

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        required=False,  # only set if user wants to change password
        help_text="Leave blank to keep current password."
    )
    email = forms.EmailField(
        label="Email",
        required=False,
        help_text="Optional. Add an email if you want to receive notifications."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        """Override save to handle password hashing if provided."""
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)  # hash password properly
        if commit:
            user.save()
        return user

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=False, help_text="Optional email")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


