import numpy as np
from flask import Flask, request, jsonify, render_template, make_response
from functools import wraps
from datetime import datetime
import pandas as pd
import pickle
from datetime import datetime
from datetime import date, timedelta

app2 = Flask(__name__)


def auth_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        auth = request.authorization
        if auth and auth.username == 'usr1' and auth.password == '123':
            return f(*args, **kwargs)
        
        return make_response('could not varify',401,{'WWW-Authenticate' : 'Basic realm = "Login Required"'})

    return decorated   


@app2.route('/')
@auth_required
def home():

    return render_template('index2.html')


@app2.route('/data2',methods=['POST'])
@auth_required
def data2():
    
    
    
    # Loading model to compare the results
    forecast = pickle.load(open('Forecast2.pkl','rb'))
    f1 =[x for x in request.form.values()]
    
    numpy_data = np.array(f1)
    
    origin_replace ={1: 'Bình Dương ',
                     2: 'Bình Phước ',
                     3: 'Bình Định ',
                     4: 'Bắc Giang ',
                     5: 'Bắc Kạn ',
                     6: 'Bắc Ninh ',
                     7: 'Cao Bằng ',
                     8: 'Cà Mau ',
                     9: 'Gia Lai ',
                     10: 'Hà Giang ',
                     11: 'Hà Nam ',
                     12: 'Hà Tĩnh ',
                     13: 'Hải Dương ',
                     14: 'Hải Phòng ',
                     15: 'Hoà Bình ',
                     16: 'Khánh Hoà ',
                     17: 'Đà Nẵng ',
                     18: 'Đắk Lăk '}
    dest_replace ={1: 'Kon Tum ',
                   2: 'Lào Cai ',
                   3: 'Lạng Sơn ',
                   4: 'Long An ',
                   5: 'Nam Định ',
                   6: 'Ninh Bình ',
                   7: 'Phú Thọ ',
                   8: 'Quảng Bình ',
                   9: 'Quảng Nam ',
                   10: 'Quảng Ngãi ',
                   11: 'Quảng Ninh ',
                   12: 'Quảng Trị ',
                   13: 'Sóc Trăng ',
                   14: 'Sơn La ',
                   15: 'Thanh Hoá ',
                   16: 'Thái Bình ',
                   17: 'Trà Vinh ',
                   18: 'Vĩnh Long '}
    
    orig=[]
    des=[]
    v1= int(numpy_data[0])
    v2= int(numpy_data[1])
    for i in range(1,len(origin_replace)+1):
        if v1 == i :
            orig = origin_replace[i]
    
        if v2 == i :
            des = dest_replace[i]
    
    dt1 = datetime.strptime(numpy_data[2], '%Y-%m-%d')
    dt2 = datetime.strptime(numpy_data[3], '%Y-%m-%d')

    sdate = date(dt1.year, dt1.month, dt1.day)   # start date
    edate = date(dt2.year, dt2.month, dt2.day)   # end date

    delta = edate - sdate  

    a= len(range(delta.days+1))
    ex = {}
    result = {}
    for i in range(delta.days + 1):
        day =str(sdate + timedelta(days=i))
    
        dt = datetime.strptime(day, '%Y-%m-%d')
    
        d={'origin':[numpy_data[0]]*10,
           'dest':[numpy_data[1]]*10,
           'item':list(range(1,11)),
           'year':[dt.year]*10,
           'month':[dt.month]*10,
           'day':[dt.day]*10}
    
    
        for key in (d.keys()):
            if key in d:
                result.setdefault(key, []).extend(d[key])
    
    dfs1 = pd.DataFrame(result)

    prdicted = forecast.predict(dfs1)
    prd = np.round(prdicted, decimals=3)
    
    
    dfs1['Pred_date']=pd.to_datetime(dfs1[['year','month','day']])
    
    dfs1 = dfs1.drop(['year','month','day','origin','dest'], axis =1) 
    
    item_replace= {1: 'Commoditity',
                   2: 'Domestic Express mail',
                   3: 'Fast Moving Consumer Goods',
                   4: 'Flower telegraph and gift ',
                   5: 'International Letter Post',
                   6: 'International Parcel Post',
                   7: 'Ordinary mail',
                   8: 'Printed papers',
                   9: 'Telecommunications Device',
                   10: 'Television Device'}
    
    dfs1.replace(item_replace, inplace=True)
    
    
    waight=[]
    volume=[]
    origin=[]
    dest=[]
    for i in range(len(prd)):
        waight.append(prd[i][0])
        volume.append(prd[i][1])
        origin.append(orig)
        dest.append(des)
        
    dfs1['origin'] = origin
    dfs1['destination'] = dest
    dfs1['predected waight']= waight
    dfs1['predected volume']= volume
    
    
    return render_template('data2.html', data=dfs1.to_dict())

@app2.route('/data1', methods=['GET', 'POST'])
def data1():
    if request.method == 'POST':
        f1 =[x for x in request.form.values()]
        f2 =[x for x in request.form.values()]
        
        x ={}
        x['key1']=f1
        x['key2']=f2
        return render_template('data2.html', data=x)

if __name__ == "__main__":
    app2.run(debug=True)