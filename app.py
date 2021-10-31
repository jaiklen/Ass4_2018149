from flask import Flask
from flask import request
from flask import render_template
from bokeh.embed import components
from bokeh.plotting import figure
import pandas as pd
import numpy as np
import datetime
app = Flask(__name__)

@app.route('/',methods = ['GET','POST'])
def index():
    #table = pd.read_csv('NIFTY50_all.csv')
    table = pd.read_csv('AXISBANK.csv')
    stock_symbols = table.Symbol.unique()
        
    if request.method == 'GET':
        p = figure(width=400, height=400,sizing_mode="stretch_width")
        p.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=20, color="navy", alpha=0.5)
        demo_script_code,chart_code = components(p)
        return render_template('view.html',stock_symbol_names=stock_symbols,chart_code = chart_code,demo_script_code = demo_script_code)
    elif request.method =='POST':
        print("post request made")
        stock_symbols = request.form['stock']
        Date_b = request.form['Date_b']
        Date_e = request.form['Date_e']
        period = request.form['Period']
        amount = request.form['Amount']
        
        return render_template('view.html')
    
    
def compute():
    stock = input("Pick a stock: ")+".csv"
    Date_b = input("Pick a beginning date: ")
    Date_e = input("Pick an end date: ")
    Period = input("Pick a Period: ")
    Amount = int(input("Pick an amount: "))

    frequency={'weekly':"W","monthly":"M","quarterly":"3 M"}
    freq=frequency[Period]
    
    stock_data=pd.read_csv(stock)
    stock_data['Date']=pd.to_datetime(stock_data['Date'])
    stock_data.set_index('Date',inplace=True)
    dts = pd.Series(pd.date_range(stock_data.index[0],stock_data.index[-1],freq=freq,closed='left'))
    nearest_dates=dts.apply(lambda dt:stock_data.index[stock_data.index.get_loc(dt,method="nearest")])
    pd.DataFrame(np.c_[dts,nearest_dates],columns=['original','closest'])
    
    investment_data=pd.DataFrame(stock_data.loc[nearest_dates,'Open']).rename(columns={'Open':'Price'})
    
    tot_units=0
    for i,row in investment_data.iterrows():
        tot_units+=Amount/row['Price']
        investment_data.loc[i,'Units']=tot_units
        investment_data.loc[i,'Wealth']=tot_units*row['Price']

    p=figure(width=900,height=700,x_axis_type='datetime',x_axis_label='Date',y_axis_label='Stock units')
    p.line(investment_data.index,investment_data['Wealth'],line_width=2)
    p.show()


if __name__ == "__main__":
    app.run(debug=True, port=5000)