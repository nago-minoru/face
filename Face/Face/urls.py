from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include   # ←, includeを追加
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('Face/', include('FaceShoot.urls')),   # アプリ別のURLを読み込み
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
