# Importation of the required libraries

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


# Definition of the class Scrapper_hamptons

class Scrapper_hamptons(object):
    def __init__(self, URL):
        """
        The class only needs one information to be initialized: the page URL
        """
        self.URL = URL
    
    def get_html(self):
        """
        This method returns the HTML code of a given URL
        """
        URL = self.URL
        page = requests.get(URL)
        return page
    
    def parse_html(self):
        """
        This method parses the HTML code for a given URL
        """
        html = self.get_html()
        soup = BeautifulSoup(html.content, 'html.parser')
        return soup

    def get_room_info(self):
        """
        This method returns a list of number of bedrooms, bathrooms and living for the properties for a given URL
        """
        a = self.parse_html()
        room = a.find_all('ul', class_='card-content__spec-list')

        room_list = []
        for i in range(0,len(room)):
            numbers = []
            c = room[i].text
            for word in c.split():
                if word.isdigit():
                    numbers.append(int(word))
            room_list.append(numbers)

        return room_list[:-1]

    def get_bedrooms(self):
        """
        This method returns the list of the bedrooms for a given URL
        """
        a = self.get_room_info()
        bedroom = []
        for i in range(0,len(a)):
            bedroom.append(int(a[i][0]))
        
        return bedroom

    def get_bathrooms(self):
        """
        This method returns the list of the bathrooms for a given URL
        """
        a = self.get_room_info()
        bathroom = []
        for i in range(0,len(a)):
            bathroom.append(int(a[i][1]))
        
        return bathroom


    def get_link(self):
        """
        This method returns a list of the property links for a given URL
        """
        a = self.parse_html()
        link = a.find_all('div',class_='card')

        link_list = []
        for i in range(0,len(link)):
            a = link[i].a['href']
            b = f'https://www.hamptons.co.uk{a}'
            link_list.append(b)
        
        return link_list[:-1]

    def get_description_and_adress(self):
        """
        This method returns a list of the property description and adress for a given URL
        """
        a = self.parse_html()
        description = a.find_all('div',class_='card__text')

        result = []

        for i in range(0,len(description)):
            text = description[i].text[1:len(description[i].text)-1]
            text = text.split('\n')
            result.append(text)


        return result[:-2]


    def get_adress(self):
        """
        This method returns a list of the property adresses for a given URL
        """
        a = self.get_description_and_adress()

        adress = []
        for i in range(0,len(a)):
            adress.append(a[i][1])
        return adress

    def get_description(self):
        """
        This method returns a list of the property descriptions for a given URL
        """
        a = self.get_description_and_adress()

        dresci = []
        for i in range(0,len(a)):
            dresci.append(a[i][0])
        return dresci


    def get_price(self):
        """
        This method returns a list of the property prices for a given URL
        """
        a = self.parse_html()
        price = a.find_all('p',class_='card__heading')
        price_list = []

        for i in range(0,len(price)-2):
            p = price[i].text
            p = p.replace("\r\n                                            ","")
            p = p.replace("                                        ","")
            p = p.replace("\r\n","")
            p = p.replace("£","")
            
            if "pw" in p:
                p = p.replace("pw","")
                p = p.replace(",","")
                p = p.replace(" ","")
                p = float(p)
                p = p*4.3333
                p = round(p,0)
            else:
                p = p.replace("pcm","")
                p = p.replace(",","")
                p = p.replace(" ","")
                p = float(p)
            price_list.append(int(p))
        return price_list

    def data_frame(self):
        """
        This method returns a data frame that contains all the information scrapped on the web page for a given URL
        """

        # The attributes are scrapped using the following class method
        adress = self.get_adress()
        prices = self.get_price()
        bedrooms = self.get_bedrooms()
        bathrooms = self.get_bathrooms()
        description = self.get_description()
        link = self.get_link()
        website = ['Hamptons' for i in range(0,len(adress))]

        df = pd.DataFrame({'Adress':adress,'Price per month (£)':prices,'Bedrooms':bedrooms,'Bathrooms':bathrooms,'Description':description,'Link to the property': link,'Scrapped on':website})
        return df




def Scr_hamptons(post_code):
    """
    This function uses the class Scrapper Hampton to scrap the main page of the website at a given postcode. The function return a data frame 
    that contains all the information scrapped on these three pages
    """

    URL_p1=f'https://www.hamptons.co.uk/rent/search/{post_code}/page-1/pricing-monthly/'
    URL_p2=f'https://www.hamptons.co.uk/rent/search/{post_code}/page-2/pricing-monthly/'
    URL_p3=f'https://www.hamptons.co.uk/rent/search/{post_code}/page-3/pricing-monthly/'
    
    c= Scrapper_hamptons(URL_p1)
    e= Scrapper_hamptons(URL_p2)
    f= Scrapper_hamptons(URL_p3)
    
    df1= c.data_frame()

    
    a = pd.concat([df1], ignore_index=True)
    a = a.drop_duplicates(subset=None, keep='first', inplace=False) #delete duplicates 
    return a


if __name__ == "__main__":
    postcode = input("Enter Postcode:")
    a = Scr_hamptons(postcode)
    print(a)