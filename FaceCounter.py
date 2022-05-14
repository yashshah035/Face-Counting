import numpy as np
import time
import cv2
import mediapipe as mp

face_detection = mp.solutions.face_detection.FaceDetection(0.4)

def detector(frame):

    count = 0
    height, width, channel = frame.shape

    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_detection.process(imgRGB)
    
    try:
        for count, detection in enumerate(result.detections):

            

            score = detection.score
            box = detection.location_data.relative_bounding_box


            x, y, w, h = int(box.xmin*width), int(box.ymin * height), int(box.width*width), int(box.height*height)
            score = str(round(score[0]*100, 2))

            print(x, y, w, h)

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            cv2.rectangle(frame, (x, y), (x+w, y-25), (0, 0, 255), -1)

            cv2.putText(frame, score,  (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        count += 1
        print("Found ",count, "Faces!")

    except:
        pass

    return count, frame

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1980)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)

while True:
    
    _, frame = cap.read()
    count, output = detector(frame)
    
    out_bil = cv2.bilateralFilter(output, 5, 6, 6)

    start = 0
    end = time.time()
    totalTime = end - start 

    fps = 1 / totalTime
    print("FPS: ", fps)

    sharp1 = cv2.addWeighted(output, 1.5,out_bil, -0.5, 0)
  

    cv2.putText(sharp1, "Number of Faces: "+str(count),(10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2 )
    cv2.imshow("frame", sharp1)
    if cv2.waitKey(15) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()