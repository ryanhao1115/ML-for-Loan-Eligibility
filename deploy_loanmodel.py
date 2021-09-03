from flask import render_template, request, jsonify,Flask
import flask
import numpy as np
import traceback
import pickle
import pandas as pd
import json


# App definition
app = Flask(__name__)

# importing models
with open('loan_model.sav', 'rb') as f:
   model = pickle.load (f)



@app.route('/')
def welcome():
   return "Welcome! Use this Flask App for applying loan."

@app.route('/predict', methods=['POST','GET'])
def predict():

   if flask.request.method == 'GET':
       return "Prediction page. Try using post with params to get specific prediction."

   if flask.request.method == 'POST':
       try:
           json_ = request.json
           print('*********-----------')
           print(type(json_)) 
           print(json_)
           print('****************-------------')
           df = pd.DataFrame.from_dict(json_)
           #x=json.loads(json_)
           #df=pd.DataFrame(x)
           print(df)
           y_pred = model.predict(df)
           if y_pred == 1:
                result = 'Approved'
           else: 
                result = 'Rejected'
                

           return jsonify({
               "prediction":result
           })

       except:
           return jsonify({
               "trace": traceback.format_exc()
               })

df_t = pd.DataFrame(columns=['Gender','Married','Dependents',
                             'Education','Property_Area','Self_Employed','ApplicantIncome',
                             'CoapplicantIncome','LoanAmount','Loan_Amount_Term','Credit_History'])
num_col = ['ApplicantIncome','CoapplicantIncome','LoanAmount','Loan_Amount_Term','Credit_History']
categ_col = ['Gender','Married','Dependents','Education','Property_Area','Self_Employed']
    
@app.route('/submit', methods=['GET'])
def submit():
    for x in request.args:
        if x in num_col:
            df_t.loc[0, x] = float(request.args[x])
        elif x in categ_col:
            df_t.loc[0, x] = request.args[x]
        else:
            return "You submited wrong key words!"
    print('***********--------------')
    print(df_t)
    y_pred = model.predict(df_t)
    if y_pred == 1:
        return "<h1> Congratulations, your loan has been approved! </h1>"
    else:
        return "Sorry, your application is rejected!"
    


if __name__ == "__main__":
   app.run(host='0.0.0.0',port=5555)
