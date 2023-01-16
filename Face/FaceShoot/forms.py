from django.forms import ModelForm
from FaceShoot.models import SimplePhoto, User


class SimplePhotoForm(ModelForm):
    """画像アップロード"""
    class Meta:
        model = SimplePhoto
        fields = ['simple_img', 'simple_name', ]


class UserForm(ModelForm):
    """ユーザーのフォーム"""
    class Meta:
        model = User
        fields = ('schoolnum', 'user_name', 'password', 'free_text', )




