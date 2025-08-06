import cv2
import numpy as np
from ultralytics import YOLO
from collections import defaultdict

model= YOLO("yolo11n.pt")
# model= YOLO("yolo11x-seg")
videocap=cv2.VideoCapture(0)
track_history=defaultdict(lambda: [])

while videocap.isOpened():
    success,frame=videocap.read()
    if success:
        results=model.track(frame,persist=True)
        boxes=results[0].boxes.xywh.cpu()
        track_ids=results[0].boxes.id.int().cpu().tolist()
        annoted_frame= results[0].plot()
        for box,track_id in zip(boxes,track_ids):
            x,y,w,h=box
            track=track_history[track_id]
            track.append((float(x),float(y)))
            if len(track)>30:
                track.pop(0)
            points=np.hstack(track).astype(np.int32).reshape((-1,1,2))
            cv2.polylines(annoted_frame,[points], isClosed=False, color=(230, 230, 230), thickness=10)
        cv2.imshow("Image Recognition Tracking", annoted_frame)
        if cv2.waitKey(1) & 0xFF==ord("q"):
            break
    else:
        break
videocap.release()
cv2.destroyAllWindows()