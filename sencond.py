import cv2
from flask import * 
from PIL import Image
from methods import success,successed

app = Flask(__name__)  
@app.route('/')  
def main():  
    return render_template("index.html")     
@app.route('/successful', methods = ['POST'])  
def mains():             
 if request.method == 'POST':  
          f1 = request.files['cnic_front']
 
          a=Image.open("cnic_front.png")

          f2= request.files['cnic_back']
      
          b=Image.open("cnic_back.png")
            
          f3= request.files['dp']
    
          c=Image.open("dp.png")
        
          try:
               result=success(a,b,c)
          except:
               result=successed(a,b,c)   
          return result     


if __name__ == '__main__':  
    app.run(port=5007, debug=True)