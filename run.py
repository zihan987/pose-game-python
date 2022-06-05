
# 游戏控制器
def game_controller():
    # 初始化游戏
    import torch, cv2, time, os
    from model import PoseClassification
    from helper import extract_coordinates, move2keyboard
    import mediapipe as mp
    time.sleep(3)   #   等待3秒

    # 设置模型路径
    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'weights/trained_2.pt')
    model = PoseClassification(57, 5)                                   #   创建一个姿态检测器模型
    model.load_state_dict(torch.load(model_path, map_location='cpu'))   #   加载模型    调用CPU
    model = model.eval()                                                #   设置模型为评估模式

    # 姿势字典{'No_action':无行动, 'hook':挂钩, 'kick':踢球, 'special':特殊动作, 'crouch':蹲下}
    move2id = {'No_action': 0, 'hook': 1, 'kick': 2, 'special': 3, 'crouch': 4}
    id2move = {x: y for y, x in move2id.items()}                        #   反向字典

    scale = 0.65                                                        #   缩放比例
    font = cv2.FONT_HERSHEY_SIMPLEX                                     #   字体
    fontScale = 0.75                                                    #   字体大小
    fontColor = (255, 255, 255)                                         #   字体颜色
    lineType = 4                                                        #   线条类型

    Capture = cv2.VideoCapture(0)                       #   创建一个视频捕获对象
    h = int(Capture.get(4))                             #   获取视频高度
    w = int(Capture.get(3))                             #   获取视频宽度
    mpPose = mp.solutions.pose                      #   创建一个姿态检测器
    pose = mpPose.Pose(                             #   创建一个姿态检测器
        static_image_mode=False,                    #   开启动态图像模式
        min_detection_confidence=0.5,               #   设置检测置信度
        min_tracking_confidence=0.5                 #   设置跟踪置信度
    )
    MP_draw = mp.solutions.drawing_utils            #   创建一个绘图工具 

    prev_movement_coords = []                       #   上一帧的姿势坐标
    ptime = 0                                       #   上一帧的时间         
    The_current_time = 0                                       #   当前帧的时间

    while True:                                     #   循环
        _, frame = Capture.read()                       #   读取一帧视频
        # frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
        frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB) #   反转图像
        try:
            output = pose.process(frame)            #   姿态检测
            MP_draw.draw_landmarks(frame, output.pose_landmarks, mpPose.POSE_CONNECTIONS)   #   绘制姿态关键点
            coords = extract_coordinates(output, mpPose)                                    #   提取姿势坐标
            if coords:                              #   如果有姿势坐标
                coords = torch.tensor(coords).unsqueeze(0)      #   将坐标转换为张量
                yhat = model(coords).view(-1)                   #   预测姿势
                yhat_ = torch.argmax(yhat)                      #   预测姿势
                conf = round(yhat[yhat_].item(), 5)             #   预测置信度
                pred = id2move[yhat_.item()]                    #   预测姿势
                if pred == 'kick' and conf < 3:                 #   如果预测为踢腿
                    pred = 'No_action'                            #   将预测姿势设置为无行动
                elif pred == 'special' and conf < 2:            #   如果预测为特殊动作
                    pred = 'No_action'                            #   将预测姿势设置为无行动
                cv2.rectangle(frame, (0, h), (w - 1000, h - 110), (0, 0, 0), -1, 1)  #   绘制矩形
                cv2.putText(frame, f'Move : {pred}', (0, h - 80), font, fontScale, fontColor, lineType=lineType,
                            thickness=2)                        #   绘制文字
                cv2.putText(frame, f'Confidence : {conf}', (0, h - 50), font, fontScale, fontColor, lineType=lineType,
                            thickness=2)                        #   绘制文字

                if len(prev_movement_coords) != 0:              #   如果有上一帧的姿势坐标
                    movement_coords = [coords[0][3].item(), coords[0][6].item()]    #   获取姿势坐标
                    move2keyboard(prev_movement_coords, movement_coords, pred)      #   将姿势坐标传递给键盘
                    prev_movement_coords = movement_coords                          #   更新上一帧的姿势坐标
                else:                                                               #   如果没有上一帧的姿势坐标
                    prev_movement_coords = [coords[0][3].item(), coords[0][6].item()]   #   更新上一帧的姿势坐标

        except cv2.error:                                                           #   如果检测失败
            pass                                                                    #   继续循环

        The_current_time = time.time()                                     #   获取当前时间
        fps = round(1 / (The_current_time - ptime), 2)                     #   计算帧率
        ptime = The_current_time                                           #   更新时间
        cv2.putText(frame, f'FPS : {str(fps)}', (0, h - 20), font, fontScale, fontColor, lineType=lineType, thickness=2)    # 绘制文字

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)          #   反转图像
        new_dims = (int(w * scale), int(h * scale))             #   设置缩放尺寸
        frame = cv2.resize(frame, new_dims)                     #   缩放图像
        cv2.imshow('Output', frame)                             #   显示图像

        if cv2.waitKey(1) & 0xFF == ord('q'):                   #   如果按下q键
            break                                               #   退出循环
