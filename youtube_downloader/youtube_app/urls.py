from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home_page'),
    path('support/', views.support, name='support_page'),
    path('search_results/', views.search_results, name='search_results'),
    path('download/<str:id>/', views.download, name='download_page'),
    path('download_audio/<str:pk>/', views.download_audio, name='download_mp3'),
    path('history/', views.history, name="history_page"),
    path('success_massage/', views.success_massage, name="success_massage"),
]
