import requests
import configparser
from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/')
def weather_dashboard():
    return render_template("home.html")


def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']


def get_weather_results(zip_code, country_code, api_key):
    api_url = "http://api.openweathermap.org/data/2.5/weather?zip={},{}&units=metric&appid={}".format(zip_code, country_code, api_key)
    print(api_url)
    r = requests.get(api_url)
    return r.json()

'''ini files in python is a very easy way to store configuration so we create one'''


@app.route('/results', methods=['POST'])
def render_results():
    zip_code = request.form['zipCode']
    country_code = request.form['countryCode']
#check out the json file for this variables
    api_key = get_api_key()
    data = get_weather_results(zip_code, country_code, api_key)
    temp = "{0:.2f}".format(data["main"]["temp"])
    feels_like = "{0:.2f}".format(data["main"]["feels_like"])
    weather = data["weather"][0]["main"]         #the weather in json file is a list not a dict so we accessed the first value
    location = data["name"]
    
#{0:.2f} thsi means format this data as a float as two decimal places only
    
    return render_template('results.html', 
                           location=location, temp=temp, 
                           feels_like=feels_like, weather=weather)



if __name__ == '__main__':
    app.run(debug=True)
    




    
