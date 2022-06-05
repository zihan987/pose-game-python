# 导入相关的库
import cv2, time, torch
import mediapipe as mp
# 从helper对象导入坐标提取（extract_coordinates）
from helper import extract_coordinates

# 创建一动作检测器相机
# 创建一个摄像头
My_Current_move = 'crouch'             #   初始化当前动作
Capture = cv2.VideoCapture(f'/users/zihan/your_path/{your_path}.mp4')  # 创建一个摄像头：摄像头的路径
#Capture = cv2.VideoCapture(0)          #   创建一个摄像头
start_time = time.time()            #   初始化开始时间

# OpenCV文本参数

# 创建一个矩形框
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1

# 矩形框的颜色：红色
fontColor = (0,0,0)
# 矩形框的线条宽度
lineType = 4
# 矩形框的线条类型
# 设置时间
setup_time = 0
# 
s = True

# Mediapipe姿势估计检测和绘制工具
# 创建一个姿势估计检测器
mpPose = mp.solutions.pose
# 设置对象pose的属性  
pose = mpPose.Pose(
    # 图片基础模型
    static_image_mode=False,
    # 最小分类置信度
    min_detection_confidence=0.5,
    # 最小人脸检测置信度
    min_tracking_confidence=0.5
)
 
# mp.solutions.drawing_utils用于绘制
MP_draw = mp.solutions.drawing_utils

# 动作标签字典
labelmap = {'No_action':0, 'hook':1, 'kick':2, 'special':3, 'crouch':4}

# 用于存储为移动收集的数据集的张量
all_coords = torch.tensor([]) 

try : 
    _ = True
    while _ : 
        # 使用OpenCV读取框架
        _, frame = Capture.read()
        # 将图片转换为RGB格式
        frame = cv2.cvtColor(cv2.flip(frame,1), cv2.COLOR_BGR2RGB)
        # 提取姿势和坐标
        output = pose.process(frame)
        coords = extract_coordinates(output, mpPose)

        # 检查是否已过设置时间
        time_left = time.time() - start_time
        if time_left > setup_time : 
            # 检测是否已经保存了数据集
            if s : 
                # 检查当前帧中是否有要添加到数据集的姿势
                if coords : 
                    coords = torch.tensor(coords, dtype=torch.float32).unsqueeze(0)
                    if all_coords.shape[0] == 0 : 
                        all_coords = coords 
                    else : 
                        all_coords = torch.cat([all_coords, coords], dim=0)
                    # 标注文字 recording started
                cv2.putText(frame, 'recording started', (100,100), font, fontScale, fontColor, lineType=lineType, thickness=3)
        else : 
            # 否则，如果设置时间尚未过去，则显示剩余时间
            if s : 
                cv2.putText(frame, str(round(setup_time - time_left,2)), (100,100), font, fontScale, fontColor, lineType=lineType, thickness=3)

        # 绘制估计的地标和显示框
        MP_draw.draw_landmarks(frame, output.pose_landmarks, mpPose.POSE_CONNECTIONS)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        cv2.imshow('output', frame)

        # 按下Q键退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
# 如果捕获到异常，则退出
except cv2.error : 
    pass

# 使用坐标保存张量，如果没有坐标，则保存空张量
if all_coords.shape[0] > 0 : 
    # 保存数据集：数据集的路径
    torch.save(all_coords, f'/your_path/move_dataset/{My_Current_move}.pt')
# 打印保存的数据集的大小
print(all_coords.shape)

