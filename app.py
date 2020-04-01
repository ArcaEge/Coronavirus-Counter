import requests
from flask import Flask, render_template, redirect, send_file

app = Flask(__name__)

all = requests.get('https://coronavirus-19-api.herokuapp.com/all')
countries = requests.get('https://coronavirus-19-api.herokuapp.com/countries')
a = countries.json()


cases_all = all.json()['cases']
deaths_all = all.json()['deaths']
recovered_all = all.json()['recovered']


@app.route('/')
def home():
    return render_template('map.html')


@app.route('/pngimages')
def images():
    return send_file('Github.png', mimetype='image/png')


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
