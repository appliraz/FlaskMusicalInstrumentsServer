import variablesService as vs
from .websites_logos.base64_logos import base64_imgs

website_key = "KLEY-ZEMER"
hebrew_name = "כלי זמר"
english_name = "Kley Zemer"
base_url = "https://www.kley-zemer.co.il/" # make sure this ends with '/'
item_tag = "div"
item_class = "border_item"
name_tag = "h2"
name_class = None
upperprice_tag = "div" 
upperprice_class = "oldprice"
lowerprice_tag = "div"
lowerprice_class = "saleprice"
lowerprice_css_class = "div.saleprice"
img_source = base64_imgs['kley-zemer']
#"https://drive.google.com/uc?export=view&id=1_gc_svy_iC4vyP14blSfJ5lzx6NKxFnK"

method = vs.pagination_method
main_html_tag = None
main_html_class = None

# try to scrap the pagination bar:
pagination_container_tag = "ul"
pagination_container_class = "pagination"
pagination_item_tag = "li"
pagination_item_class = None

paginate = vs.url_query_indicator + "bscrp=" + vs.page_index

""" When you finished don't forget to add the new website you've configs to websites_dict """

# Don't change the following

website_configs = vs.getWebsiteConfigs()
website_configs[vs.website_url] = base_url
website_configs[vs.product_element]['tag'] = item_tag
website_configs[vs.product_element]['class'] = item_class
website_configs[vs.product_name]['tag'] = name_tag
website_configs[vs.product_name]['class'] = name_class
website_configs[vs.product_list_price]['tag'] = upperprice_tag
website_configs[vs.product_list_price]['class'] = upperprice_class
website_configs[vs.product_price]['tag'] = lowerprice_tag
website_configs[vs.product_price]['class'] = lowerprice_class
website_configs[vs.product_price]['css_class'] = lowerprice_css_class
website_configs[vs.pagination]['container']['tag'] =  pagination_container_tag
website_configs[vs.pagination]['container']['class'] =  pagination_container_class
website_configs[vs.pagination]['item']['tag'] = pagination_item_tag
website_configs[vs.pagination]['item']['class'] = pagination_item_class
website_configs[vs.pagination]['indicator'] = paginate
website_configs[vs.hebrew_name] = hebrew_name
website_configs[vs.english_name] = english_name
website_configs[vs.logo_src] = img_source
website_configs[vs.method] = method
website_configs[vs.main_html_element]['tag'] = main_html_tag
website_configs[vs.main_html_element]['class'] = main_html_class
