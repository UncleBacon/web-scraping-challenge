from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import pymongo



#create Scrape function

def scrape():

    #set up Browser

    executable_path = {'executable_path': "chromedriver"}
    browser = Browser('chrome', **executable_path, headless=False)
    
    #Get Nasa News
    nasa_news = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_news)
    html = browser.html
    soup = bs(html, 'html.parser')
    results = soup.find_all('li', class_="slide")

    for result in results[0]:
        news_title = result.find('div',class_="content_title").text
        news_description = result.find('div',class_="article_teaser_body").text
        news_url = nasa_news + result.a['href']
        
    time.sleep(1)
    
    #Collect JPL Image
    jpl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl)
    html = browser.html
    soup = bs(html, 'html.parser')

    browser.click_link_by_id('full_image')
    time.sleep(2)
    browser.click_link_by_partial_href('/spaceimages/details')
    soup = bs(browser.html, 'html.parser')
    results = soup.find('figure', class_ = 'lede')
    base_url = browser.url[:24]
    img = results.a.img['src']

    featured_img_url =  base_url + img

    
    time.sleep(1)
    
    
    #Mars Weather
    weather = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather)
    html = browser.html
    soup = bs(html, 'html.parser')
    
    results = soup.find('div', class_="js-tweet-text-container")
    results.a.decompose()
    
    mars_weather = results.find('p').text
    
    time.sleep(1)
    
    #Mars Facts
    space_facts = 'https://space-facts.com/mars/'

    mars_facts = pd.read_html(space_facts)[1].rename(columns = {0:'Fact',1:'Data'}).to_html(index=False).replace('\n','')

    time.sleep(1)
    
    
    #Mars Hemispheres
    hemispheres = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres)
    html = browser.html
    soup = bs(html, 'html.parser')

    #Find list of image tags
    base_url = browser.url[:29]
    results = soup.find_all('div',attrs={'class':'collapsible results'})[0]
    images = results.find_all('div')[:]

    #iterate through length of tags and collect hrefs, navigate to page and collect full image link 
    hemisphere_image_urls = []

    for image in range(0,len(images)):
        if image == 0 or image % 2 == 0:
            url = base_url+images[image].a['href']
            title = (images[image].h3.text)
            browser.visit(url)
            time.sleep(1)
            soup = bs(browser.html,'html.parser')
            results = soup.find_all('ul')[0]
            result = results.find_all('li')[0]
            hemi_url = (result.a['href'])
            hemisphere_image_urls.append({'title':title,
                                          'img_url':hemi_url})
    facts = {'news_title':news_title,
             'news_description':news_description,
             'news_url':news_url,
             'featured_img_url':featured_img_url,
             'mars_weather':mars_weather,
             'mars_facts':mars_facts,
            'hemi_img_url':hemisphere_image_urls}
    
    browser.visit('https://bootcampspot.com/')


    return facts