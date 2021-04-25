# -*- coding: utf-8 -*-
from pymongo import MongoClient
from typing import List
from json import dumps

class Map:
    def __init__(self, uri_db):
        self.__collection_cities = MongoClient(uri_db).web_avanzada.cities

    def get_provinces(self)-> List[str]:
        return self.__collection_cities.find().distinct('admin_name')

    def get_cities(self,province:str)->List[dict[str]]:
        return [result for result in self.__collection_cities.find({"admin_name": province},{"_id":0,'admin_name':0})]

#Testing
#map = Map(uri_db="mongodb+srv://ManageData:admin@cluster0.aifq0.mongodb.net/test")
#print(dumps(map.get_provinces()))
#print(map.get_cities("Azuay"))
