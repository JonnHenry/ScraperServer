# -*- coding: utf-8 -*-

from pymongo import MongoClient
from typing import List
import json

__collection_cities = MongoClient("mongodb+srv://ManageData:admin@cluster0.aifq0.mongodb.net/test").web_avanzada.cities

def get_provinces()-> List[str]:
    return __collection_cities.find().distinct('admin_name')

def get_cities(province:str)->List[dict[str]]:
    return json.dumps([result for result in __collection_cities.find({"admin_name": province},{"_id":0,'admin_name':0})])


#Testing
#print(get_provinces())
#print(get_cities("Azuay"))
