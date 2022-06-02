import mediapipe as mp 
import cv2 

def detect_img(img_path):
    img = cv2.imread(img_path)
    mpPose = mp.solutions.pose
    pose = mpPose.Pose(
        static_image_mode=True,
        min_detection_confidence=0.5
    )
    mp_draw = mp.solutions.drawing_utils
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    output = pose.process(img)

    mp_draw.draw_landmarks(img, output.pose_landmarks, mpPose.POSE_CONNECTIONS)
    
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imshow('Output', img)
    cv2.waitKey(0)


def detect_video():
    mpPose = mp.solutions.pose
    pose = mpPose.Pose(
        static_image_mode=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    mp_draw = mp.solutions.drawing_utils
    
    cap = cv2.VideoCapture(0)
    while True : 
        _, img = cap.read()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        output = pose.process(img)

        mp_draw.draw_landmarks(img, output.pose_landmarks, mpPose.POSE_CONNECTIONS)
        
        img = cv2.cvtColor(cv2.flip(img,1), cv2.COLOR_RGB2BGR)
        cv2.imshow('Output', img)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

detect_video()