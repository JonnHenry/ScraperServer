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
from dotenv import load_dotenv

#load the url of the database
load_dotenv('.env')

port = environ.get("PORT") #Variable used to development
app = Flask(__name__)
CORS(app)
app.config.from_object('config.ProdConfig')

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
    province = request.json['province']
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
    city = request.json['city']
    try:
        response = jsonify({
            "error": False,
            "data": get_info(city)
        })
        
    except:
        response = jsonify({
            "error": True,
            "data": []
        })
    return response


@app.route('/hotels',methods=['POST'])
def get_hotels_info():

    lat = request.json['lat']
    lng = request.json['lng']
    checkIn = request.json['checkIn']
    checkOut = request.json['checkOut']
    rooms = request.json['rooms']
    sortOrder = request.json['sortOrder'] if 'sortOrder' in request.json else None

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