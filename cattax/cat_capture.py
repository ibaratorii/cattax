import cv2
from ultralytics import YOLO
import numpy as np
from .cat_behavior import CatBehaviorAnalyzer, CatBehavior
from django.conf import settings
import os
from collections import defaultdict

def process_video(video_path, analysis_id):
    """处理视频文件并返回分析结果"""
    from api.models import VideoAnalysis
    print(f"Initializing video processing for ID: {analysis_id}")

    try:
        # 初始化模型和分析器
        model = YOLO("yolo11x-seg.pt")
        behavior_analyzer = CatBehaviorAnalyzer()
        print("Models initialized successfully")

        # 打开视频文件
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise Exception(f"Could not open video file: {video_path}")

        # 获取视频属性
        original_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        original_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print(f"Video opened successfully. Total frames: {total_frames}")

        # 调整分辨率（提高到0.5）
        resize_factor = 0.5
        w, h = int(original_w * resize_factor), int(original_h * resize_factor)
        frame_skip = 1  # 处理每一帧

        # 设置输出视频
        output_path = os.path.join(settings.MEDIA_ROOT, 'processed', f'output_{analysis_id}.mp4')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        out = cv2.VideoWriter(output_path, 
                            cv2.VideoWriter_fourcc(*'mp4v'), 
                            fps, 
                            (w, h))

        # 初始化追踪历史和颜色映射
        track_history = defaultdict(lambda: [])
        cat_colors = {1: (0, 255, 0), 2: (255, 0, 0)}
        frame_count = 0
        results_data = []

        # 创建预览窗口
        cv2.namedWindow("Processing Preview", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Processing Preview", 800, 600)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # 调整帧大小
            frame = cv2.resize(frame, (w, h))

            if frame_count % 100 == 0:
                print(f"Processing frame {frame_count}/{total_frames}")

            # 处理每一帧
            results = model.track(frame, persist=True, tracker="bytetrack.yaml", 
                                 classes=[15], conf=0.5)

            frame_results = []
            cat_positions = {}

            if results[0].boxes.id is not None and results[0].masks is not None:
                masks = results[0].masks.xy
                track_ids = results[0].boxes.id.int().cpu().tolist()

                for mask, track_id in zip(masks, track_ids):
                    cat_id = min(track_id, 2)
                    color = cat_colors[cat_id]

                    # 处理掩膜和轮廓
                    mask_img = np.zeros((h, w), dtype=np.uint8)
                    cv2.fillPoly(mask_img, [np.array(mask, dtype=np.int32)], 255)

                    contours, _ = cv2.findContours(mask_img, 
                                                 cv2.RETR_EXTERNAL, 
                                                 cv2.CHAIN_APPROX_SIMPLE)
                    if contours:
                        main_contour = max(contours, key=cv2.contourArea)
                        M = cv2.moments(main_contour)
                        if M["m00"] != 0:
                            cx = int(M["m10"] / M["m00"])
                            cy = int(M["m01"] / M["m00"])
                            cat_positions[cat_id] = (cx, cy)

                            behavior = behavior_analyzer.analyze_behavior(
                                cat_id,
                                main_contour,
                                (cx, cy),
                                frame
                            )

                            # 在帧上绘制结果
                            cv2.drawContours(frame, [main_contour], -1, color, 2)
                            label = f"Cat {cat_id}: {behavior.value if behavior else 'Unknown'}"
                            cv2.putText(frame, label, (cx, cy - 10), 
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

                            # 保存结果
                            frame_results.append({
                                'cat_id': cat_id,
                                'behavior': behavior.value if behavior else 'Unknown',
                                'position': (cx, cy)
                            })

            # 写入处理后的帧
            out.write(frame)
            results_data.append(frame_results)

            # 显示预览（添加进度条）
            progress = (frame_count / total_frames) * 100
            
            # 更新进度 - 确保最后一帧时设置为 100%
            if frame_count == total_frames - 1:
                progress = 100.0

            VideoAnalysis.objects.filter(id=analysis_id).update(
                progress=progress,
                results={'frames': results_data}
            )

            # 检查是否按下 'q' 键退出
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            frame_count += 1

    except Exception as e:
        print(f"Error in process_video: {str(e)}")
        raise

    finally:
        cap.release()
        out.release()
        cv2.destroyAllWindows()

        # 确保在处理完成时设置 100% 进度
        VideoAnalysis.objects.filter(id=analysis_id).update(
            status='completed',
            progress=100.0,
            processed_video=f'processed/output_{analysis_id}.mp4'
        )

    return {
        'total_frames': total_frames,
        'processed_frames': frame_count,
        'results': results_data
    }