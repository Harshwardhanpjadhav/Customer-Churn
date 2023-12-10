import os
import pandas as pd
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
def uploadpage():
    return render_template('csv.html')


@app.route('/predict/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    if file and file.filename.endswith('.csv'):
        df = pd.read_csv(file)
        # Now you have the DataFrame (df) from the uploaded CSV file
        return df.to_html()  # For demonstration, you can return HTML representation of the DataFrame
    else:
        return "Invalid file format. Please upload a CSV file."
#=======================================================================================================

@app.route('/predict/manualy')
def manualy():
    return render_template('manual.html')

app.run(debug=True,port=8000)