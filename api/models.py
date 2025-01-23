from django.db import models

class VideoAnalysis(models.Model):
    STATUS_CHOICES = [
        ('uploading', 'Uploading'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ]

    video_file = models.FileField(upload_to='uploads/')
    processed_video = models.FileField(upload_to='processed/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='uploading')
    progress = models.FloatField(default=0)  # 0-100
    results = models.JSONField(default=dict)  # 存储分析结果
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at'] 