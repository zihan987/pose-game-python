import cv2
import mediapipe as mp
import os
import time
import torch

from helper import extract_coordinates
from model import PoseClassification

# 创建一动作检测器相机
My_model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'weights/trained_2.pt')
model = PoseClassification(57,5)    #   创建一个摄像头
model.load_state_dict(torch.load(My_model_path, map_location='cpu'))   #   加载模型
model = model.eval()                #   设置模型为验证模式

Move_two_ID = {'No_action':0, 'hook':1, 'kick':2, 'special':3, 'crouch':4}#   动作标签字典
id2move = {x:y for y,x in Move_two_ID.items()}                          #   反向字典

scale = 1                               #   缩放比例 
font = cv2.FONT_HERSHEY_SIMPLEX         #   字体
fontScale = 0.75                        #   字体大小
fontColor = (255,255,255)               #   字体颜色
lineType = 4                            #   线条类型

cap = cv2.VideoCapture(0)               #   创建一个摄像头
h = int(cap.get(4))                     #   获取摄像头的高
w = int(cap.get(3))                     #   获取摄像头的宽
mpPose = mp.solutions.pose              #   创建一个Pose类
pose = mpPose.Pose(                     #   创建一个Pose类
    static_image_mode=False,            #   动态图像模式
    min_detection_confidence=0.5,       #   检测置信度
    min_tracking_confidence=0.5         #   跟踪置信度
)
MP_draw = mp.solutions.drawing_utils    #   创建一个画图类

prev_movement_coords = []               #   上一帧的动作坐标
ptime = 0                               #   上一帧的时间
The_current_time = 0                               #   当前帧的时间

while True :                            #   循环
    _, frame = cap.read()               #   读取一帧
    frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB) #   转换颜色空间
    try :                               #   尝试
        output = pose.process(frame)    #   获取一帧的动作坐标
        MP_draw.draw_landmarks(frame, output.pose_landmarks, mpPose.POSE_CONNECTIONS)   #   画出动作坐标
        coords = extract_coordinates(output, mpPose)                                    #   提取动作坐标
        if coords :                     #   如果有动作坐标
            coords = torch.tensor(coords).unsqueeze(0)                                  #   将坐标转换为张量
            yhat = model(coords).view(-1)                                               #   预测动作
            yhat_ = torch.argmax(yhat)                                                  #   预测动作
            conf = round(yhat[yhat_].item(),5)                                          #   预测动作的置信度
            pred = id2move[yhat_.item()]                                                #   预测动作

            if pred == 'kick' and conf < 3 :                                            #   如果预测动作为踢球
                pred = 'No_action'                                                        #   将预测动作设置为无动作
            elif pred == 'special' and conf < 2 :                                       #   如果预测动作为特殊动作
                pred = 'No_action'                                                        #   将预测动作设置为无动作

            cv2.rectangle(frame, (0,h), (w-1000,h-110), (0,0,0), -1, 1)                 #   画出框
            cv2.putText(frame, f'Move : {pred}', (0,h-80), font, fontScale, fontColor, lineType=lineType, thickness=2)  #   显示动作
            cv2.putText(frame, f'Confidence : {conf}', (0,h-50), font, fontScale, fontColor, lineType=lineType, thickness=2)    #   显示置信度

    except AttributeError :             #   如果没有动作坐标    
        pass                            #   继续循环

    The_current_time = time.time()                 #   获取当前时间
    fps = round(1/(The_current_time-ptime),2)      #   计算FPS
    ptime = The_current_time                       #   记录上一帧时间
    cv2.putText(frame, f'FPS : {str(fps)}', (0, h-20), font, fontScale, fontColor, lineType=lineType, thickness=2)  #   显示FPS

    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  #   转换颜色空间
    new_dims = (int(w * scale), int(h * scale))     #   计算缩放后的尺寸
    frame = cv2.resize(frame, new_dims)             #   缩放图像
    cv2.imshow('Output', frame)                     #   显示图像

    if cv2.waitKey(1) & 0xFF == ord('q'):           #   按q退出
        break






