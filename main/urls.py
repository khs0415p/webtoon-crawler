from django.urls import path
from .views import WebtoonRealtimeView, WebtoonDayView

app_name = 'main'

urlpatterns = [
    # webtoon
    path('', WebtoonRealtimeView.as_view()),
    path('', WebtoonDayView.as_view()),
    
    # book
    
]