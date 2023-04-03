import base64
from PIL import Image
from io import BytesIO
from datetime import datetime,date
import easyocr
import re
from deepface import DeepFace
import zxing 
from  flask import *
import cv2
from cvzone.HandTrackingModule import HandDetector
import requests
import numpy as np
def fin(img):
 #img = cv2.imencode('.png', img)[1].tobytes()

 detector = HandDetector(maxHands=1, detectionCon=0.8)
 #video = cv2.VideoCapture(0)
  
 while True:
   # _, img = video.read()
    #img = cv2.flip(img, 1)
    #img=cv2.imread("hand.png")
    
    numpy_parsing = np.fromstring(base64.b64decode(img), np.uint8)
    img = cv2.imdecode(numpy_parsing, cv2.IMREAD_COLOR)
    print(img)
    cv2.imwrite("hand.png", img)

    a = cv2.imread("hand.png")
    hand = detector.findHands(img, draw=False)
    fing ="zero finger detected"
    if hand:
        lmlist = hand[0]
        if lmlist:
            fingerup = detector.fingersUp(lmlist)
            if fingerup == [0, 1, 0, 0, 0]:
                fing = "One fingers are detected"
            if fingerup == [0, 1, 1, 0, 0]:
                fing = "Two fingers are detected"
            if fingerup == [0, 1, 1, 1, 0]:
                fing = "Three fingers are detected"
            if fingerup == [0, 1, 1, 1, 1]:
                fing = "Four fingers are detected"
            if fingerup == [1, 1, 1, 1, 1]:
                fing = "Five fingers are detected"
    #fing = cv2.resize(fing, (220, 280))
    #img[50:330, 20:240] = fing
    #cv2.imshow("Video", img)
   
    #if cv2.waitKey(1) & 0xFF == ord('q'):
    break

 return fing
          
#video.release()
#cv2.destroyAllWindows()


