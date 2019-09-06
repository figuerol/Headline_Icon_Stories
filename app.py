from flask import Flask, render_template, request, redirect
from bokeh.resources import CDN
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.embed import json_item
from bokeh.resources import INLINE
# from bokeh.templates import RESOURCES
from bokeh.util.string import encode_utf8
from bokeh.util.browser import  view
import pandas as pd

import quandl
import os
import json
import requests
from bokeh.resources import INLINE



app = Flask(__name__)

SECRET_KEY=os.getenv('SECRET_KEY', default = 'SECRET_KEY')
app.vars={}

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template('index.html')
    else:
        app.vars['feature']= request.form.getlist('feature')
        app.vars['ticker']=request.form['ticker']
#getting data from API
        url= 'https://www.quandl.com/api/v3/datasets/WIKI/' + app.vars['ticker'] + '/data.json?limit=5&api_key='+SECRET_KEY
        req = requests.get(url)
        data = req.json()['dataset_data']['data']
        columns= req.json()['dataset_data']['column_names']

        app.vars['data']=pd.DataFrame(data, columns=columns)

        return redirect('/bok')


@app.route('/bok')
def bok():

    return render_template('plot.html', ticker=app.vars['ticker'], resources=CDN.render())




@app.route('/plot')
def plot():
    plot=figure()
    for box in app.vars['feature']:
        print(box)
        plot.line(pd.to_datetime(app.vars['data']['Date']),app.vars['data'][box], line_width=1)
    return json.dumps(json_item(plot, "myplot"))

@app.route('/about')
def about():
  return render_template('about.html')

if __name__ == '__main__':
  app.run()
