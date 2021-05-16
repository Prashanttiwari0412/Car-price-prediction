
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

def Convert(d):
    Year=d.get("Year")
    Year=int(Year)
    Owner_Type=d.get("Owner_Type")
    Owner_Type=int(Owner_Type)
    Mileage=d.get("Mileage")
    Mileage=float(Mileage)

    Engine=d.get("Engine")
    Engine=int(Engine)
    Power=d.get("Power")
    Power=float(Power)
    Seats=d.get("Seats")
    Seats=int(Seats)
    if d.get("Fuel_Type")== "Diesel":
        Fuel_Type_Diesel=1
        Fuel_Type_LPG=0
        Fuel_Type_Petrol=0
    elif d.get("Fuel_Type")== "Petrol":
        Fuel_Type_Diesel=0
        Fuel_Type_LPG=0
        Fuel_Type_Petrol=1
    else :
        Fuel_Type_Diesel=0
        Fuel_Type_LPG=1
        Fuel_Type_Petrol=0


    if d.get("Transmission")=="Manual":
        Transmission_Manual=1
    else:
        Transmission_Manual=0
    
    def create_dict(Year,Owner_Type,Mileage,Engine,Power,Seats,Fuel_Type_Diesel,Fuel_Type_LPG,Fuel_Type_Petrol,Transmission_Manual):
        final_dict=[{"Year":Year,"Owner_Type":Owner_Type,"Mileage":Mileage,"Engine":Engine,"Power":Power,
                "Seats":Seats,"Fuel_Type_Diesel":Fuel_Type_Diesel,"Fuel_Type_LPG":Fuel_Type_LPG,
                "Fuel_Type_Petrol":Fuel_Type_Petrol,
                "Transmission_Manual":Transmission_Manual
               
               }]
        final=pd.DataFrame(final_dict)
        pred_t=model.predict(final)
        return pred_t
        
        
    pred=create_dict(Year,Owner_Type,Mileage,Engine,Power,Seats,Fuel_Type_Diesel,Fuel_Type_LPG,Fuel_Type_Petrol,Transmission_Manual)
    return pred
    















@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    d=request.form
    pred_1=Convert(d)
    
    
    
    return render_template('result.html', prediction_text="Your Car's Price Should Be {:.2f} lakhs".format(float(pred_1)))


if __name__ == "__main__":
    app.run(debug=True)