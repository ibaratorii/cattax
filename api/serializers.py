from rest_framework import serializers
from .models import VideoAnalysis

class VideoAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoAnalysis
        fields = ['id', 'video_file', 'processed_video', 'status', 'progress', 'results']
        read_only_fields = ['processed_video', 'status', 'progress', 'results'] 