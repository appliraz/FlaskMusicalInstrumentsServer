""" Add parent package to project path """
import sys
import os
from os.path import dirname, abspath
current_dir = dirname(abspath(__file__))
parent_dir = dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(parent_dir)


#print(sys.path)

""" Import extrnal packages """
from bs4 import BeautifulSoup
import requests


""" Import project modules """
from configurations import variablesService as vs
import SoupParser


def getTextToScrap(url: str, first_page: int, website_configs: dict) -> str:
    # page number yelds url yelds responds yelds text to scrap 
    session = requests.Session()
    last_page = getLastPage(session, url, website_configs)
    scrap_text = ""
    for page in range(first_page, last_page+1):
        print(f"page = {page}")
        current_url = getNextUrl(url, page)
        print(f"current url = {current_url}")
        res = requestUrl(session, current_url)
        if res is None or not res.status_code == 200:
            print(f"requests to url {current_url} failed with status code = {res.status_code}")
            break
        page_text = getTextFromResponse(res)
        if not page_text or areNoItemsInPage(page_text, website_configs):
            break
        scrap_text += page_text
    session.close()
    return scrap_text



def areNoItemsInPage(page_text: str, website_configs: dict) -> bool:
    items_tag = website_configs[vs.product_element]['tag']
    items_class = website_configs[vs.product_element]['class']
    item = BeautifulSoup(page_text, 'html.parser').find(items_tag, class_ = items_class)
    return item is None




def getSoup(url: str, first_page: int, website_configs: dict):
    scrap_text = getTextToScrap(url, first_page, website_configs)
    if not scrap_text:
        raise Exception("Something went wrong and no text was found")
    try:
        full_bowl_of_soup = BeautifulSoup(scrap_text, 'html.parser')
    except Exception as e:
        print(e)
        full_bowl_of_soup = None
    return full_bowl_of_soup


def initSoup(url: str, website_configs: dict):
    paginate_url, first_page = paginateUrl(url, website_configs)
    print("\n\tpaginated")
    print(paginate_url)
    soup = getSoup(paginate_url, first_page, website_configs)
    return soup




""" Utility Pagination Functions """

def paginateUrl(url: str, website_configs: dict):
    print(website_configs)
    website_pagination = website_configs[vs.pagination]['indicator']
    if vs.page_index not in website_pagination:
        raise Exception(f"The configuration for website_pagination is invalid\nThe website_pagination has to contain {vs.page_index}, found: {website_pagination}")
    if isPaginationApplied(url, website_pagination):
        fixed_url, first_page = addPageIndexToUrl(url, website_pagination)
        return fixed_url, first_page
    if vs.url_query_indicator in website_pagination:
        paginate_url = appendQueryToUrl(url, website_pagination)
        first_page = 1
        return paginate_url, first_page
    if vs.extension_indicator in website_pagination:
        paginate_url = appendExtensionToUrl(url, website_pagination)
        first_page = 1
        return paginate_url, first_page
    raise Exception(f"The configuration for website_pagination is invalid\nExcpected to have {vs.url_query_indicator} or {vs.extension_indicator} but none were found in {website_pagination}")


def appendQueryToUrl(url: str, website_pagination: str):
    if vs.url_query_indicator in url:
        website_pagination = website_pagination.replace(vs.url_query_indicator, vs.url_param)
    url = removeLastExtensionSign(url)
    url += website_pagination
    return url

def removeLastExtensionSign(url: str):
    if url[-1] == vs.extension_indicator:
        url = url[:-1]
    return url

def addExtensionAtIndex(url: str, extension: str, index: int):
    left_url = url[:index]
    right_url = url[index:]
    left_url = removeLastExtensionSign(left_url)
    url = left_url + extension + right_url
    return url

def appendExtensionToUrl(url: str, website_pagination: str):
    if vs.url_query_indicator in url:
        query_index = url.find(vs.url_query_indicator)
        url = addExtensionAtIndex(url, extension=website_pagination, index=query_index)
    else:
        url = removeLastExtensionSign(url)
        url += website_pagination
    return url

def getNextUrl(url: str, page: int):
    next_url = url.replace(vs.page_index, str(page))
    return next_url

def isPaginationApplied(url: str, pagination: str):
    indicator = pagination.replace(vs.page_index, "")
    return indicator in url or indicator[1:] in url

def addPageIndexToUrl(url: str, website_pagination: str):
    page_index = vs.page_index
    paginate = website_pagination.replace(page_index, "")
    index = url.find(paginate)
    left_url = url[:index+len(paginate)]
    right_url = url[len(left_url):]
    end_of_page_number_index = getNextSignIndex(right_url)
    current_page = right_url[:end_of_page_number_index]
    right_url = right_url[end_of_page_number_index:]
    full_url = left_url + vs.page_index + right_url
    return (full_url, int(current_page))

def getNextSignIndex(url: str):
    signs = [vs.url_query_indicator, vs.extension_indicator, ",", vs.url_param]
    next_index = len(url)
    for sign in signs:
        index =  url.find(sign)
        if index != -1 and index < next_index:
            next_index = index
    return next_index

def getTextFromResponse(response):
    try:           
        text = response.text
        return text
    except Exception as e:
        print("could not get text from response")
        print(e)
        return ""
    

    


""" Requests function"""

def requestUrl(session: requests.Session, url: str) -> requests.Response:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}
    try:
        res = session.get(url, headers=headers)
        return res
    except Exception as e:
        print("failed in request url")
        print(e)
        return None


def getLastPage(session: requests.Session, url: str, website_configs: dict) -> int:
    first_page_res = session.get(url)
    if first_page_res.status_code != 200:
        return vs.max_pages
    try:
        page_soup = BeautifulSoup(first_page_res.text, "html.parser")
        last_page = SoupParser.getLastPage(page_soup, website_configs)
        last_page = last_page if last_page < vs.max_pages else vs.max_pages
        print(f"\nlast page is : {last_page}")
        return last_page
    except Exception as e:
        print(e)
        return vs.max_pages
    
    





















def getLastPageFromText(page_text: str, website_configs:dict):
    try:
        page_soup = BeautifulSoup(page_text, "html.parser")
        last_page = SoupParser.getLastPage(page_soup, website_configs)
        print(f"\nlast page is : {last_page}")
        return last_page
    except Exception as e:
        print(e)
        return vs.max_pages
    















def isStatusCodeOK(url):
    status_code = requests.get(url).status_code
    if status_code == 403:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}
        status_code = requests.get(url, headers=headers).status_code
    print(f"status code is {status_code}")
    return status_code == 200