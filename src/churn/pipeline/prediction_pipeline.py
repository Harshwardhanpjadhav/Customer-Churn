import os
import sys
import pandas as pd
from src.churn.exception import CustomException
from src.churn.logger import logging
from src.churn.utils.main_utilis import load_object


class PredictPipeline:
    def __init__(self):
        pass
    
    def predict(self,features):
        try:
            preprocessor_path=os.path.join("artifact","preprocessing.pkl")
            model_path=os.path.join("artifact","model.pkl")
            
            preprocessor=load_object(preprocessor_path)
            model=load_object(model_path)
            
            scaled_data=preprocessor.transform(features)
            
            pred=model.predict(scaled_data)
            
            return pred
            
        except Exception as e:
            raise CustomException(e,sys)
    
    
    
class CustomData:
    def __init__(self,
                 Age:int,
                 Married:object,
                 Offer:object,
                 Phone_Service:object,
                 Avg_Monthly_Long_Distance_Charges:float,
                 Multiple_Lines:object,
                 Internet_Type:object,
                 Avg_Monthly_GB_Download:float,
                 Online_Security:object,
                 Online_Backup:object,
                 Device_Protection_Plan:object,
                 Premium_Tech_Support:object,
                 Streaming_TV:object,
                 Streaming_Movies:object,
                 Streaming_Music: object,
                 Contract:object,
                 Paperless_Billing:object,
                 Payment_Method:object,
                 Monthly_Charge:float,
                 Total_Charges:float,
                 Total_Long_Distance_Charges:float,
                 #Customer_Status:object
                 ):
        
            self.Age=Age
            self.Married=Married
            self.Offer=Offer
            self.Phone_Service=Phone_Service
            self.Avg_Monthly_Long_Distance_Charges=Avg_Monthly_Long_Distance_Charges
            self.Multiple_Lines=Multiple_Lines
            self.Internet_Type=Internet_Type
            self.Avg_Monthly_GB_Download=Avg_Monthly_GB_Download
            self.Online_Security=Online_Security
            self.Online_Backup=Online_Backup
            self.Device_Protection_Plan=Device_Protection_Plan
            self.Premium_Tech_Support=Premium_Tech_Support
            self.Streaming_TV=Streaming_TV
            self.Streaming_Movies=Streaming_Movies
            self.Streaming_Music=Streaming_Music
            self.Contract=Contract
            self.Paperless_Billing=Paperless_Billing
            self.Payment_Method=Payment_Method
            self.Monthly_Charge=Monthly_Charge
            self.Total_Charges=Total_Charges
            self.Total_Long_Distance_Charges=Total_Long_Distance_Charges
            #self.Customer_Status=Customer_Status
    
    def get_data_as_dataframe(self):
            try:
                custom_data_input_dict = {
                    'Age':[self.Age], 
                    'Married':[self.Married], 
                    'Offer':[self.Offer], 
                    'Phone_Service':[self.Phone_Service], 
                    'Avg_Monthly_Long_Distance_Charges':[self.Avg_Monthly_Long_Distance_Charges], 
                    'Multiple_Lines':[self.Multiple_Lines],
                    'Internet_Type':[self.Internet_Type],
                    'Avg_Monthly_GB_Download':[self.Avg_Monthly_GB_Download], 
                    'Online_Security':[self.Online_Security], 
                    'Online_Backup':[self.Online_Backup], 
                    'Device_Protection_Plan':[self.Device_Protection_Plan], 
                    'Premium_Tech_Support':[self.Premium_Tech_Support], 
                    'Streaming_TV':[self.Streaming_TV],
                    'Streaming_Movies':[self.Streaming_Movies], 
                    'Streaming_Music':[self.Streaming_Music], 
                    'Contract':[self.Contract], 
                    'Paperless_Billing':[self.Paperless_Billing], 
                    'Payment_Method':[self.Payment_Method],
                    'Monthly_Charge':[self.Monthly_Charge],
                    'Total_Charges':[self.Total_Charges], 
                    'Total_Long_Distance_Charges':[self.Total_Long_Distance_Charges], 
                    #'Customer_Status':[self.Customer_Status]
                }
                df = pd.DataFrame(custom_data_input_dict)
                logging.info('Dataframe Gathered')
                return df
            except Exception as e:
                logging.info('Exception Occured in prediction pipeline')
                raise CustomException(e,sys)