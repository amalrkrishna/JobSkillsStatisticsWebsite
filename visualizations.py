from scraper import scrape
import plotly
import os.path
import json

def scrape_and_save():
    data = scrape()
    with open('scrapped.json', 'w') as outfile:
        json.dump(data, outfile)

if os.path.isfile("scrapped.json") == True:
    print("File exists")  
    scrapped_data = json.load(open('scrapped.json'))
    print(scrapped_data)
else:
    scrape_and_save()
