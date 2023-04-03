import cv2
from flask import * 
from PIL import Image
from methods import success,successed,fin
import base64
 
app = Flask(__name__) 

@app.route('/')  
def main():   
    return render_template("index.html")  

@app.route('/successful/fingers', methods = ['POST'])  
def fingers(): 
    if request.method == 'POST': 
       data = json.loads(request.data)
       print(type(data))
       a=data["hand"]
       print(type(a)) 
          
    result=fin(a)    
    return result

@app.route('/successful', methods = ['POST'])  
def mains():             
 if request.method == 'POST':  
          data = json.loads(request.data)
          print(type(data))
          a=data["cnic_front"]
          print(type(a))

          b= data['cnic_back']
            
          c= data['dp']
        
          try:
               result=successed(a,b,c) 
          except:
                result=success(a,b,c) 
          return result     

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5008, debug=True)

