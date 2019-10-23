import numpy as np
import cv2
import json

cap = cv2.VideoCapture(0)

cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
font = cv2.FONT_HERSHEY_SIMPLEX

thickness = 2
color = (255, 0 , 0 )
FACE_SHAPE = 0.45
org = (10, 40)
fontScale = 1


sensorData =  {
                "coachId": 1,
                "capacity": 4,
                "measurement" : 0
              }


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # do what you want with frame
    #  and then save to file
    imageGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    
    faceRect = cascade.detectMultiScale(imageGray, scaleFactor=1.1, minNeighbors=1, minSize=(1,1))
      
    
    filteredFaceRects = []
    
    for faceR in faceRect:
        faceSize = faceR[2]*faceR[3]
        if FACE_SHAPE > min(faceR[2], faceR[3])/max(faceR[2], faceR[3]):
            break
        filteredFaceRects.append(faceR)
    
    for faceR in filteredFaceRects:
        point1 = ( faceR[0] , faceR[1])
        point2 = ( faceR[0] + faceR[2] , faceR[1] + faceR[3] )
    
    cv2.rectangle(imageGray, point1, point2, color, thickness)
    image = cv2.putText(imageGray,  str(len( filteredFaceRects) ), org, font, fontScale, color, thickness, cv2.LINE_AA)
    
    sensorData["measurement"] = len(filteredFaceRects)
    
    print(json.dumps( sensorData, sort_keys=True, indent=4 ) )

    cv2.imshow('Frame',imageGray)
    
    
#    cv2.imwrite('image.png', frame)
    if cv2.waitKey(30) & 0xFF == ord('q'): # you can increase delay to 2 seconds here
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
