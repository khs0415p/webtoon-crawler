from typing import Any
from django.shortcuts import render, get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from main.models import *
# Create your views here.


class WebtoonRealtimeView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'webtoon_realtime.html'
        
    def get(self, request):
        ## 실시간 순위
        # naver (시간)
        # naver = NaverRealtime.object.filter(update_at__range = [start_day, end_day])
        
        # kakao
        # toptoon
        # lezhin
        # toomics
        # ridi
        
        return Response({'naver': "naver", "kakao": "kakao", "toptoon": "toptoon", "lezhin": "lezhin", "toomics":"toomics", "ridi":"ridi"})



class WebtoonDayView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'webtoon_realtime.html'
        
    def get(self, request):
        ## 실시간 순위
        # naver
        # kakao
        # toptoon
        # lezhin
        # toomics
        # ridi
        
        return Response({'naver': "naver", "kakao": "kakao", "toptoon": "toptoon", "lezhin": "lezhin", "toomics":"toomics", "ridi":"ridi"})