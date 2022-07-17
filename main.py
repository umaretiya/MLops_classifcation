from django.shortcuts import redirect
from flask import Flask,render_template, flash, request
import io
import pickle,bz2
import numpy as np
import pandas as pd

app = Flask(__name__)


# with open("D:\\PycharmProjects\\DS_ML_Self\\MLops_classifcation\\notebooks\\xgb_banking.pkl", "rb") as f:
    # file = f.read()
with open("D:\\PycharmProjects\\DS_ML_Self\\MLops_classifcation\\notebooks\\xgb_banking.pkl", "rb") as file:
    pick = file.read()
    gredeint_model = pickle.loads(pick)

keys = ['LIMIT_BAL', 'PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6', 
        'BILL_AMT1', 'BILL_AMT2', 'BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6', 
        'PAY_AMT1', 'PAY_AMT2', 'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6']

dict_data = {'PAY_0':-1, 'PAY_2':3, 'PAY_3':0, 'PAY_4':0, 'PAY_5':4, 'PAY_6':1, 'BILL_AMT2':2000,
       'BILL_AMT3':5000, 'BILL_AMT4':3400, 'BILL_AMT5':10000, 'BILL_AMT6':2500, 'PAY_AMT1':0,
       'PAY_AMT2':1000, 'PAY_AMT3':2000, 'PAY_AMT4':1000}

@app.route("/", methods=['GET','POST'])
def home():

    try:
        LIMIT_BAL = request.form.get('LIMIT_BAL')
        PAY_0 = request.form.get('PAY_0')
        PAY_2 = request.form.get('PAY_2')
        PAY_3 = request.form.get('PAY_3')
        PAY_4 = request.form.get('PAY_4')
        PAY_5 = request.form.get('PAY_5')
        PAY_6 = request.form.get('PAY_6')
        BILL_AMT1 = request.form.get('BILL_AMT1')
        BILL_AMT2 = request.form.get('BILL_AMT2')
        BILL_AMT3 = request.form.get('BILL_AMT3')
        BILL_AMT4 = request.form.get('BILL_AMT4')
        BILL_AMT5 = request.form.get('BILL_AMT5')
        BILL_AMT6 = request.form.get('BILL_AMT6')
        PAY_AMT1 = request.form.get('PAY_AMT1')
        PAY_AMT2 = request.form.get('PAY_AMT2')
        PAY_AMT3 = request.form.get('PAY_AMT3')
        PAY_AMT4 = request.form.get('PAY_AMT4')
        PAY_AMT5 = request.form.get('PAY_AMT5')
        PAY_AMT6 = request.form.get('PAY_AMT6')
        input_data={'LIMIT_BAL':LIMIT_BAL, 'PAY_0':PAY_0, 'PAY_2':PAY_2, 'PAY_3':PAY_3, 
                    'PAY_4':PAY_4, 'PAY_5':PAY_5, 'PAY_6':PAY_6, 
            'BILL_AMT1':BILL_AMT1, 'BILL_AMT2':BILL_AMT2, 'BILL_AMT3':BILL_AMT3, 'BILL_AMT4':BILL_AMT4, 
            'BILL_AMT5':BILL_AMT5, 'BILL_AMT6':BILL_AMT6, 
            'PAY_AMT1':PAY_AMT1, 'PAY_AMT2':PAY_AMT2, 'PAY_AMT3':PAY_AMT3, 'PAY_AMT4':PAY_AMT4, 
            'PAY_AMT5':PAY_AMT5, 'PAY_AMT6':PAY_AMT6}
        
        # return render_template("index.html")
    except Exception as e:
        return render_template('index.html', prediction="Check the Input again!!!")
    
    return render_template("index.html")


@app.route('/classify',methods=['POST',"GET"])
def classify():
    if request.method == 'POST':
        # try:
        # LIMIT_BAL = request.form.get('LIMIT_BAL')
        PAY_0 = request.form.get('PAY_0')
        PAY_2 = request.form.get('PAY_2')
        PAY_3 = request.form.get('PAY_3')
        PAY_4 = request.form.get('PAY_4')
        PAY_5 = request.form.get('PAY_5')
        PAY_6 = request.form.get('PAY_6')
        # BILL_AMT1 = request.form.get('BILL_AMT1')
        BILL_AMT2 = request.form.get('BILL_AMT2')
        BILL_AMT3 = request.form.get('BILL_AMT3')
        BILL_AMT4 = request.form.get('BILL_AMT4')
        BILL_AMT5 = request.form.get('BILL_AMT5')
        BILL_AMT6 = request.form.get('BILL_AMT6')
        PAY_AMT1 = request.form.get('PAY_AMT1')
        PAY_AMT2 = request.form.get('PAY_AMT2')
        PAY_AMT3 = request.form.get('PAY_AMT3')
        PAY_AMT4 = request.form.get('PAY_AMT4')
        # PAY_AMT5 = request.form.get('PAY_AMT5')
        # PAY_AMT6 = request.form.get('PAY_AMT6')
        dict_data = {'PAY_0':-1, 'PAY_2':3, 'PAY_3':0, 'PAY_4':0, 'PAY_5':4, 'PAY_6':1, 'BILL_AMT2':2000,
        'BILL_AMT3':5000, 'BILL_AMT4':3400, 'BILL_AMT5':10000, 'BILL_AMT6':2500, 'PAY_AMT1':0,
        'PAY_AMT2':1000, 'PAY_AMT3':2000, 'PAY_AMT4':1000}
        
        input_data={'PAY_0':PAY_0, 'PAY_2':PAY_2, 'PAY_3':PAY_3, 
                    'PAY_4':PAY_4, 'PAY_5':PAY_5, 'PAY_6':PAY_6, 
            'BILL_AMT2':BILL_AMT2, 'BILL_AMT3':BILL_AMT3, 'BILL_AMT4':BILL_AMT4, 
            'BILL_AMT5':BILL_AMT5, 'BILL_AMT6':BILL_AMT6, 
            'PAY_AMT1':PAY_AMT1, 'PAY_AMT2':PAY_AMT2, 'PAY_AMT3':PAY_AMT3, 'PAY_AMT4':PAY_AMT4}
        
        xint =[float(i) for i in input_data.values()]
        array_input = np.array(xint).reshape(1,15)
        results = gredeint_model.predict(array_input)
        print(results)
        if results[0] == 0:
            flash("Results is 0, No chanse for defalut: ","success")
            return render_template("index.html",context={"message":results[0]})
        else:
            flash("Results is 1, High chanse for defalut: ","warning")
            return render_template("classifcation_data.html",context={"message": results[0]})
    # except:
    #     flash("Something went wrong")
    #     return render_template("index.html",context={"message": gredeint_model})
    else:
        # flash("Results is 0, No chanse for defalut: ","success")
        return render_template("classifcation_data.html",context={"message":"Post method doesn't works"})
        



if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.run(debug=True)