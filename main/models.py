from django.db import models

# Create your models here.
class NaverRealtime:
    title = models.CharField(max_length=50)
    thumbnail = models.ImageField(upload_to="%Y/%m/%d/naver")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class KakaoRealtime:
    title = models.CharField(max_length=50)
    thumbnail = models.ImageField(upload_to="%Y/%m/%d/naver")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)