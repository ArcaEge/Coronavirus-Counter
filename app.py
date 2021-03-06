import requests
from flask import Flask, render_template, redirect, send_file, Markup, request

app = Flask(__name__)

all = requests.get('https://corona.lmao.ninja/v2/all')
countries = requests.get('https://corona.lmao.ninja/v2/countries')
a = countries.json()


cases_all = all.json()['cases']
deaths_all = all.json()['deaths']
recovered_all = all.json()['recovered']


@app.route('/')
def home():
    return render_template('map.html')


@app.route('/news')
def news():
    request = requests.get("https://content.guardianapis.com/search?show-fields=all&page-size=100&q=coronavirus&api-key=a7daa1b5-293f-44dc-b5d2-81e552e1a7d7")
    JSON = request.json()
    to_return = JSON["response"]["results"]
    nws = []
    # print(to_return[9].get("headline"))
    for news in to_return:
        nw = {
        "webUrl": news["webUrl"],
        "headline": news["fields"].get("headline"),
        "byline": news["fields"].get("byline"),
        "thumbnail": news["fields"].get("thumbnail"),
        "trailText": Markup(news["fields"].get("trailText")),
        "sectionName": news["sectionName"],
        "id": news["id"],
        "body": Markup(news["fields"].get("body").replace("h2", "h4").replace("h1", "h4"))
        }
        nws.append(nw)
    return render_template('news.html', news=nws)


@app.route('/newscontent', methods=['GET'])
def new():
    ID = request.args.get("id")
    urll = "https://content.guardianapis.com/{}?show-fields=all&api-key=a7daa1b5-293f-44dc-b5d2-81e552e1a7d7".format(ID)
    requestAPI = requests.get(urll)

    JSON = requestAPI.json()
    to_return = JSON.get("response")
    content = to_return.get("content")
    fields = content.get("fields")
    nw = {
    "webUrl": content.get("webUrl"),
    "sectionName": content.get("sectionName"),
    "headline": fields.get("headline"),
    "byline": fields.get("byline"),
    "thumbnail": fields.get("thumbnail"),
    "trailText": Markup(fields.get("trailText")),
    "body": Markup(fields.get("body").replace("h2", "h4").replace("h1", "h3"))
    }
    return render_template('newscont.html', news=nw)


@app.route('/pngimages')
def images():
    return send_file('Github.png', mimetype='image/png')


@app.route('/mapjavascript')
def js():
    return send_file('map.js', mimetype='text/javascript')


@app.route('/pngimages2')
def images2():
    return send_file('GithubLight.png', mimetype='image/png')


@app.route('/icologo')
def logo():
    return send_file('Logo.ico', mimetype='image/x-icon')


@app.route('/worldwide')
def world():
    cases_formatted = '{:,d}'.format(cases_all)
    deaths_formatted = '{:,d}'.format(deaths_all)
    recovered_formatted = '{:,d}'.format(recovered_all)
    return render_template('worldwide.html', cases=cases_formatted, deaths=deaths_formatted, recovered=recovered_formatted)


@app.route('/countries')
def country():
    return render_template('countries.html', a=a)


@app.route('/countries/<string:name_of_country>')
def country_details(name_of_country):
    b = 0
    for i in countries.json():
        if (i['country'] == name_of_country):
            b = i
    if b == 0:
        return redirect('/countries')
    else:
        return render_template('country.html', b=b)


if __name__ == '__main__':
    print(0)
    app.run()
