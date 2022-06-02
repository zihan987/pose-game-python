import torch
import mediapipe as mp 
import numpy as np
from torchvision import transforms
from statistics import mean
from pynput.keyboard import Controller, Key

keyboard = Controller()
keybinds = {'hook':'j', 'kick':'k', 'special':'o', 'crouch':'s'}

def extract_coordinates(output, mpPose):
    output_list = []
    lms_list = [
        mpPose.PoseLandmark.NOSE, 
        mpPose.PoseLandmark.RIGHT_SHOULDER,
        mpPose.PoseLandmark.LEFT_SHOULDER,
        mpPose.PoseLandmark.LEFT_ELBOW,
        mpPose.PoseLandmark.RIGHT_ELBOW,
        mpPose.PoseLandmark.LEFT_WRIST,
        mpPose.PoseLandmark.RIGHT_WRIST,
        mpPose.PoseLandmark.LEFT_PINKY,
        mpPose.PoseLandmark.RIGHT_PINKY,
        mpPose.PoseLandmark.LEFT_INDEX,
        mpPose.PoseLandmark.RIGHT_INDEX,
        mpPose.PoseLandmark.LEFT_THUMB,
        mpPose.PoseLandmark.RIGHT_THUMB,
        mpPose.PoseLandmark.LEFT_HIP,
        mpPose.PoseLandmark.RIGHT_HIP,
        mpPose.PoseLandmark.LEFT_KNEE,
        mpPose.PoseLandmark.RIGHT_KNEE,
        mpPose.PoseLandmark.LEFT_ANKLE,
        mpPose.PoseLandmark.RIGHT_ANKLE,
    ]

    if output.pose_landmarks is not None : 
        for lm in lms_list : 
            landmark = output.pose_landmarks.landmark[lm]
            output_list.append(landmark.x)
            output_list.append(landmark.y)
            output_list.append(landmark.z)
        return output_list
    else :
        return False



def detect_coordinates_img(imgs):
    output_tensor = []
    for img in imgs : 
        img = transforms.ToPILImage()(img)
        img = np.array(img)
        mpPose = mp.solutions.pose
        pose = mpPose.Pose(
            static_image_mode=True,
            min_detection_confidence=0.5
        )
        output = pose.process(img)
        coords = extract_coordinates(output, mpPose)
        if coords : 
            output_tensor.append(coords)

    return torch.tensor(output_tensor)


def move2keyboard(prev_coords, coords, move_detected):
    global keybinds
    global keyboard

    if move_detected != 'no_move':
        keyboard.press(keybinds[move_detected])
    else : 
        threshold = 0.007
        body_center = mean(coords)
        prev_body_center = mean(prev_coords)
        if (body_center - prev_body_center)>threshold : 
            keyboard.press('d')
        elif (body_center - prev_body_center)<-(threshold) : 
            keyboard.press('a')