from django.urls import path
from FaceShoot import views

app_name = 'FaceShoot'
urlpatterns = [

    # お試し
    path('picture/', views.picture_list, name='picture'),  # 画像アップロード①
    path('imagelist/', views.imagelist, name='imagelist'),  # 画像アップロード②


    # MySQL実験
    path('mysql_disp/', views.mysql_disp, name='mysql_disp'),  # MySQLの実験
    path('search/', views.search, name='search'),  # MySQL検索
    path('mysql_add/', views.mysql_add, name='mysql_add'),  # MySQL追加入力ページへのへのリンク
    path('mysql_insert/', views.mysql_insert, name='mysql_insert'),  # MySQL追加実行
    path('mysql_update/<int:schoolnum>', views.mysql_update, name='mysql_update'),  # MySQL更新リンク
    path('mysql_update_commit/', views.mysql_update_commit, name='mysql_update_commit'),  # MySQL更新実行
    path('mysql_del/<int:schoolnum>', views.mysql_del, name='mysql_del'),  # MySQL削除リンクページ
    path('mysql_delete_commit/', views.mysql_delete_commit, name='mysql_delete_commit'),  # MySQL削除実行


    # ユーザー操作
    path('user_disp/', views.user_disp, name='user_disp'),  # SQLite
    path('user_add/', views.user_edit, name='user_add'),  # SQLite-add
    path('user/mod/<int:user_id>/', views.user_edit, name='user_mod'),  # 修正
    path('user/del/<int:user_id>/', views.user_del, name='user_del'),  # 削除


    # 顔認証の処理
    path('facepic/<int:school_num>', views.learn_face, name='facepic'),  # 写真撮影
    path('ninsyo/', views.ninsyo, name='ninsyo'),  # 認証
    path('login/<int:user_id>', views.login, name='login'),  # ユーザー指定
    path('get_image/', views.get_image, name='get_image'),  # 画像取得
    path('user_face_learn/<int:user_id>', views.user_face_learn, name='user_face_learn'),  # 個人の顔で学習する


    # いらない画像を消す処理
    path('imgdel/', views.imgdel, name='imgdel'),  # 全部の顔一覧から選択した画像を削除する
    path('user_face_del/', views.user_face_del, name='user_face_del'),  # 全部の顔一覧から選択した画像を削除する
    path('user_this_time_face_del/',
         views.user_this_time_face_del,
         name='user_this_time_face_del'),  # 今回撮影した顔一覧から選択した画像を削除する


    # QRcode
    path('qr_code/', views.qr_code, name='qr_code'),



]
