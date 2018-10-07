from flask import *
from twilio.rest import Client
import pandas as pd
import random
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix,roc_auc_score,roc_curve
import numpy as np
import matplotlib.pyplot as plt
import scipy
import mlxtend
import pygeoip
from sklearn.externals import joblib

app = Flask(__name__)


# twilio----------------------------------------------------------------------------------------------------------------
tonum = "+917702323506"
account_sid = 'AC5ef2ac76764f0e878407f86fdb5468db'
auth_token = '8cafc221f3811d84ed5b15da949af40b'

clas = 0

a = str(random.randint(9999,99999))
url1 = 'https://handler.twilio.com/twiml/EHe67d2f134b9149bb803d161f52cd620a?Name=Harsha&Numb='+str(a)

# ----------------------------------------------------------------------------------------------------------------------

df = pd.read_csv(r"C:\Users\bhava\PycharmProjects\untitled\creditcardwithD.csv")
df.set_index('Number', inplace=True)

total_amount = 0
# Webpages---------------------------------------------------------------------------------------------------------------


@app.route('/', methods=['GET','POST'])
def home():
    return render_template('orders.html')


@app.route('/payment', methods=['GET','POST'])
def get_order_amount():
    if request.method == "GET":
        return render_template('payment.html')
    elif request.method == "POST":
        p1= 500*int(request.form['p1'])
        p2 = 2000 * int(request.form['p2'])
        p3 = 15000 * int(request.form['p3'])
        p4 = 92000 * int(request.form['p4'])
        total_amount = p1+p2+p3+p4
        if total_amount == 0:
            oh = "Please select any product"
            return render_template('orders.html', oh = oh)
    return render_template('payment.html',ta=total_amount)


@app.route('/submit', methods=['GET','POST'])
def payment_page():
    if request.method == "GET":
        return render_template('payment.html')
    elif request.method == "POST":

        first_name = request.form['fn']
        last_name = request.form['ln']
        credit_card_number = request.form['cc']
        cc = int(request.form['cc'])
        cvv = request.form['cvv']
        ip1 = request.remote_addr
        ip = request.form['ip']
        GEOIP = pygeoip.GeoIP(r"C:\Users\bhava\PycharmProjects\untitled\GeoIP.dat", pygeoip.MEMORY_CACHE)
        countryname=GEOIP.country_name_by_addr('176.148.229.178')
        print("Country is: " + countryname)
        print("Ip address is: " + ip)
        print("CVV address is: " + cvv)
        print("Credit card number is: " + credit_card_number)
        print("First name is: " + first_name)
        print("Last name is: " + last_name)

        # Machine Learning Algorithm------------------------------------------------------------------------------------
        test = df.loc[cc]
        test1 = test.iloc[0:30]
        test2 = test1.as_matrix(columns=None)
        l = test2.reshape(1,-1)

        filename = 'final_model.sav'
        loaded_model = joblib.load(filename, 'readwrite')
        result = loaded_model.predict(l)
        print(result)
        clas = int(result[0])
        # --------------------------------------------------------------------------------------------------------------

        if clas == 1:
            client = Client(account_sid, auth_token)
            call = client.calls.create(url=url1, to=tonum, from_='+12702142043', )
            print(call.sid)
            return render_template('maybe_fraud.html', lol=ip)
        else:
            return render_template('order_placed.html', lol=ip)
    else:
        print("No")


@app.route('/order', methods=['GET', 'POST'])
def orders():
    if request.method == "GET":
        return render_template('maybe_fraud.html')
    elif request.method == "POST":
        otp = str(request.form['otp'])
        if otp in a:
            print(1)
            return render_template('order_placed.html')
        else:
            print(2)
            return render_template('Definite_fraud.html')

# ----------------------------------------------------------------------------------------------------------------------


# Main Function---------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run(debug=True)

