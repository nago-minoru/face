# Generated by Django 2.2 on 2019-04-19 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schoolnum', models.CharField(max_length=5, unique=True, verbose_name='学籍番号')),
                ('user_name', models.CharField(max_length=20, verbose_name='名前')),
                ('password', models.CharField(max_length=6, verbose_name='パスワード')),
                ('free_text', models.CharField(blank=True, max_length=255, verbose_name='フリーテキスト')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日')),
            ],
        ),
    ]
