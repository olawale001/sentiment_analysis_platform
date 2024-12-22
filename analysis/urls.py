from django.urls import path
from .views import SentimentAnalysisView, download_csv
from .views import index, dashboard

urlpatterns = [
    path('', index, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('analyze/', SentimentAnalysisView.as_view(), name='analyze_sentiment'),
    path('download-csv/', download_csv, name='download_csv'),
]
