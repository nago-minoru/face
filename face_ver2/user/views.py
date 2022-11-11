from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect

# テーブルとDBのフォーム読み込み
from user.models import User
from user.forms import UserForm

# 画像認識の参照
import shutil  # ファイル操作
import os  # OSのファイル操作
import glob  # ワイルドカードの操作


def user_disp(req):
    """ユーザー一覧"""
    users = User.objects.all().order_by('id')
    return render(req, 'user/user_disp.html', {'users': users})


def user_edit(req, user_id=None):
    """ユーザーの編集"""
    # 修正か追加か判断する
    if user_id:  # 修正するユーザID
        user = get_object_or_404(User, schoolnum=user_id)
    else:  # user_id が指定されていない (追加時)
        user = User()  # 追加フォームを作成
    # 修正の送信前か送信後か判断する
    if req.method == 'POST':
        form = UserForm(req.POST, instance=user)  # POST された request データからフォームを作成
        if form.is_valid():  # フォームのバリデーション
            user = form.save(commit=False)
            user.save()
            return render(req, 'user/user_config.html', {'user': user})
    else:
        form = UserForm(instance=user)  # 修正フォームを作成

    return render(req, 'user/user_edit.html', dict(form=form, user_id=user_id))


def user_del(req, user_id=None):
    """ユーザーの削除"""
    user = get_object_or_404(User, schoolnum=user_id)
    user.delete()
    users = User.objects.all().order_by('id')
    return render(req, 'user/user_disp.html', {'users': users})


def user_config(req, user_id=None):
    user = None  # 個人情報の箱
    if user_id:  # 指定のユーザー情報を取得
        user = get_object_or_404(User, schoolnum=user_id)

    return render(req, 'user/user_config.html',
                  {'user': user})


