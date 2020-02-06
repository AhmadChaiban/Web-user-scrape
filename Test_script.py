import numpy as np 
import pandas as pd 
from time import sleep
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from stem import Signal
from stem.control import Controller

class ReviewsScraper:
    def __init__(self):
        self.names = []
        self.ratings = []
        self.headers = []
        self.reviews = []
        self.dates = []
        self.locations = []

    def security_breacher(self, http):
        print(http)
        proxies = {'http':  'socks5://127.0.0.1:9050',
                   'https': 'socks5://127.0.0.1:9050'}
 
        s = requests.Session()
        s.proxies = proxies
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
            }
        html = s.get(http, headers=headers).content
        return html

    def get_new_ip(self):
        with Controller.from_port(address = '127.0.0.1', port=9051) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)
            sleep(controller.get_newnym_wait())
    
    def scrape(self, PATH, n_pages, sleep_time = 0.3):
        for p in range(n_pages):
            sleep(sleep_time)
            # self.get_new_ip()            
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
            http = requests.get(f"{PATH}{p+1}", headers= headers, stream=False)
            # http = self.security_breacher(http)
            # http = PATH + str(p+1)
            print(f"{http.text}")

            bsoup = BeautifulSoup(http.text, 'html.parser')
            sleep(5)
            heading_containers = bsoup.find_all('div', class_ = 'box__heading box__heading--bordered p-1')
            ## Review body: reviewBody
            ## Check if you need to click the show more
            review_containers = bsoup.find_all('div', class_ = 'p-1')
            sleep(5)
            ## Generalize the rating boxes
            rating_container = bsoup.find_all('div',class_ = "stars stars--secondary large xlarge--medium-down stars-10")
            sleep(5)
            ## Want the date from inside this
            date_container = bsoup.find_all('div',class_ = "x-current-review-date")
            sleep(5)
            ## We want the href of this 
            profile_link_containers = bsoup.find_all('aside', class_ = 'mr-1' )
            sleep(5)
            print(len(bsoup))
            print(len(review_containers))

            print(rating_container)
            print(heading_containers)

            print(bsoup)
            return
            for x in range(len(bsoup)):
                review_c = review_containers[x]
                self.headers.append(review_c.h2.a.text)
                self.reviews.append(review_c.p.text)
                reviewer = user_containers[x]
                self.names.append(reviewer.h3.text)
                rating = rating_container[x]
                self.ratings.append(rating.div.attrs['class'][1][12])
                date = date_container[x]
                self.dates.append(datetime.datetime.strptime(date.time.attrs['datetime'][0:10], '%Y-%m-%d').date())
                prof = profile_link_containers[x]
                link = 'https://www.trustpilot.com'+ prof.a['href']
                c_profile = requests.get(f'{link}')
                csoup = BeautifulSoup(c_profile.text, 'html.parser')
                cust_container = csoup.find('div', class_ = 'user-summary-location')
                self.locations.append(cust_container.text)
            
        rev_df = pd.DataFrame(list(zip(self.headers, self.reviews, self.ratings, self.names, self.locations, self.dates)),\
        columns = ['Header','Review','Rating', 'Name', 'Location', 'Date'])
    
        rev_df.Review = self.clean_string(rev_df.Review)
        rev_df.Name = self.clean_string(rev_df.Name)
        rev_df.Location = self.clean_string(rev_df.Location)
        rev_df.Location = rev_df.Location.apply(lambda x: x.split(',',1)[-1])
        rev_df.Rating = rev_df.Rating.astype('int')
        rev_df.Date = pd.to_datetime(df.Date)
    
        return rev_df

    def clean_string(self, column):
        return column.apply(lambda x: x.replace("\n",'',2)).apply(lambda x: x.replace('  ',''))

if __name__ == '__main__':
    Trello_df = ReviewsScraper().scrape(PATH='https://www.g2.com/products/trello/reviews?page=',\
                                         n_pages = 1)
    print(Trello_df)

