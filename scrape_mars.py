from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import requests
import config

def scrape():
    ### NASA Mars News ###
    html = urlopen(config.NASA_Mars_News_url)
    soup = BeautifulSoup(html, 'lxml')
    News_Description = soup.findAll("div", {"class": "rollover_description_inner"})
    News_Title = soup.findAll("div", {"class": "content_title"})
    Mars_News = pd.DataFrame(columns=['news_title', 'news_p'])
    for i in range(len(News_Description)):
        Title = News_Title[i].get_text().replace('\n\n', '')
        Desc = News_Description[i].get_text().replace('\n', '')
        df = pd.DataFrame({'news_title': [Title], 'news_p': [Desc]})
        Mars_News = Mars_News.append(df).reset_index(drop=True)

    ### JPL Mars Space Images - Featured Image ###
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    res = requests.get(url)
    soup_table = BeautifulSoup(res.content, 'html.parser')
    # print(soup_table)
    hemisphere_AllInfo = soup_table.findAll("a", {"class": "button fancybox"})
    featured_image = {}
    for i in hemisphere_AllInfo:
        image_loc = i.get('data-fancybox-href').replace('/spaceimages', 'https://www.jpl.nasa.gov/spaceimages')
        featured_image['Featured_Mars_Image'] = image_loc

    ### Mars Facts ###
    res = requests.get(config.Mars_Facts_url)
    soup_table = BeautifulSoup(res.content, 'html.parser')
    Mars_facts = pd.DataFrame(columns=['Description', 'Facts'])
    for tbody in soup_table.findAll('table', {"id": "tablepress-p-mars"}):
        tr = tbody.find_all('tr')
        for _tr in tr:
            td = _tr.find_all('td')
            col1 = td[0].get_text()
            col2 = td[1].get_text()
            df = pd.DataFrame({'Description': [col1], 'Facts': [col2]})
            Mars_facts = Mars_facts.append(df).reset_index(drop=True)

    Mars_facts.to_html('Mars_Facts.html', index=False)

    ### Mars Hemispheres ###
    res = requests.get(config.Mars_Hemispheres_url)
    soup_table = BeautifulSoup(res.content, 'html.parser')
    hemisphere_AllInfo = soup_table.findAll("div", {"class": "collapsible results"})
    items = soup_table.findAll("div", {"class": "item"})

    hemisphere_image_urls = []
    Mars_hemisphere = pd.DataFrame(columns=['Hemisphere_Title', 'ImageLocation'])
    for _item in items:
        class1 = _item.find_all('a')
        for _class1 in class1:
            title = _class1.get_text()
            image_loc = _class1.find('img')['src'].replace('/cache', 'https://astrogeology.usgs.gov/cache')
            d = pd.DataFrame({'Hemisphere_Title': [title], 'ImageLocation': [image_loc]})
            mars_dict = {'Hemisphere_Title': title, 'ImageLocation': image_loc}
            hemisphere_image_urls.append(mars_dict)
            Mars_hemisphere = Mars_hemisphere.append(d).reset_index(drop=True)
    scrap_dictionary = {"_id":"mars_record","Mars_News":Mars_News.to_dict(orient='records'),"Featured_Image":[featured_image],"Mars_facts":Mars_facts.to_dict(orient='records'),"Mars_hemisphere":Mars_hemisphere.to_dict(orient='records')}
    return scrap_dictionary

if __name__=='__main__':
    a = scrape()
    print(a)

