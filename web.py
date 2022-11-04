import pandas as pd
from flask import Flask,request,render_template
import pickle
from sklearn.preprocessing import MinMaxScaler
model = pickle.load(open('model.pkl', 'rb'))


app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/show')
def show():
    return render_template('prediction.html')

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    if request.method == "POST":
        tenure=float(request.form['Tenure'])
        citytier=float(request.form['CityTier'])
        warethome=float(request.form['WarehouseToHome'])
        paymode=request.form['PreferredPaymentMode']
        hourapp=float(request.form['HourSpendOnApp'])
        nofdev=float(request.form['NumberOfDeviceRegistered'])
        ordhike=float(request.form['OrderAmountHikeFromlastYear'])
        gender=request.form['Gender']
        ordcnt=float(request.form['OrderCount'])
        logdev=request.form['PreferredLoginDevice']
        daylastord=float(request.form['DaySinceLastOrder'])
        nofadd=float(request.form['NumberOfAddress'])
        cashback=float(request.form['CashbackAmount'])
        ordcat=float(request.form['PreferedOrderCat'])
        satscore=float(request.form['SatisfactionScore'])
        coupused=float(request.form['CouponUsed'])
        marstat=request.form['MaritalStatus']
        complain=float(request.form['Complain'])

        #payment mode
        if paymode==1:
            dc=1.0
            cc=0.0
            cod=0.0
            upi=0.0
            ewall=0.0
        elif paymode==2:
            dc=0.0
            cc=1.0
            cod=0.0
            upi=0.0
            ewall=0.0
        elif paymode==3:
            dc=0.0
            cc=0.0
            cod=1.0
            upi=0.0
            ewall=0.0
        elif paymode==4:
            dc=0.0
            cc=0.0
            cod=0.0
            upi=1.0
            ewall=0.0
        else:
            dc=0.0
            cc=0.0
            cod=0.0
            upi=0.0
            ewall=1.0
        
        #Gender
        if gender=='M':
            male=1.0
            female=0.0
        else:
            female=1.0
            male=0.0
            
        #Login Device
        if logdev=='Computer':
            computer=1.0
            phone=0.0
        else:
            computer=0.0
            phone=1.0
            
        #Marital Status
        if marstat=='Single':
            single=1.0
            married=0.0
            divorced=0.0
        elif marstat=='Married':
            single=0.0
            married=1.0
            divorced=0.0
        else:
            single=0.0
            married=0.0
            divorced=1.0

        data = {'Tenure':[tenure], 'CityTier':[citytier], 'WarehouseToHome':[warethome], 'HourSpendOnApp':[hourapp], 'NumberOfDeviceRegistered':[nofdev], 'PreferedOrderCat':[ordcat], 'SatisfactionScore':[satscore], 'NumberOfAddress':[nofadd], 'Complain':[complain], 'OrderAmountHikeFromlastYear':[ordhike], 'CouponUsed':[coupused], 'OrderCount':[ordcnt], 'DaySinceLastOrder':[daylastord], 'CashbackAmount':[cashback], 'PreferredPaymentMode_Cash on Delivery':[cod], 'PreferredPaymentMode_Credit Card':[cc], 'PreferredPaymentMode_Debit Card':[dc], 'PreferredPaymentMode_E wallet':[ewall], 'PreferredPaymentMode_UPI':[upi], 'PreferredLoginDevice_Computer':[computer], 'PreferredLoginDevice_Phone':[phone], 'Gender_Female':[female], 'Gender_Male':[male], 'MaritalStatus_Divorced':[divorced], 'MaritalStatus_Married':[married], 'MaritalStatus_Single':[single]}

       
        df = pd.DataFrame(data)
        
        min_max=MinMaxScaler(feature_range=(0,1))
        df_scaled = pd.DataFrame(min_max.fit_transform(df),columns = df.columns)

        prediction = model.predict(df_scaled)
        
        if prediction.item()==1:
            output='will chrn.'
        else:
            output='will not churn'

        return render_template ('result.html',prediction_text="There is 97% chance that your customer "+output)

if __name__=='__main__':
      app.run(port=8000)

