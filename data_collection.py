import cv2, time, torch
import mediapipe as mp
from helper import extract_coordinates

current_move = 'crouch'
cap = cv2.VideoCapture(f'/users/gursi/desktop/{current_move}.mp4')
#cap = cv2.VideoCapture(0)
start_time = time.time()

# OpenCV text paramters
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
fontColor = (0,0,0)
lineType = 4
setup_time = 0
s = True

# Mediapipe pose estimation detection and drawing tools
mpPose = mp.solutions.pose
pose = mpPose.Pose(
    static_image_mode=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_draw = mp.solutions.drawing_utils
  
labelmap = {'no_move':0, 'hook':1, 'kick':2, 'special':3, 'crouch':4}

# Tensor to store dataset gathered for moves
all_coords = torch.tensor([]) 

try : 
    _ = True
    while _ : 
        # Read frame in with OpenCV
        _, frame = cap.read()
        frame = cv2.cvtColor(cv2.flip(frame,1), cv2.COLOR_BGR2RGB)
        # Extract poses and coordinates
        output = pose.process(frame)
        coords = extract_coordinates(output, mpPose)

        # Check if setup time has elapsed
        time_left = time.time() - start_time
        if time_left > setup_time : 
            # Check is saving is set to True 
            if s : 
                # Check if there is a pose in current frame to add to dataset
                if coords : 
                    coords = torch.tensor(coords, dtype=torch.float32).unsqueeze(0)
                    if all_coords.shape[0] == 0 : 
                        all_coords = coords 
                    else : 
                        all_coords = torch.cat([all_coords, coords], dim=0)

                cv2.putText(frame, 'recording started', (100,100), font, fontScale, fontColor, lineType=lineType, thickness=3)
        else : 
            # Else if setup time not yet elapsed display time left
            if s : 
                cv2.putText(frame, str(round(setup_time - time_left,2)), (100,100), font, fontScale, fontColor, lineType=lineType, thickness=3)

        # Draw estimated landmarks and display frame
        mp_draw.draw_landmarks(frame, output.pose_landmarks, mpPose.POSE_CONNECTIONS)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        cv2.imshow('output', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except cv2.error : 
    pass

# Save tensor with coordinates
if all_coords.shape[0] > 0 : 
    torch.save(all_coords, f'/users/gursi/desktop/Pose2Play/move_dataset/{current_move}.pt')
print(all_coords.shape)

