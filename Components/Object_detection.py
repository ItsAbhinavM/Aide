import cv2
import time
import numpy as np
from ultralytics import YOLO
from collections import defaultdict

def object_detection(duration=3):
    model= YOLO("yolo11n.pt")
    # model= YOLO("yolo11x-seg")
    videocap=cv2.VideoCapture(0)
    
    if not videocap.isOpened():
        return {"error": "Could not open webcam"}
    
    track_history = defaultdict(list)
    start_time = time.time()
    frame_count = 0
    
    print(f"Starting object detection for {duration} seconds...")
    
    while True:
        success, frame = videocap.read()        
        if not success:
            break
            
        frame_count += 1
        current_time = time.time()
        results = model.track(frame, persist=True)
        
        if results[0].boxes is not None:
            boxes = results[0].boxes
            annotated_frame = results[0].plot()
            class_ids = boxes.cls.int().cpu().tolist()
            confidences = boxes.conf.cpu().tolist()
            track_ids = boxes.id.int().cpu().tolist() if boxes.id is not None else []
            
            for track_id, cls_id, conf in zip(track_ids, class_ids, confidences):
                label = model.names[int(cls_id)]
                if not track_history[track_id] or track_history[track_id][-1][0] != label:
                    track_history[track_id].append((label, round(float(conf), 2)))
            
            cv2.imshow("Object Detection", annotated_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Detection stopped by user")
                break
        
        if current_time - start_time >= duration:
            print(f"Detection completed after {duration} seconds")
            break
    videocap.release()
    cv2.destroyAllWindows()
    return track_history
if __name__ == "__main__":
    result = object_detection(3)
    print("Detection result:", result)