import cv2
import numpy as np
from collections import defaultdict, deque, Counter
from enum import Enum
from scipy.spatial.distance import cosine, euclidean

class CatBehavior(Enum):
    WALKING = "walking"      # 移动状态
    RESTING = "resting"      # 静止状态（包括坐着和躺着）
    STANDING = "standing"    # 站立状态
    UNKNOWN = "unknown"      # 无法识别

class CatBehaviorAnalyzer:
    def __init__(self):
        self.prev_positions = {}
        self.static_duration = defaultdict(int)
        # 添加行为历史记录，用于平滑处理
        self.behavior_history = defaultdict(lambda: deque(maxlen=5))
        # 增加状态切换的阈值
        self.state_change_threshold = 3

    def analyze_behavior(self, cat_id, contour, position, frame):
        """分析猫的行为"""
        try:
            # 基本特征
            (x, y, w, h) = cv2.boundingRect(contour)
            aspect_ratio = float(w) / h
            area = cv2.contourArea(contour)
            
            # 形状特征
            perimeter = cv2.arcLength(contour, True)
            compactness = 4 * np.pi * area / (perimeter * perimeter) if perimeter > 0 else 0
            
            # 计算轮廓的主要特征
            if len(contour) >= 5:
                hull = cv2.convexHull(contour)
                hull_area = cv2.contourArea(hull)
                solidity = float(area) / hull_area if hull_area > 0 else 0
                
                # 分析轮廓的形状特征
                _, (width, height), _ = cv2.fitEllipse(contour)
                shape_ratio = min(width, height) / max(width, height)
            else:
                solidity = 1
                shape_ratio = 1
            
            # 计算运动特征，增加容忍度
            is_moving = False
            if cat_id in self.prev_positions:
                prev_pos = self.prev_positions[cat_id]
                movement = np.sqrt((position[0] - prev_pos[0])**2 + 
                                 (position[1] - prev_pos[1])**2)
                is_moving = movement > 15  # 增加移动阈值，减少抖动影响
            
            self.prev_positions[cat_id] = position
            
            # 行为判断逻辑
            current_behavior = None
            if is_moving and aspect_ratio > 1.2:
                current_behavior = CatBehavior.WALKING
            else:
                # 静止状态的判断
                if solidity > 0.75 and shape_ratio > 0.6:
                    # 形状紧凑且较为圆润，可能是蜷缩/休息状态
                    current_behavior = CatBehavior.RESTING
                elif aspect_ratio < 0.7:
                    # 明显的竖直特征才判断为站立
                    current_behavior = CatBehavior.STANDING
                else:
                    current_behavior = CatBehavior.RESTING
            
            # 使用历史记录来平滑行为判断
            self.behavior_history[cat_id].append(current_behavior)
            
            # 只有当新状态在历史记录中占主导地位时才改变状态
            behavior_counts = Counter(self.behavior_history[cat_id])
            most_common_behavior = behavior_counts.most_common(1)[0][0]
            if behavior_counts[most_common_behavior] >= self.state_change_threshold:
                return most_common_behavior
            
            # 如果没有明显的主导状态，保持当前状态
            return current_behavior if len(self.behavior_history[cat_id]) < self.state_change_threshold else most_common_behavior
            
        except Exception as e:
            print(f"Error in analyze_behavior: {str(e)}")
            return CatBehavior.UNKNOWN

    def detect_background_motion(self, frame):
        if self.last_frame is None:
            self.last_frame = frame.copy()
            return np.zeros(2)
        
        # 使用光流法检测背景运动
        prev_gray = cv2.cvtColor(self.last_frame, cv2.COLOR_BGR2GRAY)
        curr_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 计算整体光流
        flow = cv2.calcOpticalFlowFarneback(prev_gray, curr_gray, None, 
                                          0.5, 3, 15, 3, 5, 1.2, 0)
        
        # 计算平均运动向量
        avg_motion = np.mean(flow, axis=(0,1))
        
        self.last_frame = frame.copy()
        return avg_motion
        
    def calculate_relative_speed(self, positions, background_motion):
        if len(positions) < 2:
            return 0
        
        # 计算猫咪的实际运动
        p1, p2 = positions[-2], positions[-1]
        cat_motion = np.array([p2[0] - p1[0], p2[1] - p1[1]])
        
        # 减去背景运动的影响
        relative_motion = cat_motion - background_motion
        
        # 计算相对速度并添加阈值过滤
        speed = np.sqrt(np.sum(relative_motion**2))
        
        # 添加噪声过滤
        if speed < 0.1:  # 极小的移动视为静止
            return 0
        return speed

    def analyze_shape(self, contour):
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        if perimeter == 0:
            return None
            
        circularity = 4 * np.pi * area / (perimeter * perimeter)
        rect = cv2.minAreaRect(contour)
        width, height = rect[1]
        if width == 0 or height == 0:
            return None
            
        aspect_ratio = max(width, height) / min(width, height)
        
        # 调整形状判断的阈值，让蜷缩状态更容易被识别
        if circularity > 0.6 and aspect_ratio < 2.0:  # 更宽松的圆形判定
            return CatBehavior.SLEEPING
        elif circularity > 0.5:  # 较圆
            return CatBehavior.SITTING
        elif aspect_ratio > 2.8:  # 细长
            return CatBehavior.WALKING
        return CatBehavior.SITTING  # 默认返回坐着，而不是None

    def check_interaction(self, cat1_pos, cat2_pos, threshold=100):
        if cat1_pos is None or cat2_pos is None:
            return False
        distance = np.sqrt((cat1_pos[0] - cat2_pos[0])**2 + 
                         (cat1_pos[1] - cat2_pos[1])**2)
        return distance < threshold

    def analyze_appearance(self, appearance, cat_id):
        """分析猫咪的外观特征来辅助判断姿态"""
        if appearance is None:
            return None

        # 存储外观特征历史
        self.appearance_history[cat_id].append(appearance)
        
        if len(self.appearance_history[cat_id]) < 2:
            return None

        # 计算外观变化
        prev_appearance = self.appearance_history[cat_id][-2]
        appearance_diff = np.sum(np.abs(appearance - prev_appearance))
        
        # 分析外观特征的分布
        feature_distribution = np.histogram(appearance, bins=8)[0]
        feature_concentration = np.max(feature_distribution) / np.sum(feature_distribution)
        
        # 根据外观特征判断可能的姿态
        if feature_concentration > 0.4:  # 特征集中说明姿态比较紧凑
            if appearance_diff < 0.1:  # 外观变化很小
                return "compact"  # 蜷缩/睡觉姿态
            else:
                return "active"  # 活跃姿态
        else:  # 特征分散说明姿态舒展
            if appearance_diff < 0.1:
                return "rest"    # 休息姿态
            else:
                return "moving"  # 移动姿态

    def _get_orientation(self, contour):
        """计算轮廓的主方向"""
        try:
            (_, _), (MA, ma), angle = cv2.fitEllipse(contour)
            return angle
        except:
            return 0

    def _detect_behavior(self, contour, center_point, other_cat_pos, appearance):
        # 实现具体的行为检测逻辑
        # 返回一个行为标签
        pass