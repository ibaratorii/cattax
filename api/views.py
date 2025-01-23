from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.conf import settings
import os
import cv2
from .serializers import VideoAnalysisSerializer
from .models import VideoAnalysis
from .tasks import process_video_task

class VideoAnalysisViewSet(viewsets.ModelViewSet):
    queryset = VideoAnalysis.objects.all()
    serializer_class = VideoAnalysisSerializer

    @action(detail=False, methods=['POST'])
    def upload_video(self, request):
        """处理视频上传并开始分析"""
        try:
            # 添加日志
            print("Received upload request")
            video_file = request.FILES.get('video')
            if not video_file:
                return Response({'error': 'No video file provided'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            print(f"Processing video: {video_file.name}")  # 添加日志
            # 保存上传的视频
            video_path = os.path.join(settings.MEDIA_ROOT, 'uploads', video_file.name)
            os.makedirs(os.path.dirname(video_path), exist_ok=True)
            
            with open(video_path, 'wb+') as destination:
                for chunk in video_file.chunks():
                    destination.write(chunk)

            # 创建分析任务记录
            analysis = VideoAnalysis.objects.create(
                video_file=f'uploads/{video_file.name}',
                status='processing'
            )

            # 使用Celery异步处理视频
            task = process_video_task.delay(video_path, analysis.id)  # 使用 delay 而不是 apply_async
            
            return Response({
                'id': analysis.id,
                'task_id': task.id,
                'status': 'processing',
                'message': 'Video upload successful, processing started'
            })
        except Exception as e:
            print(f"Error in upload_video: {str(e)}")
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['GET'])
    def status(self, request, pk=None):
        """获取视频分析状态"""
        try:
            analysis = VideoAnalysis.objects.get(pk=pk)
            return Response({
                'id': analysis.id,
                'status': analysis.status,
                'progress': analysis.progress,
                'results': analysis.results
            })
        except VideoAnalysis.DoesNotExist:
            return Response({'error': 'Analysis not found'}, 
                          status=status.HTTP_404_NOT_FOUND) 