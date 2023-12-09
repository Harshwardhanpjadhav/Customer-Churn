from src.churn.pipeline.prediction_pipeline import CustomData,PredictPipeline

from flask import Flask,request,render_template,jsonify


app=Flask(__name__)


@app.route('/')
def home_page():
    return render_template("index.html")


@app.route("/churn",methods=["GET","POST"])
def predict_datapoint():
    if request.method == "GET":
        return render_template("form.html")
    
    else:
        data=CustomData(

            Age = int(request.form.get('Age')),
            Married = object(request.form.get('Married')),
            Offer = object(request.form.get('Offer')),
            Phone_Service = object(request.form.get('Phone Service')),
            Avg_Monthly_Long_Distance_Charges = float(request.form.get('Avg Monthly Long Distance Charges')),
            Multiple_Lines = object(request.form.get('Multiple Lines')),
            Internet_Type = object(request.form.get('Internet Type')),
            Avg_Monthly_GB_Download = float(request.form.get('Avg Monthly GB Download')),
            Online_Security = object(request.form.get('Online Security')),
            Online_Backup = object(request.form.get('Online Backup')),
            Device_Protection_Plan = object(request.form.get('Device Protection Plan')),
            Premium_Tech_Support = object(request.form.get('Premium Tech Support')),
            Streaming_TV = object(request.form.get('Streaming TV')),
            Streaming_Movies = object(request.form.get('Streaming Movies')),
            Streaming_Music = object(request.form.get('Streaming Music')),
            Contract = object(request.form.get('Contract')),
            Paperless_Billing = object(request.form.get('Paperless Billing')),
            Payment_Method = object(request.form.get('Payment Method')),
            Monthly_Charge = float(request.form.get('Monthly Charge')),
            Total_Charges = float(request.form.get('Total Charges')),
            Total_Long_Distance_Charges = float(request.form.get('Total Long Distance Charges')),
            #Customer_Status = object(request.form.get('Customer_Status'))
        )

        # this is my final data
        final_data=data.get_data_as_dataframe()
        
        predict_pipeline=PredictPipeline()
        
        pred=predict_pipeline.predict(final_data)
        
        result=round(pred[0],2)
        
        return render_template("result.html",final_result=result)

#execution begin
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8000)
