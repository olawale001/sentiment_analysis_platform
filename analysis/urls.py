from django.urls import path
from .views import SentimentAnalysisView
from .views import index, dashboard

urlpatterns = [
    path('', index, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('analyze/', SentimentAnalysisView.as_view(), name='analyze_sentiment'),
]
