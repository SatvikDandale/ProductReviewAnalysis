import json 
from time import sleep
from dateutil import parser as dateparser
from selectorlib import Extractor
import requests 
import json 
from time import sleep
import csv
from dateutil import parser as dateparser
import pandas as pd
import requests
from lxml.html import fromstring
from bs4 import BeautifulSoup

# Purpose of this module
    # This module will extract the reviews from the given URL
    # Return a Pandas DataFrame of a specified format with these reviews.
    # 


# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('selectors.yml')

def scrape(url):
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
        "Accept-Encoding":"gzip, deflate", 
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
        "DNT":"1",
        "Connection":"close", 
        "Upgrade-Insecure-Requests":"1"}


    r = requests.get(url, headers=headers)
    
    # Download the page using requests
    print("Downloading %s\n"%url)

    # Simple check to check if page was blocked (Usually 503)

    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return

    # Pass the HTML of the page and create

    # with open('response.html', 'r', encoding='utf-8') as f:
    #     text = f.read()

    soup = BeautifulSoup(r.text, "lxml")
    
    try:
        name = soup.find("span", {"class": "a-size-large"})
        product_name = name.contents[0].strip()
    except:
        name = soup.find("a", {"class": "a-link-normal"})
        if name == None:
            product_name = "---------------"
        else:
            try:
                product_name = name.contents[0].strip()
            except:
                product_name = "---------------"
                
    return product_name, e.extract(r.text)

# url = "https://www.amazon.com/Nike-Womens-Reax-Running-Shoes/dp/B07ZPL752N/ref=cm_cr_arp_d_product_top?ie=UTF8"
# url = "https://www.amazon.com/Nike-Womens-Reax-Running-Shoes/product-reviews/B07ZPL752N/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"

def get_reviews(url):
    product_name, data = scrape(url)
    list_of_reviews = []
    if data:
        for r in data['reviews']:
            if len(r.keys()) == 3:  # If the URL is of ALL REVIEWS
                r["product"] = data["product_title"]
                r['url'] = url
                try:
                    r['rating'] = r['rating'].split(' out of')[0]
                except:
                    pass
                del r["date"]
                del r["variant"]
                del r["images"]
                del r["verified"]
                del r["url"]
                list_of_reviews.append(r)
            else: # Product landing page has URLS with direct data
                try:
                    r['rating'] = r['rating'].split(' out of')[0]
                except:
                    pass
                del r["date"]
                del r["variant"]
                del r["images"]
                del r["verified"]
                list_of_reviews.append(r)
        new_data = pd.DataFrame(list_of_reviews)
    else:
        raise ValueError("Failed to retireve data")
    new_data = new_data.dropna()
    return product_name, new_data

if __name__ == "__main__":
    url = "https://www.amazon.com/Moto-G7-Power-Unlocked-Warranty/dp/B07N9KQDVG/ref=psdc_2407749011_t3_B07N92347B"
    product_name, data = get_reviews(url)
    print(data.columns)