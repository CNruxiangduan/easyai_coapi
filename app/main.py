import os
from flask import Flask,request,g
from ultralytics import YOLO
import json
import io
from PIL import Image
import cv2
app = Flask(__name__)
# @app.before_first_request
# # def first_request():
# #     g.detModel=YOLO("/app/yolov8n.pt")
# #     return g.detModel
@app.before_first_request
def init_request():    
    app.detModel=YOLO("/app/yolov8n.pt")    
    return app.detModel

@app.route('/count_api', methods=['POST'])
def predict():        
    if request.method != 'POST':        
        return
    if request.files.get('image'):        
        # Method 1        
        # with request.files["image"] as f:        
            # im = Image.open(io.BytesIO(f.read()))
        # Method 2        
        im_file = request.files['image']        
        im_bytes = im_file.read()        
        im = Image.open(io.BytesIO(im_bytes))   

        w, h = im.size        
        if h>w and h>640:            
            rate =640/h            
            new_h = 640            
            new_w = w*rate        
        elif h<w and w>640:            
            rate =640/w            
            new_h = h*rate            
            new_w = 640 

        print(w,h)        
        print(int(new_w), int(new_h))        
        im = im.resize((int(new_w), int(new_h)))        
        results = app.detModel(source=im)        
        # print(results)        
        re_results = {"det_res":{}}                
        names = results[0].names
        cls = results[0].boxes.cls.numpy()    # cls, (N, 1)        
        probs = results[0].boxes.conf.numpy()  # confidence score, (N, 1)        
        boxes = results[0].boxes.xyxy.numpy()   # box with xyxy format, (N, 4)        
        # print(cls)       
        # print(probs)        
        # print(boxes)        
        results = list(results)        
           
        res_plotted =results[0].plot()        
        cv2.imwrite("./static/img/img.jpg",res_plotted)        
        for i in range(boxes.shape[0]):            
            box = boxes[i]            
            id = cls[i]            
            label = names[id]            
            if label not in re_results["det_res"].keys():                
                re_results["det_res"][label]={"boxes":[box.tolist()],"num":1}        
            else:                
                re_results["det_res"][label]["boxes"].append(box.tolist())                
                re_results["det_res"][label]["num"]+=1
    re_results["res_URL"]="https://flask-hp6c-32790-7-1317006726.sh.run.tcloudbase.com/static/img/img.jpg"
    return json.dumps(re_results)
if __name__ == "__main__":    # Load a model    
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 80)))