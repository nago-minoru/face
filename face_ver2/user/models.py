from django.db import models


class User(models.Model):
    schoolnum = models.CharField('学籍番号', max_length=5, unique=True)
    user_name = models.CharField('名前', max_length=20)
    password = models.CharField('パスワード', max_length=6)
    free_text = models.CharField('フリーテキスト', blank=True, max_length=255)
    created_at = models.DateTimeField('作成日', auto_now_add=True)
    updated_at = models.DateTimeField('更新日', auto_now=True)

    def __str__(self):
        return self.schoolnum


