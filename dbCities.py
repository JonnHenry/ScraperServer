from pymongo import MongoClient
from typing import List
import json

class MapCities():
    def __init__(self):
        self.__collection_cities = MongoClient("mongodb+srv://ManageData:admin@cluster0.aifq0.mongodb.net/test").web_avanzada.cities

    def get_provinces(self)-> List[str]:
        return self.__collection_cities.find().distinct('admin_name')

    def get_city(self,province:str)->List[dict[str]]:
        return json.dumps([result for result in self.__collection_cities.find({"admin_name": province},{"_id":0,'admin_name':0})])

cities = MapCities()
print(cities.get_provinces())
#print(get_provinces())
#print(get_cities("Azuay"))
