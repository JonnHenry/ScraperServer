# -*- coding: utf-8 -*-
from re import sub
from typing import List
from urllib.parse import unquote
from threading import Thread
from wikipedia import summary,set_lang
from requests import get
from google_images_search import GoogleImagesSearch

images_urls = []
wiki_info = ""
set_lang("es")

def get_images(city:str,api_key:str,cx_key:str)-> List[str]:
    global images_urls
    gis = GoogleImagesSearch(api_key,cx_key)

    # define search params:
    _search_params = {
        'q': 'Cuenca Ecuador',
        'num': 4,
        'safe': 'off',
        'fileType': 'jpg|png',
        'imgType': 'photo',
        'imgSize': 'MEDIUM',
        'imgDominantColor': 'white',
        'rights': 'cc_publicdomain|cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived'
    }
    gis.search(search_params=_search_params)
    images_urls = [image.url for image in gis.results()]
    

def get_data_wiki(city:str)-> str:
    global wiki_info
    query = "{} Ecuador ciudad".format(city)
    data_without_clean = summary(query,sentences=2)
    text_cleaned = sub(r'\s+', ' ',data_without_clean)
    text_cleaned =sub(r'\[.*?\]', '', text_cleaned)
    wiki_info = sub("\n", ' ', text_cleaned)


def get_info(city:str,image_subscription_key:str,cx_key:str):
    try:
        global images_urls,wiki_info
        thread_images = Thread(target=get_images,args=(city,image_subscription_key,cx_key,),name="thread_images")
        thread_images.start()
        thread_wiki = Thread(target=get_data_wiki,args=(city,),name="thread_wiki")
        thread_wiki.start()

        thread_images.join()
        thread_wiki.join()
    except:
        return {"wiki": wiki_info,"imgs": images_urls}
    
    return {"wiki": wiki_info,"imgs": images_urls}

#Testing
#get_info("Cuenca","AIzaSyADjI1y3TPjyX3ex-ERV-0EBoHLmquvERo","5e4bcca5fce1a42dc")
#print(images_urls)