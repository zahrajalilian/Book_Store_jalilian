from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    """
    a form for our custom user
    """

    class Meta(UserCreationForm):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('company', 'address', 'phone', 'fax',)


class CustomUserChangeForm(UserChangeForm):

    """
    a form for change custom user
    """
    class Meta(UserChangeForm):

        model = CustomUser

        fields = UserChangeForm.Meta.fields



