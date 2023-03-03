from distutils.log import debug
from fileinput import filename
from flask import * 
from PIL import Image
import base64
from io import BytesIO
from datetime import datetime,date
import easyocr
import re
from deepface import DeepFace
import zxing
app = Flask(__name__)  
  
@app.route('/')  
def main():  
    return render_template("index.html")  
  
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']
        #f.save(f.filename) 
        #a=pytesseract.image_to_string(f.filename)
        with open(f.filename, "rb") as img_file:
         my_string = base64.b64encode(img_file.read())
        
         #return my_string
        return render_template("response.html", name =  my_string)   
@app.route('/successful', methods = ['POST'])  
def successed(): 
             data=json.loads(request.data)
             d=data['cnic-img']
             print(type(d))
             dat=json.dumps(d).encode('utf-8')
             print(type(dat))
             
             my_string = base64.b64decode(dat)
             imges=BytesIO(my_string)
             img=Image.open(imges)
             print(img)
             img.save("ggg.png")
             i= img.show()
            
             a=data['dp-img']
             print(type(a))
             da=json.dumps(a).encode('utf-8')
             print(type(da))
        
             my_string = base64.b64decode(da)
             imges=BytesIO(my_string)
             img=Image.open(imges)
             img.save("hhh.png")
             i= img.show()

            
             e=data['cnic-back-img']
             print(type(e))
             dae=json.dumps(e).encode('utf-8')
             
             
             my_strin = base64.b64decode(dae)
             
             imge=BytesIO(my_strin)
             
             img=Image.open(imge)
             img.save("bbb.png")
             img.show()
             print(img)

             reader = zxing.BarCodeReader()
             print(reader.zxing_version, reader.zxing_version_info)
             barcode = reader.decode("bbb.png")
             print(barcode)
             barcode=barcode.raw

             reader = easyocr.Reader(['ar']) 

             resul = reader.readtext("bbb.png",  detail = 0, paragraph=True)
             print(resul)
             results="".join(resul)
             
             urdu=re.sub(r"[A-Za-z0-9@;:]", "", results, flags=re.UNICODE)
            

             address="".join(urdu)

             

             CNIC_NO1=re.findall(r'\d{5}[-]\d{7}[-]\d{1}', results)[0]
             print(CNIC_NO1)

             
             reader = easyocr.Reader(['en']) 

             result = reader.readtext("ggg.png",  detail = 0, paragraph=True)
             results="".join(result)
        
             CNIC_NO=re.findall(r'\d{5}[-]\d{7}[-]\d{1}', results)[0]
             cnic_no=CNIC_NO.replace("-","")
             cnic_from_barcode=barcode[12:25]
             if cnic_no== cnic_from_barcode:
                fake=True
             else:
                fake=False
             

             DATE_OF_BIRTH= re.findall("\d{2}[.]\d{2}[.]\d{4}", results)[0]
             DATE_OF_BIRTH= DATE_OF_BIRTH.replace('.', '/',)
             datetime_object = datetime.strptime(DATE_OF_BIRTH, '%d/%m/%Y').date()
             DATE_OF_BIRTH=datetime_object.strftime("%m/%d/%Y")

             DATE_OF_ISSUE= re.findall("\d{2}[.]\d{2}[.]\d{4}", results)[1]
             DATE_OF_ISSUE= DATE_OF_ISSUE.replace('.', '/',)
             datetimes_object = datetime.strptime(DATE_OF_ISSUE, '%d/%m/%Y').date()
             DATE_OF_ISSUE=datetimes_object.strftime("%m/%d/%Y")

             DATE_OF_EXPIRE= re.findall("\d{2}[.]\d{2}[.]\d{4}", results)[2]
             DATE_OF_EXPIRE= DATE_OF_EXPIRE.replace('.', '/',)
             datetime_objects= datetime.strptime(DATE_OF_EXPIRE, '%d/%m/%Y').date()
             DATE_OF_EXPIRE=datetime_objects.strftime("%m/%d/%Y")

             TODAYs = date.today()
             TODAY=TODAYs.strftime("%m/%d/%Y")

             age=TODAYs - datetime_object
             if age.days<=8035:
              age="your age is under 22 years"
             else:
              age= "your age is over 22 years"   
              EXPIRE= datetime_objects - TODAYs
              if EXPIRE.days<=0:
                EXPIRE="your card is expire"
              else:
                EXPIRE= "their are "+ str(EXPIRE.days)+" days remaining to expire card" 
                F_NAME=  re.findall("[A-Za-z]+\s?", results)
                F_NAME=''.join(F_NAME)

                NAMES=  re.findall("[A-Za-z]{3}[e]\s[A-Z][a-z]+\s[A-Z][a-z]+\S", F_NAME)[0]
                FIRST_NAMES=  re.findall("[A-Z][a-z]+\S", NAMES)[1]
                LAST_NAMES=  re.findall("[A-Z][a-z]+\S", NAMES)[2]

                Father_name=re.findall("[A-Za-z]{3}[e]\s[A-Z][a-z]+\s[A-Z][a-z]+\S", F_NAME)[1]
                FIRST_NAME=  re.findall("[A-Z][a-z]+\S", Father_name)[1]
                LAST_NAME=  re.findall("[A-Z][a-z]+\S", Father_name)[2]
            
            
           
             if LAST_NAME==re.findall("[A-Z][a-z]+[L]", LAST_NAME)[0]:
              LAST_NAME= LAST_NAME[::-1]
              LAST_NAME= LAST_NAME.replace("L", '',1)
              LAST_NAME= LAST_NAME[::-1]
           
             result = DeepFace.verify(img1_path = "ggg.png", img2_path = "hhh.png")
             result=result['verified']
              
        
        

             #a=type(result)
             my_information ={'name':{'first-name': FIRST_NAMES,'last-name':LAST_NAMES},'father-name':{'first-name': FIRST_NAME,'last-name':LAST_NAME}, 'cnic-no.': CNIC_NO, 'date-of-birth': DATE_OF_BIRTH, 'date-of-issue': DATE_OF_ISSUE, 'date-of-expire': DATE_OF_EXPIRE, 'today': TODAY, 'expire':EXPIRE, 'age': age, 'is-selfie':result, 'Address':address,'is_idcard_verified':fake }
             return my_information
            
             
             my_string = base64.b64encode(data)
             imges=BytesIO(my_string)
             data = data.decode("utf-8")
             d= data['img']
             my_string = base64.b64encode(d)
             img=Image.open(imges)
             img.save("dddd.png")
             return  img
             

            
           
             
             #with open("imageToSave.png", "wb") as fh:
              #fh.write(my_string.decode('base64'))
             
            
             #
             #a=pytesseract.image_to_string(img)
            
            
             #return render_template("respon.html", name = imges )  
                


if __name__ == '__main__':  
    app.run(port=5007, debug=True)