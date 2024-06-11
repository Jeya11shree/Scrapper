from django.urls import path
from .views import StartScrapingAPIView, ScrapingStatusAPIView

urlpatterns = [
    path('taskmanager/start_scraping', StartScrapingAPIView.as_view(), name='start_scraping'),
    path('taskmanager/scraping_status/<uuid:job_id>', ScrapingStatusAPIView.as_view(), name='scraping_status'),
]
