import numpy as np
import cv2
import json
import requests

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1096)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)

cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
font = cv2.FONT_HERSHEY_SIMPLEX

thickness = 2
color = (0, 0 , 0 )
FACE_SHAPE = 0.45
org = (10, 40)
fontScale = 1

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
                "PersonCount" : "0"
              }
              
              
requestCounter = 0


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
    
    sensorData["PersonCount"] = str(len(filteredFaceRects))
    

    
    requestCounter = requestCounter + 1
    
    if requestCounter > 50:
        requestCounter = 0
        payload = json.dumps( sensorData, sort_keys=True ) #, indent=4 )
        print( payload )
        answer = requests.post(url = URL, params = sensorData, data = payload, headers = headers )


        print( answer.text )
        
        

    cv2.imshow('Frame',imageGray)
    
    
#    cv2.imwrite('image.png', frame)
    if cv2.waitKey(30) & 0xFF == ord('q'): # you can increase delay to 2 seconds here
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
