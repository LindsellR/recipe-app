# users/forms.py
from django import forms
from django.contrib.auth.models import User

class UserProfileForm(forms.ModelForm):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        required=False,  # optional; only fill if changing password
        help_text="Leave blank to keep current password."
    )
    email = forms.EmailField(
        label="Email",
        required=False,  # optional
        help_text="Optional. Add an email if you want to receive notifications."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)  # only change password if provided
        if commit:
            user.save()
        return user
