from django.urls import path
from tool import views

app_name = 'Tool'
urlpatterns = [

    path('tool/top/', views.tool_top, name='tool_top'),  # top
    path('tool/seiki/', views.tool_seiki, name='tool_seikihyogen'),  # 正規表現
    path('tool/seiki/履歴', views.tool_seiki_rireki, name='tool_seiki_rireki'),  # 正規表現の履歴

]
