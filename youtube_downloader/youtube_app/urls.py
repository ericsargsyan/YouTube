from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home_page'),
    path('support/', views.SupportView.as_view(), name='support_page'),
    path('search_results/', views.search_results, name='search_results'),
    path('download/<str:id>/', views.download, name='download_page'),
    path('download_audio/<str:pk>/', views.download_audio, name='download_mp3'),
    # path('history/', views.history, name="history_page"),
    path('history/', views.HistoryView.as_view(), name="history_page"),
    path('success_massage/', views.MassageView.as_view(), name="success_massage"),
    path('playlist_history/', views.playlist_history, name="playlist_history"),
    path('playlist_mp4/', views.playlist_mp4, name="playlist_mp4"),
    path('playlist_mp3/', views.playlist_mp3, name="playlist_mp3"),
]
