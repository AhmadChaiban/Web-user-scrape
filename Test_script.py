import numpy as np 
import pandas as pd 
from time import sleep
import requests
from bs4 import BeautifulSoup
from datetime import datetime

class ReviewsScraper:
    def __init__(self):
        self.names = []
        self.ratings = []
        self.headers = []
        self.reviews = []
        self.dates = []
        self.locations = []
    
    def scrape(self, PATH, n_pages, sleep_time = 0.3):
        print(n_pages)
        for p in range(n_pages):
            sleep(sleep_time)

            http = requests.get(f"{PATH}{p+1}")
            bsoup = BeautifulSoup(http.text, 'html.parser')

            review_containers = bsoup.find_all('div', class_ = 'review-info__body')
            user_containers = bsoup.find_all('div', class_ = 'consumer-info__details')
            rating_container = bsoup.find_all('div',class_ = "review-info__header__verified")
            date_container = bsoup.find_all('div',class_ = "header__verified__date")
            profile_link_containers = bsoup.find_all('aside', class_ = 'content-section__consumer-info' )
            print(len(bsoup))
            print(len(review_containers))
            
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
    Reviews_df = ReviewsScraper().scrape(PATH='https://www.trustpilot.com/review/flixbus.com?languages=all&page=',\
        n_pages = 80)

    print(Reviews_df)