def successed(img1,img2,img3): 
          my_string = base64.b64decode(img1)
          imges=BytesIO(my_string)
          img=Image.open(imges)
          img.save("cnic_front.png")

          my_string = base64.b64decode(img2)
          imges=BytesIO(my_string)
          img=Image.open(imges)
          img.save("cnic_back.png")
           
          my_string = base64.b64decode(img3)
          imges=BytesIO(my_string)
          img=Image.open(imges)
          img.save("dp.png") 

          liveness="verified"
          resultoo=False
          reader = zxing.BarCodeReader()
          barcode = reader.decode("cnic_back.png")
          barcode=barcode.raw

      
          cnic = re.findall("\d{13}", barcode)[3]
      

          try:
              reader = easyocr.Reader(['ur','en']) 
              resul = reader.readtext("cnic_back.png",  detail = 0, paragraph=True)
              resul="".join(resul)
              DATE_OF_ISSUE= re.findall("\d{2}[/]\d{2}[/]\d{4}", resul)[1]
          except:
                DATE_OF_ISSUE = "not_found"
          try:      
             DATE_OF_EXPIRE= re.findall("\d{2}[/]\d{2}[/]\d{4}", resul)[0]
             DATE_OF_EXPIRES = datetime.strptime(DATE_OF_EXPIRE, '%d/%m/%Y').date()
          except:
             DATE_OF_EXPIRES = "not_found"
          try:      
            N=  re.findall("[\u0600-\u06FF]+\s?",resul) 
            N=''.join(N)
            n=  re.findall("\s[\u0600-\u06FF]{2}[\u0647]\s[\u0600-\u06FF]+\s[\u0600-\u06FF]+\s[\u0600-\u06FF]+\s[\u0600-\u06FF]+\s[\u0600-\u06FF]+\s[\u0600-\u06FF]+\s[\u0600-\u06FF]+\s[\u0600-\u06FF]+\s[\u0600-\u06FF]+\s[\u0600-\u06FF]+\s[\u0600-\u06FF]+\s[\u0600-\u06FF]+\s[\u0600-\u06FF]+\s[\u0600-\u06FF]+\s[\u0600-\u06FF]+\S",N)[0]
          except:
               n="not_found"
          try:    
             result = reader.readtext("cnic_front.png",  detail = 0, paragraph=True)
             results="".join(result)
             
             CNIC_NO=re.findall(r'\d{5}[-]\d{7}[-]\d{1}', results)[0]
             cnic_no=CNIC_NO.replace("-","")
          except:
             CNIC_NO= "not_found"
          try:   
             if cnic_no== cnic:
                 fake=True
             else:
                fake=False
          except:
                 fake: False  
          try:   
             DATE_OF_BIRTH= re.findall("\d{2}[/]\d{2}[/]\d{4}", results)[0]
             DATE_OF_BIRTHS= datetime.strptime(DATE_OF_BIRTH, '%d/%m/%Y').date()
          except:
               DATE_OF_BIRTH= "not_found"
          try:    
             NAMES=  re.findall("[\u0600-\u06FF]+\s?",results) 
             NAMES=''.join(NAMES)
             nAMES=  re.findall("[\u0600-\u06FF]{3}[\u0645]\s[\u0600-\u06FF]+\s[\u0600-\u06FF]+\S",NAMES)[0]
             first_nAMES= re.findall("[\u0600-\u06FF]+\S",nAMES)[1]
             last_name= re.findall("[\u0600-\u06FF]+\S",nAMES)[2]
          except: 
                first_nAMES="not_found"
                last_name="not_found"
          try:    
             NAMES=  re.findall("[\u0600-\u06FF]+\s?",results) 
             NAMES=''.join(NAMES)
             nAMES=  re.findall("[\u0600-\u06FF]{3}[\u0645]\s[\u0600-\u06FF]+\s[\u0600-\u06FF]+\S",NAMES)[1]
             first_NAMES= re.findall("[\u0600-\u06FF]+\S",nAMES)[1]
             last_nname= re.findall("[\u0600-\u06FF]+\S",nAMES)[2]
          except: 
                first_NAMES="not_found"
                last_nname="not_found"
     

          TODAYs = date.today()
          TODAY=TODAYs.strftime("%d/%m/%Y")

          try:
             age=TODAYs - DATE_OF_BIRTHS
             if age.days<=8035:
              age="your age is under 22 years"
             else:
              age= "your age is over 22 years"   
              EXPIRE= DATE_OF_EXPIRES - TODAYs
              if EXPIRE.days<=0:
                EXPIRE="your card is expire"
              else:
                EXPIRE= "their are "+ str(EXPIRE.days)+" days remaining to expire card" 
          except:
              age="not_found"   

          try:     
              with open("dp.png", "rb") as img_file:
                my_string = base64.b64encode(img_file.read())
                img=my_string.decode('utf-8')
              img="data:image/png;base64,"+img
             
              response = requests.post("https://nraffa-liveness-detection.hf.space/run/predict", json={
              "data": [img]}).json()
              data = response["data"]
              spoof=data[0]["confidences"][0]["confidence"]

              if spoof > 0.84:
                 liveness= "spoof_img"
              try: 
                     reult= bool(DeepFace.verify(img1_path = "cnic_front.png", img2_path = "dp.png"))
                     if reult==False:
                        liveness="dp-error"
                     else: 
                      a= bool(DeepFace.verify(img1_path = "cnic_front.png", img2_path = "dp.png")["verified"]) 
                      resultoo= a 
              except:
                     liveness="dp-error"    
                     print("11-step") 
          except:
               liveness="liveness_error"
        
          #{'is_verified_person':resultoo, 'cnic':CNIC_NO,'date_of_birth':DATE_OF_BIRTH,'date_of_issue':DATE_OF_ISSUE,'date_of_expire':DATE_OF_EXPIRE, 'is_idcard_verified':fake,'first_name':first_nAMES, 'last_name':last_name, 'address':n,'expire':EXPIRE, 'today':TODAY,'age':age, 'liveness':liveness}
          info={'name':{'first_name': first_nAMES,'last_name':last_name},'father_name':{'first_name': first_NAMES,'last_name':last_nname}, 'cnic_no.': CNIC_NO, 'date_of_birth': DATE_OF_BIRTH, 'date_of_issue': DATE_OF_ISSUE, 'date_of_expire': DATE_OF_EXPIRE, 'today': TODAY, 'expire':EXPIRE, 'age': age, 'is_selfie':resultoo, 'Address':n,'is_idcard_verified':fake, 'liveness':liveness }
          return info 


