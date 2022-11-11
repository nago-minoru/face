from django.forms import ModelForm
from user.models import User


class UserForm(ModelForm):
    """ユーザーのフォーム"""
    class Meta:
        model = User
        fields = ('schoolnum', 'user_name', 'password', 'free_text', )




