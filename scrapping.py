# -*- coding: utf-8 -*-
from re import sub
from typing import List
from urllib.parse import unquote
from threading import Thread
from wikipedia import summary,set_lang
from requests import get

images_urls = []
wiki_info = ""
set_lang("es")

def get_images(city:str,image_subscription_key:str)-> List[str]:
    global images_urls
    search_url = "https://api.bing.microsoft.com/v7.0/images/search"
    search_term = "{} ecuador".format(city)

    headers = {"Ocp-Apim-Subscription-Key" : image_subscription_key}
    params  = {"q": search_term, "license": "public", "imageType": "photo"}
    response = get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    images_urls = [img["thumbnailUrl"] for img in search_results["value"][:4]]


def get_data_wiki(city:str)-> str:
    global wiki_info
    query = "{} Ecuador ciudad".format(city)
    data_without_clean = summary(query,sentences=2)
    text_cleaned = sub(r'\s+', ' ',data_without_clean)
    text_cleaned =sub(r'\[.*?\]', '', text_cleaned)
    wiki_info = sub("\n", ' ', text_cleaned)


def get_info(city:str,image_subscription_key:str):
    try:
        global images_urls,wiki_info
        thread_images = Thread(target=get_images,args=(city,image_subscription_key,),name="thread_images")
        thread_images.start()
        thread_wiki = Thread(target=get_data_wiki,args=(city,),name="thread_wiki")
        thread_wiki.start()

        thread_images.join()
        thread_wiki.join()
    except:
        return {"wiki": wiki_info,"imgs": images_urls}
    
    return {"wiki": wiki_info,"imgs": images_urls}

#Testing
#get_images("Cuenca","a50938067fe9431ea31c8377e4ea6790")
#print(images_urls)