import mediapipe as mp 
import cv2 
#  
def detect_img(img_path):
    img = cv2.imread(img_path)          # 读取图片
    mpPose = mp.solutions.pose          # 创建 mpPose 类
    pose = mpPose.Pose(                 # 创建 Pose 对象
        static_image_mode=True,         # 图片模式
        min_detection_confidence=0.5    # 最小检测置信度
    )
    MP_draw = mp.solutions.drawing_utils        # 创建 MP_draw 类
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 将图片转换为RGB格式
    output = pose.process(img)                  # 输出检测姿势

    # 绘制姿势
    MP_draw.draw_landmarks(img, output.pose_landmarks, mpPose.POSE_CONNECTIONS)
    
    # 将图片转换为BGR格式
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imshow('Output', img)               # 显示图片
    cv2.waitKey(0)                          # 等待按键

#  使用OpenCV读取视频框架
def detect_video():
    mpPose = mp.solutions.pose              # 创建 mpPose 类
    pose = mpPose.Pose(                     # 创建 Pose 对象
        static_image_mode=False,            # 视频模式
        min_detection_confidence=0.5,       # 最小检测置信度
        min_tracking_confidence=0.5         # 最小追踪置信度
    )
    MP_draw = mp.solutions.drawing_utils    # 创建 MP_draw 类
    
    cap = cv2.VideoCapture(0)               # 创建 VideoCapture 对象
    while True :                            # 循环
        _, img = cap.read()                 # 读取视频帧
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 将图片转换为RGB格式
        output = pose.process(img)          # 输出检测姿势
        # 绘制姿势
        MP_draw.draw_landmarks(img, output.pose_landmarks, mpPose.POSE_CONNECTIONS)
        # 将图片转换为BGR格式
        img = cv2.cvtColor(cv2.flip(img,1), cv2.COLOR_RGB2BGR)
        cv2.imshow('Output', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # 等待按键
            break
# 函数调用
detect_video()