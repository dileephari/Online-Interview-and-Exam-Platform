from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserForm(UserCreationForm):
    # Hidden field for user_type (Hire / Practice)
    user_type = forms.ChoiceField(
        choices=(
            ('hire', 'Hire Tech Talent'),
            ('practice', 'Practice & Prepare')
        ),
        widget=forms.HiddenInput()
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'user_type')

    def save(self, commit=True):
        """
        Override save to prevent saving user_type to User model directly.
        Profile creation will handle user_type separately in views.
        """
        user = super().save(commit=commit)
        return user
