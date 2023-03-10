from flask import Flask
import datetime
import os
import numpy as np
import pickle


from keras.applications.imagenet_utils import preprocess_input,decode_predictions
from keras.models import load_model
from keras.preprocessing import image

from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
  
x = datetime.datetime.now()
  
# Initializing flask app
app = Flask(__name__)


def model_predict(img_path,model):
    
    img = image.load_img(img_path)

    x=image.img_to_array(img)

    x = np.expand_dims(x,axis=0)

    x = preprocess_input(x,mode='caffe')

    preds = model.predict(x)
    return preds

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        with open(r"C:\Users\DELL\Desktop\demo1\backend\models\rebuilt.HRmodel.pkl","rb") as f:
            model=pickle.load(f)
        
        preds = model_predict(file_path,model)

        pred_class = decode_predictions(preds,top=1)
        result = str(pred_class[0][0][1])
        return result
    return 
      
# Running app
if __name__ == '__main__':
    app.run(debug=True)