def success(img1,img2,img3): 
             my_string = base64.b64decode(img1)
             imges=BytesIO(my_string)
             img=Image.open(imges)
             img.save("cnic_front.png")

             my_string = base64.b64decode(img2)
             imges=BytesIO(my_string)
             img=Image.open(imges)
             img.save("cnic_back.png")
           
             my_string = base64.b64decode(img3)
             imges=BytesIO(my_string)
             img=Image.open(imges)
             img.save("dp.png") 

             liveness="verified"
             resultoo=False
             try:         
                reader = zxing.BarCodeReader()
                #print(reader.zxing_version, reader.zxing_version_info)
                barcode = reader.decode("cnic_back.png")
            
                barcode=barcode.raw
             
                reader = easyocr.Reader(['ar']) 

                resul = reader.readtext("cnic_back.png",  detail = 0, paragraph=True)
            
                results="".join(resul)
             
                urdu=re.sub(r"[A-Za-z0-9@;:]", "", results, flags=re.UNICODE)
            
                print("bb",urdu)
                address="".join(urdu)
             except:
                  address="not_found"
             try:     
                reader = easyocr.Reader(['en']) 

                result = reader.readtext("cnic_front.png",  detail = 0, paragraph=True)
                results="".join(result)
                CNIC_NO=re.findall(r'\d{5}[-]\d{7}[-]\d{1}', results)[0]
                cnic_no=CNIC_NO.replace("-","")
             except:
                    CNIC_NO="not_found"
             try:
                cnic_from_barcode=barcode[12:25]
                if cnic_no== cnic_from_barcode:
                   fake=True
                else:
                   fake=False
             except:
                fake=False  
             
             try:
                DATE_OF_BIRTH= re.findall("\d{2}[.]\d{2}[.]\d{4}", results)[0]
                DATE_OF_BIRTH= DATE_OF_BIRTH.replace('.', '/',)
                datetime_object = datetime.strptime(DATE_OF_BIRTH, '%d/%m/%Y').date()
                DATE_OF_BIRTH=datetime_object.strftime("%m/%d/%Y")
             except:
                 DATE_OF_BIRTH="not_found"
             try:
                DATE_OF_ISSUE= re.findall("\d{2}[.]\d{2}[.]\d{4}", results)[1]
                DATE_OF_ISSUE= DATE_OF_ISSUE.replace('.', '/',)
                datetimes_object = datetime.strptime(DATE_OF_ISSUE, '%d/%m/%Y').date()
                DATE_OF_ISSUE=datetimes_object.strftime("%m/%d/%Y")
             except:
                 DATE_OF_ISSUE="not_found"  
             try:     
                DATE_OF_EXPIRE= re.findall("\d{2}[.]\d{2}[.]\d{4}", results)[2]
                DATE_OF_EXPIRE= DATE_OF_EXPIRE.replace('.', '/',)
                datetime_objects= datetime.strptime(DATE_OF_EXPIRE, '%d/%m/%Y').date()
                DATE_OF_EXPIRE=datetime_objects.strftime("%m/%d/%Y")
             except:
                 DATE_OF_EXPIRE="not_found"
            
             try:
                TODAYs = date.today()
                TODAY=TODAYs.strftime("%m/%d/%Y")

                age=TODAYs - datetime_object
                if age.days<=8035:
                   age="your age is under 22 years"
                else:
                   age= "your age is over 22 years"  
             except:
                  age="not_found" 
             try:     
                EXPIRE= datetime_objects - TODAYs
                if EXPIRE.days<=0:
                   EXPIRE="your card is expire"
                else:
                   EXPIRE= "their are "+ str(EXPIRE.days)+" days remaining to expire card" 
             except:
                   EXPIRE ="not_found" 
             try:      
                F_NAME=  re.findall("[A-Za-z]+\s?", results)
                F_NAME=''.join(F_NAME)

                NAMES=  re.findall("[A-Za-z]{3}[e]\s[A-Z][a-z]+\s[A-Z][a-z]+\S", F_NAME)[0]
                FIRST_NAMES=  re.findall("[A-Z][a-z]+\S", NAMES)[1]
                LAST_NAMES=  re.findall("[A-Z][a-z]+\S", NAMES)[2]
             except:
                   FIRST_NAMES= "not_found"
                   LAST_NAMES=  "not_found"
             try:      
                Father_name=re.findall("[A-Za-z]{3}[e]\s[A-Z][a-z]+\s[A-Z][a-z]+\S", F_NAME)[1]
                FIRST_NAME=  re.findall("[A-Z][a-z]+\S", Father_name)[1]
                LAST_NAME=  re.findall("[A-Z][a-z]+\S", Father_name)[2]
             except:
                   FIRST_NAME= "not_found"
                   LAST_NAME= "not_found"
             print("1-step")      
             try:
                print("2-step")
                with open("dp.png", "rb") as img_file:
                   print("3-step") 
                   my_string = base64.b64encode(img_file.read())
                   print("4-step") 
                   img=my_string.decode('utf-8')
                   print("5-step") 
                img="data:image/png;base64,"+img
                print("6-step") 
                response = requests.post("https://nraffa-liveness-detection.hf.space/run/predict", json={
                "data": [img]}).json()
                print("7-step") 
                data = response["data"]
                print("8-step") 
                spoof=data[0]["confidences"][0]["confidence"]
         
                if spoof > 0.84:
                      liveness= "spoof-img"
                try: 
                   reult= bool(DeepFace.verify(img1_path = "cnic_front.png", img2_path = "dp.png"))
                   if reult==False:
                      liveness="dp-error"
                   else: 
                      a= bool(DeepFace.verify(img1_path = "cnic_front.png", img2_path = "dp.png")["verified"]) 
                      resultoo= a 
                except:
                     liveness="dp-error"    
                     print("11-step") 
             except:
                   print("13-step") 
                   liveness= "liveness_error"
                       
              
        
        

            
             my_information ={'name':{'first_name': FIRST_NAMES,'last_name':LAST_NAMES},'father_name':{'first_name': FIRST_NAME,'last_name':LAST_NAME}, 'cnic_no.': CNIC_NO, 'date_of_birth': DATE_OF_BIRTH, 'date_of_issue': DATE_OF_ISSUE, 'date_of_expire': DATE_OF_EXPIRE, 'today': TODAY, 'expire':EXPIRE, 'age': age, 'is_selfie':resultoo, 'Address':address,'is_idcard_verified':fake, 'liveness':liveness }
             return my_information        