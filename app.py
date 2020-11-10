import numpy as np
from flask import Flask, request, jsonify, render_template, make_response
from functools import wraps
from datetime import datetime
import pandas as pd
import pickle

app = Flask(__name__)

@app.route('/')
def home():

    return render_template('index.html')


@app.route('/predict',methods=['POST'])
def predict():
    
    # Loading model to compare the results
    forecast = pickle.load(open('Forecast2.pkl','rb'))
    f1 =[x for x in request.form.values()]
    
    numpy_data = np.array(f1)
    dt = datetime.strptime(numpy_data[3], '%Y-%m-%d')
    numpy_data[3] = dt.year
    newArray = np.append (numpy_data, [dt.month, dt.day])
    predictions = forecast.predict([newArray])
    final = np.round(predictions, decimals=3)
    
    return render_template('index.html', prediction_text ='Predicted waight {} kg and volume {} in3'.format(final[0][0],final[0][1]))


if __name__ == "__main__":
    app.run(debug=True)