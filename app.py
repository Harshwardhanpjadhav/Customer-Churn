import os
import pandas as pd
from flask import Flask,request,render_template,jsonify,send_file
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

#=======================================================================================================
@app.route('/predict/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    if file and file.filename.endswith('.csv'):
        df = pd.read_csv(file,index_col=None)
        model = PredictPipeline()
        pred_df = model.predict_csv(df)

        Total_Customers = pred_df.shape
        Total_Customers = Total_Customers[0]

        churned = pred_df.value_counts()
        Stayed = pred_df.value_counts()
        churned_count = churned['Churned']
        Stayed_count = Stayed['Stayed']

        return render_template('result_csv.html',churned=churned_count,stayed=Stayed_count,Total_Customers=Total_Customers)
    else:
        return "Invalid file format. Please upload a CSV file."
    

#=======================================================================================================
@app.route('/predict/manualy')
def manualy():
    return render_template('manual.html')

app.run(debug=True,port=8000)