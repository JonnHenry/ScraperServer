# -*- coding: utf-8 -*-
from mechanicalsoup import StatefulBrowser
from re import sub
from typing import List
from urllib.parse import unquote
import fake_useragent


location = './fake_useragent%s.json' % fake_useragent.VERSION
ua = fake_useragent.UserAgent(path=location)

def get_images(city:str)-> List[str]:
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

    return image_source


def get_data_wiki(city:str)-> str:
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
    return sub("\n", ' ', text_cleaned)

#Testing
#print(get_images("Cuenca"))
#print(get_data_wiki("Cuenca"))

