import pandas as pd
from bs4 import BeautifulSoup
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

def scrape():
    #Latest Title and Paragraph
    browser = init_browser()
    browser.visit('https://mars.nasa.gov/news/')
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    element = soup.select_one("ul.item_list li.slide")
    latest_title = element.find("div", class_ = "content_title").get_text()
    all_p = soup.find_all('div', class_ = 'article_teaser_body')
    latest_p = all_p[0].text

    #Featured Image
    browser.visit('https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html')
    browser.click_link_by_partial_text('FULL IMAGE')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    img_search = soup.find_all('div', class_ = 'fancybox-inner')
    img_result = img_search[0].img['src']
    featured_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + img_result

    #Mars Table
    mars_table = pd.read_html('https://space-facts.com/mars/')
    table = mars_table[0]
    table.columns = ['Description', 'Value']
    table_final = table.to_html(classes="table table-striped table-bordered", index=False, header=False, border=1)

    #Mars Hemispheres Titles and Full Images
    browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    hemisphere_search = soup.find_all('div', class_ = 'collapsible results')
    hemisphere_titles = hemisphere_search[0].find_all('h3')
    titles = []
    for title in hemisphere_titles:
        titles.append(title.text)
    hemisphere_links = soup.find_all('div', class_ = 'item')
    links = []
    for link in hemisphere_links:
        img_link = 'https://astrogeology.usgs.gov' + link.a['href']
        links.append(img_link)
    full_imgs = []
    for link in links:
        browser.visit(link)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        full_img_search = soup.find_all('img', class_ = 'wide-image')
        full_img = 'https://astrogeology.usgs.gov' + full_img_search[0]['src']
        full_imgs.append(full_img)

    #List of Dictionaries
    title_img_zip = zip(titles, full_imgs)
    dict_list = []
    for title, img in title_img_zip:
        title_img_dict = {}
        title_img_dict['title'] = title
        title_img_dict['full_img'] = img
        dict_list.append(title_img_dict)
    
    #Put Data in Dictionary
    scraped_data = {
        "latest_title": latest_title,
        "latest_paragraph": latest_p,
        "featured_image": featured_image_url,
        "mars_facts_table": table_final,
        "hemispheres": dict_list
    }
    
    return scraped_data
    browser.quit()
    