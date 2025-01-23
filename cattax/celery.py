from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cattax.settings')

# 创建 celery 应用
app = Celery('cattax')

# 从Django设置文件中导入celery配置
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动发现任务
app.autodiscover_tasks()

# 基本配置
app.conf.update(
    broker_url='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/0',
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Shanghai',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,
    worker_prefetch_multiplier=1,
    task_always_eager=False,  # 确保任务在 worker 中执行
)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}') 