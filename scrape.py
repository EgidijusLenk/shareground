import re
import requests
from bs4 import BeautifulSoup


def metadata_tags(url):

    
    

    r = requests.get(url)

    website = BeautifulSoup(r.text, "lxml")
    metatags= []
    for metatag in website.find_all('meta', property=re.compile(r'og\:')):
        metatags.append(str(metatag))  
        print(metatags)
    return metatags
