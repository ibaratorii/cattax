from django.contrib import admin
from .models import VideoAnalysis

@admin.register(VideoAnalysis)
class VideoAnalysisAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'progress', 'created_at', 'updated_at']
    list_filter = ['status']
    readonly_fields = ['progress', 'results', 'created_at', 'updated_at'] 