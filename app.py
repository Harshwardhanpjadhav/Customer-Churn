import os
from flask import Flask,request,render_template,jsonify
from src.churn.pipeline.prediction_pipeline import PredictPipeline

app = Flask(__name__)

# Home Page
@app.route('/')
def homepage():
    return render_template('home.html')
#=======================================================================================================
# Train Model Page
@app.route('/trainModel')
def trainmodelpage():
    return render_template('train.html')

@app.route('/trainModel',methods=['GET','POST'])
def starttraining():
    os.system("python main.py")
    return render_template('success.html')
#=======================================================================================================
# Predict Page
@app.route('/predict')
def predictpage():
    return render_template('predict.html')

#=======================================================================================================

@app.route('/predict/uploadcsv')
def uploadcsv():
    return render_template('train.html')

#=======================================================================================================

@app.route('/predict/manualy')
def manualy():
    return render_template('manual.html')

app.run(debug=True,port=8000)