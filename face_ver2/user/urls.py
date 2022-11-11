from django.urls import path
from user import views

app_name = 'User'
urlpatterns = [

    # ユーザー操作
    # path('user/login/<int:user_id>/', views.user_del, name='user_login'),  # 削除
    path('user_disp/', views.user_disp, name='user_disp'),  # SQLite
    path('user_add/', views.user_edit, name='user_add'),  # SQLite-add
    path('user/mod/<int:user_id>/', views.user_edit, name='user_mod'),  # 修正
    path('user/del/<int:user_id>/', views.user_del, name='user_del'),  # 削除
    path('user/config/<int:user_id>/', views.user_config, name='user_config'),  # 設定


]
