# -*- coding: utf-8 -*-
from mechanicalsoup import StatefulBrowser
from re import sub
from typing import List
from urllib.parse import unquote
import fake_useragent
from threading import Thread

location = './fake_useragent%s.json' % fake_useragent.VERSION
ua = fake_useragent.UserAgent(path=location)

images_urls = []
wiki_info = ""

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
    browser["q"] = '{} Ecuador'.format(city) 
    #submit/"click" search
    browser.submit_selected(btnName="btnG")
    
    page = browser.get_current_page()
    all_images = page.find_all('img')

    image_source: List = []
    cont:int = 0
    for image in all_images[:5]:
        if cont > 4:
            break
        image = image.get('src')
        if image.startswith('https'):    
            image_source.append(image)
            cont+=1

    images_urls = image_source


def get_data_wiki(city:str)-> str:
    global wiki_info
    browser =StatefulBrowser(
        soup_config={'features': 'lxml'},  # Use the lxml HTML parser
        raise_on_404=True,
        user_agent=ua.random
    )
    browser.open("https://www.google.com/") #Open link to the google Images
    #target the search input
    browser.select_form('form[action="/search"]') #The form used is 'q'
    #search for a term
    browser["q"] = "{} Ecuador wikipedia".format(city)
    #submit/"click" search
    browser.submit_selected(btnName="btnG")
    url:str = ""
    for link in browser.links():
        target = link.attrs['href']
        # Filter-out unrelated links and extract actual URL from Google's
        # click-tracking.
        if (target.startswith('/url?') and not target.startswith("/url?q=http://webcache.googleusercontent.com")):
            target = sub(r"^/url\?q=([^&]*)&.*", r"\1", target)
            url = unquote(target)
            break 
    
    browser.open(url)
    data_without_clean = browser.get_current_page().find('p').text
    text_cleaned = sub(r'\s+', ' ',data_without_clean)
    text_cleaned =sub(r'\[.*?\]', '', text_cleaned)
    wiki_info = sub("\n", '', text_cleaned)


def get_info(city:str):
    global images_urls,wiki_info
    thread_images = Thread(target=get_images,args=(city,),name="thread_images")
    thread_images.start()
    thread_wiki = Thread(target=get_data_wiki,args=(city,),name="thread_wiki")
    thread_wiki.start()

    thread_images.join()
    thread_wiki.join()

    return {"wiki": wiki_info,"imgs": images_urls}