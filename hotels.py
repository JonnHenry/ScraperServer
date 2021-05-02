# -*- coding: utf-8 -*-
import requests
from json import loads
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
    #New code: 1947a8bc22msh4fba3831b95a335p18879ejsn5748d4c16c85
    #Last code: 362591bdf2msh4ca334d27aa010bp11f3d0jsnd48789d729f4
    headers = {
        'x-rapidapi-key': "1947a8bc22msh4fba3831b95a335p18879ejsn5748d4c16c85",
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

    return hotels

#Testing
#print(get_hotels(lat="-2.90055",lng="-79.00453",checkIn="2021-01-27",checkOut="2021-01-28",rooms="1",sortOrder="BEST_SELLER"))

#{
#    "lat":"-2.90055",
#    "lng":"-79.00453",
#    "checkIn":"2021-01-27",
#    "checkOut":"2021-01-28",
#    "rooms":"1",
#    "sortOrder":"BEST_SELLER"
#}