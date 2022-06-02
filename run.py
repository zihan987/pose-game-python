

def game_controller():
    import torch, cv2, time, os
    from model import PoseClassification
    from helper import extract_coordinates, move2keyboard
    import mediapipe as mp
    time.sleep(3)

    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'weights/trained_2.pt')
    model = PoseClassification(57, 5)
    model.load_state_dict(torch.load(model_path, map_location='cpu'))
    model = model.eval()

    move2id = {'no_move': 0, 'hook': 1, 'kick': 2, 'special': 3, 'crouch': 4}
    id2move = {x: y for y, x in move2id.items()}

    scale = 0.65
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.75
    fontColor = (255, 255, 255)
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

    while True:
        _, frame = cap.read()
        # frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
        frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
        try:
            output = pose.process(frame)
            mp_draw.draw_landmarks(frame, output.pose_landmarks, mpPose.POSE_CONNECTIONS)
            coords = extract_coordinates(output, mpPose)
            if coords:
                coords = torch.tensor(coords).unsqueeze(0)
                yhat = model(coords).view(-1)
                yhat_ = torch.argmax(yhat)
                conf = round(yhat[yhat_].item(), 5)
                pred = id2move[yhat_.item()]
                if pred == 'kick' and conf < 3:
                    pred = 'no_move'
                elif pred == 'special' and conf < 2:
                    pred = 'no_move'
                cv2.rectangle(frame, (0, h), (w - 1000, h - 110), (0, 0, 0), -1, 1)
                cv2.putText(frame, f'Move : {pred}', (0, h - 80), font, fontScale, fontColor, lineType=lineType,
                            thickness=2)
                cv2.putText(frame, f'Confidence : {conf}', (0, h - 50), font, fontScale, fontColor, lineType=lineType,
                            thickness=2)

                if len(prev_movement_coords) != 0:
                    movement_coords = [coords[0][3].item(), coords[0][6].item()]
                    move2keyboard(prev_movement_coords, movement_coords, pred)
                    prev_movement_coords = movement_coords
                else:
                    prev_movement_coords = [coords[0][3].item(), coords[0][6].item()]

        except cv2.error:
            pass

        ctime = time.time()
        fps = round(1 / (ctime - ptime), 2)
        ptime = ctime
        cv2.putText(frame, f'FPS : {str(fps)}', (0, h - 20), font, fontScale, fontColor, lineType=lineType, thickness=2)

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        new_dims = (int(w * scale), int(h * scale))
        frame = cv2.resize(frame, new_dims)
        cv2.imshow('Output', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
