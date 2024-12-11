import os
from unittest import result
from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SentimentAnalysisSerializer
from .utils import analysis_sentiment, analyze_csv, generate_sentiment_chart
from .models import SentimentAnalysis

class SentimentAnalysisView(APIView):
    def post(self, request):
        file = request.FILE.get("file")
        text = request.data.get("text")

        if file:
            file_path = os.path.join(settings.MEDIA_ROOT, file.name)
            with open(file_path, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)

            results = analyze_csv(file_path)
            SentimentAnalysis.objects.bulk_create(
                [SentimentAnalysis(text=result["text"], sentiment=result["sentiment"], confidence=result["confidence"]) for result in results]

            )   
            return Response({"message": "File processed successfully", "results": results}, status=status.HTTP_201_CREATED)     
        elif text:
            result = analysis_sentiment(text)
            sentiment_instance = SentimentAnalysis.objects.create(
                text=text, sentiment=result["sentiment"], confidence=result["confidence"]
            )
            serializer = SentimentAnalysisSerializer(sentiment_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response({"error": "Please provide text or a file"}, status=status.HTTP_400_BAD_REQUEST)
    

def index(request):
    return render(request, "index.html")    

def dashboard(request):
    chart = generate_sentiment_chart
    return render(request, "dashboard.html", {"chart": chart})