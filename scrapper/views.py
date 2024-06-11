from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ScrapingJob, ScrapingTask
from .serializers import ScrapingJobSerializer, ScrapingTaskSerializer, CreateScrapingJobSerializer
from .tasks import scrape_coin_data

class StartScrapingAPIView(APIView):
    def post(self, request):
        serializer = CreateScrapingJobSerializer(data=request.data)
        if serializer.is_valid():
            job = ScrapingJob.objects.create()
            for coin in serializer.validated_data['coins']:
                scrape_coin_data.delay(job.job_id, coin)
            return Response({"job_id": job.job_id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ScrapingStatusAPIView(APIView):
    def get(self, request, job_id):
        try:
            job = ScrapingJob.objects.get(job_id=job_id)
        except ScrapingJob.DoesNotExist:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
        
        tasks = ScrapingTask.objects.filter(job=job)
        tasks_data = ScrapingTaskSerializer(tasks, many=True).data
        return Response({
            "job_id": job.job_id,
            "tasks": tasks_data
        })
