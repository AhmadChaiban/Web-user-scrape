from selenium.webdriver import Firefox
import pandas as pd

class CHOOCHOO_Scraper:
    def __init__(self):
        self.webdriver = "./"
        self.driver = Firefox(self.webdriver)

    def scrape(self, pages, pre_url):
        for page in range(0,pages):
            url = pre_url + str(page+1)
            self.driver.get(url)
            items = len(self.driver.find_elements_by_class_name("quote"))
            total = []
            for item in range(items):
                quotes = self.driver.find_elements_by_class_name("quote")
                for quote in quotes:
                    quote_text = quote.find_element_by_class_name('text').text
                    author = quote.find_element_by_class_name('author').text
                    new = ((quote_text,author))
                    total.append(new)
            df = pd.DataFrame(total,columns=['quote','author'])
            # df.to_csv('quoted.csv')
        self.driver.close()
        return df

if __name__ == '__main__':
    pre_url = "https://www.g2.com/products/trello/reviews?page="
    pages = 1
    Trello_df = CHOOCHOO_Scraper().scrape(pages, pre_url)
    print(Trello_df)