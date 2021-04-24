# -*- coding: utf-8 -*-
import requests
from json import dumps,loads
from typing import List

def get_hotels(lat:str,lng:str,checkIn:str,checkOut:str,rooms:str,sortOrder:str="NO_SORT")-> List[dict[str]]:
    url = "https://hotels-com-free.p.rapidapi.com/srle/listing/v1/brands/hotels.com"
    querystring = {
        "lat": lat,
        "lon": lng,
        "checkIn": checkIn,
        "checkOut": checkOut,
        "rooms": rooms,
        "locale":"en_US",
        "currency":"USD",
        "pageNumber":"1",
        "sortOrder": sortOrder
        }

    headers = {
        'x-rapidapi-key': "362591bdf2msh4ca334d27aa010bp11f3d0jsnd48789d729f4",
        'x-rapidapi-host': "hotels-com-free.p.rapidapi.com"
        }
    hotels:List = []
    response = loads(requests.request("GET", url, headers=headers, params=querystring).text)["data"]["body"]["searchResults"]["results"]
    for row in response:
        hotel = {}
        hotel["name"] = row["name"] if "name" in row else None
        hotel["cost"] = row["ratePlan"]["price"]["exactCurrent"] if "ratePlan" in row else None
        hotel["img"] = row["optimizedThumbUrls"]["srpDesktop"] if "optimizedThumbUrls" in row else None
        hotel["address"] = row["address"]["streetAddress"] if "address" in row else None
        hotels.append(hotel)

    return dumps(hotels)

#print(get_hotels(lat="-2.90055",lng="-79.00453",checkIn="2021-01-27",checkOut="2021-01-28",rooms="1",sortOrder="BEST_SELLER"))
