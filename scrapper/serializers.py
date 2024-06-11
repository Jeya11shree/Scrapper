from rest_framework import serializers
from .models import ScrapingJob, ScrapingTask

class ScrapingJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapingJob
        fields = ['job_id', 'created_at', 'status']

class ScrapingTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapingTask
        fields = ['coin', 'data', 'status', 'created_at']

class CreateScrapingJobSerializer(serializers.Serializer):
    coins = serializers.ListField(
        child=serializers.CharField(max_length=10),
        allow_empty=False
    )
