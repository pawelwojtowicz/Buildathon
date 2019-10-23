import numpy as np
import cv2
import json
import requests

cap = cv2.VideoCapture(0)

imageWidth = 1096
imageHeight = 800

seats = 4

cap.set(cv2.CAP_PROP_FRAME_WIDTH, imageWidth)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, imageHeight)

cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
font = cv2.FONT_HERSHEY_SIMPLEX

thickness = 2
color = (0, 0 , 0 )
FACE_SHAPE = 0.45
#FACE_SHAPE = 0.5
org = (10, 40)
fontScale = 1

imageWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
seatWidth = int (imageWidth / seats )

headers = {
    'Content-Type': "application/json",
    'User-Agent': "PostmanRuntime/7.18.0",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Postman-Token': "3fea7bd8-7d6d-40ff-90e9-f472827a3996,cb4c6e7f-6b87-46e2-b073-303cfd5bc889",
    'Host': "build-a-thon-rest-api.azurewebsites.net",
    'Accept-Encoding': "gzip, deflate",
    'Content-Length': "61",
    'Cookie': "ARRAffinity=e26452b9ab4162bf874a7a557d2b3213793b954884fe2afaba6f881f8f5285d5",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }




#URL = "http://127.0.0.1:8080"
URL = "http://build-a-thon-rest-api.azurewebsites.net/api/Vehicles"

sensorData =  {
                "vehicleId": "1",
                "coachNumber": "1",
                "PersonCount" : "0",
                "seatOccupancy": []
              }
              
              
requestCounter = 0

average  = 0;
sum = 0;


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # do what you want with frame
    #  and then save to file
    imageGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    
    faceRect = cascade.detectMultiScale(imageGray, scaleFactor=1.1, minNeighbors=1, minSize=(100,100))
    
    seatOccupancy = []
    for a in range(seats):
        seatOccupancy.append(0)
            
    filteredFaceRects = []
    
    for faceR in faceRect:
        faceSize = faceR[2]*faceR[3]
        if FACE_SHAPE > min(faceR[2], faceR[3])/max(faceR[2], faceR[3]):
            break
        filteredFaceRects.append(faceR)
    
    for faceR in filteredFaceRects:
        point1 = ( faceR[0] , faceR[1])
        point2 = ( faceR[0] + faceR[2] , faceR[1] + faceR[3] )
        cv2.rectangle(frame, point1, point2, color, thickness)
        seatIndex = int(faceR[0]/seatWidth)
        seatOccupancy[seatIndex] = int(1)
        
        
   
    image = cv2.putText(frame,  str(len( filteredFaceRects) ), org, font, fontScale, color, thickness, cv2.LINE_AA)
    
    
    for i in range(seats):
        
        point1 = (int(((i+1)*imageWidth)/seats), 0 )
        point2 = int(((i+1)*imageWidth)/seats) , imageHeight
        cv2.line( frame, point1, point2, color, thickness)
    
    sensorData["PersonCount"] = str(len(filteredFaceRects))
    sensorData["seatOccupancy"] = seatOccupancy
    
    
    
    
    requestCounter = requestCounter + 1
    
    if requestCounter > 50:
        requestCounter = 0
        payload = json.dumps( sensorData, sort_keys=True ) #, indent=4 )
        print( payload )
        answer = requests.post(url = URL, params = sensorData, data = payload, headers = headers )

        print( answer.text )
        
        

    cv2.imshow('Frame',frame)
    
    
#    cv2.imwrite('image.png', frame)
    if cv2.waitKey(30) & 0xFF == ord('q'): # you can increase delay to 2 seconds here
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()