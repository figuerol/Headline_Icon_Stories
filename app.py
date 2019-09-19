from flask import Flask, render_template, request, redirect
import os
import json
import requests
from requests_oauthlib import OAuth1
import webbrowser


app = Flask(__name__)

NYTKEY = os.getenv('KEY_NYT', default = 'SECRET_KEY')
NOUN_KEY=os.getenv('KEY_NOUN', default = 'SECRET_KEY')
NOUN_SECRET=os.getenv('SECRET_NOUN', default = 'SECRET_KEY')
app.vars={}

@app.route('/')
def main():
    return redirect('/index')


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template('index.html')
    else:
        app.vars['topic']=request.form['topic']

        app.vars['snippet']=request.form['snippet']
#getting data from NYT API  #WTforms package for WTforms
#if you specify a topic it will return headline else just return the icon associated to the snippet

        urlnyt= 'https://api.nytimes.com/svc/search/v2/articlesearch.json?q={}&api-key={}'.format(app.vars['topic'], NYTKEY)
        req = requests.get(urlnyt)
        first_article = req.json()['response']['docs'][0]
        lead_paragraph = first_article['lead_paragraph']
        snippet = first_article['snippet']

        try:
            headline=first_article['headline']['print_headline']

        except:
            headline=first_article['headline']['main']



#getting data from Noun project
        authnoun = OAuth1(NOUN_KEY, NOUN_SECRET)
        try:#We check wether there was an assigned topic as default
                app.vars['headline']=headline

                endpoint = 'http://api.thenounproject.com/icon/{}'.format(app.vars['topic'])

                response = requests.get(endpoint, auth=authnoun)
                app.vars['icon_url']=response.json()["icon"]["preview_url"]

        except: #if not we search for snippet
                keywords= app.vars['snippet']


                endpoint = 'http://api.thenounproject.com/icon/{}'.format(keywords)

                response = requests.get(endpoint, auth=authnoun)

                app.vars['icon_url']=response.json()["icon"]["preview_url"]
                print(app.vars['icon_url'])
        webbrowser.open(app.vars['icon_url'])



        return redirect('/icon')



@app.route('/icon')
def icon():
#if you specify a topic it will return headline and snippet, else just return the icon associated to the snippet
    icon_topic='None'
    icon_headline='None'
    icon_snippet='None'
    try:
        icon_snippet=app.vars['snippet']

    except:
        None
    try:
        icon_topic=app.vars['topic']

    except:
        None
    try:
        icon_headline=app.vars['headline']

    except:
        None


    return render_template('plot.html', icon_topic=icon_topic, icon_headline=icon_headline, icon_snippet=icon_snippet)#, resources=CDN.render())




@app.route('/plot')
def plot():
    plot=figure(x_axis_type="datetime")

    for i,box in enumerate(app.vars['feature']):
        print(box)
        plot.line(pd.to_datetime(app.vars['data']['Date']),app.vars['data'][box], color= palette[i], legend=box, line_width=1)

    return json.dumps(json_item(plot, "myplot"))



if __name__ == '__main__':
  app.run(debug = True)
