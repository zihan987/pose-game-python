import cv2
import mediapipe as mp
import os
import time
import torch

from helper import extract_coordinates
from model import PoseClassification

model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'weights/trained_2.pt')
model = PoseClassification(57,5)
model.load_state_dict(torch.load(model_path, map_location='cpu'))
model = model.eval()

move2id = {'no_move':0, 'hook':1, 'kick':2, 'special':3, 'crouch':4}
id2move = {x:y for y,x in move2id.items()}

scale = 1
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 0.75
fontColor = (255,255,255)
lineType = 4

cap = cv2.VideoCapture(0)
h = int(cap.get(4))
w = int(cap.get(3))
mpPose = mp.solutions.pose
pose = mpPose.Pose(
    static_image_mode=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_draw = mp.solutions.drawing_utils

prev_movement_coords = []
ptime = 0
ctime = 0

while True :
    _, frame = cap.read()
    frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
    try :
        output = pose.process(frame)
        mp_draw.draw_landmarks(frame, output.pose_landmarks, mpPose.POSE_CONNECTIONS)
        coords = extract_coordinates(output, mpPose)
        if coords :
            coords = torch.tensor(coords).unsqueeze(0)
            yhat = model(coords).view(-1)
            yhat_ = torch.argmax(yhat)
            conf = round(yhat[yhat_].item(),5)
            pred = id2move[yhat_.item()]

            if pred == 'kick' and conf < 3 :
                pred = 'no_move'
            elif pred == 'special' and conf < 2 :
                pred = 'no_move'

            cv2.rectangle(frame, (0,h), (w-1000,h-110), (0,0,0), -1, 1)
            cv2.putText(frame, f'Move : {pred}', (0,h-80), font, fontScale, fontColor, lineType=lineType, thickness=2)
            cv2.putText(frame, f'Confidence : {conf}', (0,h-50), font, fontScale, fontColor, lineType=lineType, thickness=2)

    except AttributeError :
        pass

    ctime = time.time()
    fps = round(1/(ctime-ptime),2)
    ptime = ctime
    cv2.putText(frame, f'FPS : {str(fps)}', (0, h-20), font, fontScale, fontColor, lineType=lineType, thickness=2)

    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    new_dims = (int(w * scale), int(h * scale))
    frame = cv2.resize(frame, new_dims)
    cv2.imshow('Output', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break






