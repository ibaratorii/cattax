from celery import shared_task
from cattax.cat_capture import process_video
from cattax.cat_behavior import CatBehaviorAnalyzer
from .models import VideoAnalysis
import logging

logger = logging.getLogger(__name__)

@shared_task(name='api.tasks.process_video_task')  # 使用完整的任务名称
def process_video_task(video_path, analysis_id):  # 移除 bind=True 和 self
    try:
        print(f"Starting to process video: {video_path} with ID: {analysis_id}")  # 添加日志
        process_video(video_path, analysis_id)
        print(f"Video processing completed for ID: {analysis_id}")  # 添加日志
    except Exception as e:
        print(f"Error in process_video_task: {str(e)}")
        logger.error(f"Error processing video {analysis_id}: {str(e)}", exc_info=True)  # 添加详细错误日志
        VideoAnalysis.objects.filter(id=analysis_id).update(
            status='failed',
            results={'error': str(e)}
        )
        raise 