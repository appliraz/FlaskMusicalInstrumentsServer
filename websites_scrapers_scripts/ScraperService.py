""" Add parent package to project path """
import sys
import os
from os.path import dirname, abspath

parent_dir = dirname(dirname(abspath(__file__)))
sys.path.append(parent_dir)

from configurations.websites_configs.websites_dict import websites_dict
from configurations import variablesService as vs
from scrap_scripts import SoupParser, PaginationScrap

def extractDomain(url: str):
    domain = url.replace("https://", "").replace("www.", "")
    return domain

def getWebsiteKey(url):
    for key, website_configs in websites_dict.items():
        domain = extractDomain(website_configs[vs.website_url])
        if domain in url:
            return key
    return None

def scrap(url):
    key = getWebsiteKey(url)
    print(f"key is {key}\n\n\n\n\n")
    website_configs = websites_dict[key]
    soup = PaginationScrap.initSoup(url, website_configs)
    print("returned with soup")
    data = SoupParser.parseSoup(soup, website_configs)
    return data

