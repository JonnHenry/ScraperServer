# -*- coding: utf-8 -*-
from flask import Flask
from dbCities import get_provinces,get_cities
from hotels import get_hotels
from scrapping import get_images,get_data_wiki

#name of the app
app = Flask(__main__)

@app.route('/')
def hello_world():
    return 'Hello, World!'