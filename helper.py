import torch
import mediapipe as mp 
import numpy as np
from torchvision import transforms
from statistics import mean
from pynput.keyboard import Controller, Key

# 创建键盘控制器
keyboard = Controller()
# 创建键盘按键绑定
keybinds = {'hook':'j', 'kick':'k', 'special':'o', 'crouch':'s'}

# 坐标提取方法
def extract_coordinates(output, mpPose):
    output_list = []
    lms_list = [
        mpPose.PoseLandmark.NOSE,               # 鼻子
        mpPose.PoseLandmark.RIGHT_SHOULDER,     # 右肩
        mpPose.PoseLandmark.LEFT_SHOULDER,      # 左肩
        mpPose.PoseLandmark.LEFT_ELBOW,         # 左肘
        mpPose.PoseLandmark.RIGHT_ELBOW,        # 右肘
        mpPose.PoseLandmark.LEFT_WRIST,         # 左手腕
        mpPose.PoseLandmark.RIGHT_WRIST,        # 右手腕
        mpPose.PoseLandmark.LEFT_PINKY,         # 左手指
        mpPose.PoseLandmark.RIGHT_PINKY,        # 右手指
        mpPose.PoseLandmark.LEFT_INDEX,         # 左手指
        mpPose.PoseLandmark.RIGHT_INDEX,        # 右手指
        mpPose.PoseLandmark.LEFT_THUMB,         # 左手拇指
        mpPose.PoseLandmark.RIGHT_THUMB,        # 右手拇指
        mpPose.PoseLandmark.LEFT_HIP,           # 左臀
        mpPose.PoseLandmark.RIGHT_HIP,          # 右臀
        mpPose.PoseLandmark.LEFT_KNEE,          # 左膝
        mpPose.PoseLandmark.RIGHT_KNEE,         # 右膝
        mpPose.PoseLandmark.LEFT_ANKLE,         # 左脚踝
        mpPose.PoseLandmark.RIGHT_ANKLE,        # 右脚踝
    ]

    # 取出 pose 坐标
    if output.pose_landmarks is not None : 
        for lm in lms_list : 
            landmark = output.pose_landmarks.landmark[lm]
            output_list.append(landmark.x)
            output_list.append(landmark.y)
            output_list.append(landmark.z)
        return output_list
    else :
        return False


# 检测图片动作方法
def detect_coordinates_img(imgs):
    # 输出结果列表
    output_tensor = []
    for img in imgs : 
        img = transforms.ToPILImage()(img)  # 将 tensor 转换为 PIL 图片
        img = np.array(img)                 # 将 PIL 图片转换为 numpy 数组
        mpPose = mp.solutions.pose          # 创建 mpPose 类
        # 创建 Pose 对象
        pose = mpPose.Pose(                 
            static_image_mode=True,         # 图片模式
            min_detection_confidence=0.5    # 置信度
        )
        output = pose.process(img)          # 处理图片
        coords = extract_coordinates(output, mpPose)    # 提取坐标
        if coords : 
            output_tensor.append(coords)    # 将坐标添加到输出结果列表

    return torch.tensor(output_tensor)      # 返回输出结果

# 
def move2keyboard(prev_coords, coords, move_detected):
    global keybinds     # 全局变量
    global keyboard     # 全局变量

    # 如果检测到动作
    if move_detected != 'No_action':
        # 按下键盘按键
        keyboard.press(keybinds[move_detected])
    else : 
        # 如果没有检测到动作
        threshold = 0.007           
        body_center = mean(coords)                           # 计算坐标平均值
        prev_body_center = mean(prev_coords)                 # 计算上一帧坐标平均值
        if (body_center - prev_body_center)>threshold :      # 如果坐标平均值大于阈值
            keyboard.press('d')                              # 按下 d 键
        elif (body_center - prev_body_center)<-(threshold) : # 如果坐标平均值小于阈值
            keyboard.press('a')                              # 按下 a 键