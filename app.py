# -*- coding: utf-8 -*-
#External libraries
from flask import Flask, jsonify, request
from flask_cors import CORS

#Own
from dbCities import Map
from hotels import get_hotels
from scrapping import get_info
import config

#enviroment
from os import environ
from os.path import join, dirname
from dotenv import load_dotenv

#load the url of the database
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

port = environ.get("PORT") #Variable used to development CX_KEY
image_subscription_key = environ.get("IMG_KEY")
cx_key = environ.get("CX_KEY")
app = Flask(__name__)
app.config.from_object('config.ProdConfig')
CORS(app)

#Get data from database

database = Map(uri_db = environ.get("BD_URL"))

@app.route('/', methods=['GET'])
def ping():
    return "Server is running!"

@app.route('/provinces',methods=['GET'])
def get_provinces():
    try:
        response = jsonify({
            "error": False,
            "data": database.get_provinces()
        })
        
    except:
        response = jsonify({
            "error": True,
            "data": []
        })
    return response

@app.route('/cities',methods=['GET'])
def get_cities():
    province = request.args.get('province',type = str)
    try:
        response = jsonify({
            "error": False,
            "data": database.get_cities(province)
        })
        
    except:
        response = jsonify({
            "error": True,
            "data": []
        })
    return response


@app.route('/info_city',methods=['GET'])
def get_information():
    city = request.args.get('city',type = str)
    try:
        response = jsonify({
            "error": False,
            "data": get_info(city,image_subscription_key,cx_key)
        })
        
    except:
        response = jsonify({
            "error": True,
            "data": []
        })
    return response


@app.route('/hotels',methods=['GET'])
def get_hotels_info():

    lat =  request.args.get('lat',type = str)
    lng = request.args.get('lng',type = str)
    checkIn = request.args.get('checkIn',type = str)
    checkOut = request.args.get('checkOut',type = str)
    rooms = request.args.get('rooms',type = str)
    sortOrder = request.args.get('sortOrder',type = str) if 'sortOrder' in request.args else None

    try:
        response = jsonify({
            "error": False,
            "data": get_hotels(lat,lng,checkIn,checkOut,rooms,sortOrder)
        })
        
    except:
        response = jsonify({
            "error": True,
            "data": []
        })
    return response


if __name__ == '__main__':
    app.run()