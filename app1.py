import numpy as np
from flask import Flask, request, jsonify, render_template, make_response
from functools import wraps
from datetime import datetime
import pandas as pd
import pickle

app1 = Flask(__name__)

@app1.route('/')
def home():

    return render_template('index1.html')


@app1.route('/data',methods=['POST'])
def data():
    
    
    
    # Loading model to compare the results
    forecast = pickle.load(open('Forecast2.pkl','rb'))
    f1 =[x for x in request.form.values()]
    
    numpy_data = np.array(f1)
    dt = datetime.strptime(numpy_data[2], '%Y-%m-%d')
    
    
    d={'origin':[numpy_data[0]]*10,
    'dest':[numpy_data[1]]*10,
    'item':list(range(1,11)),
    'year':[dt.year]*10,
    'month':[dt.month]*10,
    'day':[dt.day]*10}
    dfs=pd.DataFrame(d)
    
    prdicted = forecast.predict(dfs)
    prd = np.round(prdicted, decimals=3)
    data={}
    waight=[]
    volume=[]
    Date=[]
    
    for i in range(0,10):
        waight.append(prd[i][0])
        Date.append(numpy_data[2])
        volume.append(prd[i][1])
    
  
    items = ['Commoditity',
                    'Domestic Express mail',
                    'Fast Moving Consumer Goods',
            'Flower telegraph and gift ',
            'International Letter Post',
            'International Parcel Post',
            'Ordinary mail',
            'Printed papers',
            'Telecommunications Device',
            'Television Device']
    data['items']= items
    data['waight']= waight
    data['volume']= volume
    data['Date'] = Date
    
    
    return render_template('data.html', data=data)

@app1.route('/data1', methods=['GET', 'POST'])
def data1():
    if request.method == 'POST':
        f1 =[x for x in request.form.values()]
        f2 =[x for x in request.form.values()]
        
        x ={}
        x['key1']=f1
        x['key2']=f2
        return render_template('data.html', data=x)

if __name__ == "__main__":
    app1.run(debug=True)