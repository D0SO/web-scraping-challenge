# import necessary libraries
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as Soup
import datetime as dt


def init_browser():
    
    executable_path = {"executable_path": "C:/chromedriver.exe"}

    return Browser("chrome", **executable_path, headless=False)


def scrape():
    
    browser = init_browser()
    title, paragraph = news(browser)

    # Run scraping and store the results in a dictionary

    mars_dict = {
        "news_title": title,
        "news_paragraph": paragraph,
        "featured_image": image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser),
        "last_modified": dt.datetime.now()
    }

    # Stop Browser connection 
    browser.quit()

    return mars_dict

def news(browser):

    # Visit the mars nasa news site with splinter
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

     # Use beautiful soup to turn the browser html to a soup object
    html = browser.html
    news_soup = Soup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        
        # Use bs to get news title and paragraph info from the html object
        title = slide_elem.find("div", class_="content_title").text
        paragraph = slide_elem.find("div", class_="article_teaser_body").text

    except AttributeError:
        return None, None

    return title, paragraph

def image(browser):

    # Visit the mars nasa news site for images
    url_img = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_img)
    # Turn webpage into HTML object
    html_img = browser.html
    soup_img = Soup(html_img, "html.parser")
    # Create a list to collect the link to each image displayed on the page
    img_list = []
    try: 
    # Locate the images in this webpage
        images = soup_img.find_all('img')
   
    # Create a loop through the imaged to append the image link to our img_list
        for img in images:
            img_list.append(img['src'])

    # Select the specific desired image

    except AttributeError:
        return None
    # Select the specific desired image
    img_url = img_list[2]
    
    # full_url = url_img + img_url 

    return img_url

def mars_facts():
    # Mars facts to be scraped
    url_facts = 'https://space-facts.com/mars/'

    try:
        # Use pandas to read the tables available on the html
        read_table = pd.read_html(url_facts)

    except BaseException:
        return None
    # Select the first table of the html
    facts_df = read_table[0]
    facts_df.columns =  ['Facts', 'Mars']

    return facts_df.to_html()


def hemispheres(browser):
    # Create a lists to store the large image links
    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)

    hemi_links = []

    try: 
        # Create a soup object
        html_hemi = browser.html
        soup_hemi = Soup(html_hemi, 'html.parser')
        # Find the desired data by tag and class
        hemis = soup_hemi.find_all("div", class_="item")
        # loop through image data to find title and url info
        for h in hemis:
            # Identify the image name 
            title = h.find("h3").text
    
            # Collect the direct image address
            img_url = h.a["href"]
    
            # build the complete link 
            url = "https://astrogeology.usgs.gov" + img_url
    
            # Visit img url with splinter
            browser.visit(url)
            each_pic_html = browser.html

            # Create soup object fo each of the individual pictures we are visiting
            soup = Soup(each_pic_html,"html.parser")

            # Find the url for high resolution picture
            new_url = soup.find("img", class_="wide-image")["src"]
    
            # Build large picture complete link
            hemi_link = "https://astrogeology.usgs.gov" + new_url
            # Create a dictionary with thetitle and link collected on this loop and append it to our hemi_links list
            hemi_links.append({"title": title, "img_url": hemi_link})

    except AttributeError:
        return None 

    return hemi_links


if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape())