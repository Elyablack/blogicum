# users/forms.py
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

User = get_user_model()


class ProfileCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email')


class ProfileEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )