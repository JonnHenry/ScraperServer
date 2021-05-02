# -*- coding: utf-8 -*-
from mechanicalsoup import StatefulBrowser
from re import sub
from typing import List
from urllib.parse import unquote
import fake_useragent
from threading import Thread
from wikipedia import summary,set_lang
from time import sleep

location = './fake_useragent%s.json' % fake_useragent.VERSION
ua = fake_useragent.UserAgent(path=location)

images_urls = []
wiki_info = ""
set_lang("es")

def get_images(city:str)-> List[str]:
    global images_urls
    browser = StatefulBrowser(
        soup_config={'features': 'lxml'},  # Use the lxml HTML parser
        raise_on_404=True,
        user_agent=ua.random
    )
    browser.open("https://images.google.com/") #Open link to the google Images
    #target the search input
    browser.select_form() #The form used is 'q'
    #search for a term
    browser["q"] = '{} Ecuador high definition'.format(city) 
    sleep(2)
    #submit/"click" search
    browser.submit_selected(btnName="btnG")
    
    page = browser.get_current_page()
    all_images = page.find_all('img')

    image_source: List = []
    cont:int = 1
    for image in all_images:
        if cont > 4:
            break
        image = image.get('src')
        if image.startswith('https'):    
            image_source.append(image)
            cont+=1

    images_urls = image_source


def get_data_wiki(city:str)-> str:
    global wiki_info
    query = "{} Ecuador ".format(city)
    data_without_clean = summary(query,sentences=2)
    text_cleaned = sub(r'\s+', ' ',data_without_clean)
    text_cleaned =sub(r'\[.*?\]', '', text_cleaned)
    wiki_info = sub("\n", ' ', text_cleaned)


def get_info(city:str):
    global images_urls,wiki_info
    thread_images = Thread(target=get_images,args=(city,),name="thread_images")
    thread_images.start()
    thread_wiki = Thread(target=get_data_wiki,args=(city,),name="thread_wiki")
    thread_wiki.start()

    thread_images.join()
    thread_wiki.join()

    return {"wiki": wiki_info,"imgs": images_urls}

#Testing
#print(get_info("Cuenca"))