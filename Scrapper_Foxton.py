# Importation of the required libraries

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


# Definition of the class Scrapper_Alpha

class Scrapper_Foxton(object):
    def __init__(self, Post_Code):
        """
        The class only needs one information to be initialized: the post_code
        """
        self.post_code = Post_Code
    
    def get_html(self):
        """
        This method returns the HTML code of a given Post code
        """
        URL = f'https://www.foxtons.co.uk/properties-to-rent/{self.post_code}/'
        page = requests.get(URL)
        return page
    
    def parse_html(self):
        """
        This method parses the HTML code for a given postcode
        """
        html = self.get_html()
        soup = BeautifulSoup(html.content, 'html.parser')
        return soup
    
    def get_links(self):
        """
        This method returns a list of the property links for a given postcode
        """
        a = self.parse_html()
        links = a.find_all('p', class_='description')
        liste = []
        for i in range(0,len(links)):
            link = links[i].a['href']
            link_new = f'https://www.foxtons.co.uk{link}'
            liste.append(link_new)
        return liste
    
    def get_prices_tag(self):
        """
        This method returns a list of the markups with the price for a given postcode
        """
        a = self.parse_html()
        price_tag = a.find_all('span', class_="month")
        return price_tag
    
    def get_prices_list(self):
        """
        This method returns a list of the markups with the price for a given postcode
        """
        a = self.get_prices_tag()
        price_list = []
        for i in range(0,len(a)):
            price = a[i].text
            price = int(price.replace(" pcm", ""))
            price_list.append(price)
        return price_list
    
    def get_adress_tag(self):
        """
        This method returns a list of the markups with the adresses for a given postcode
        """
        a = self.parse_html()
        adress_tag = a.find_all('h6')
        return adress_tag
    
    def get_adress_list(self):
        """
        This method returns a list of the adresses for a given postcode
        """
        a = self.get_adress_tag()
        adress_list = []
        for i in range(0,len(a)):
            adress = a[i].text
            if adress[-1] == self.post_code[-1]:
                adress_list.append(adress)
        
        if 'You might also be interested in...' in adress_list:
            adress_list.remove('You might also be interested in...')
        return adress_list
        

    def get_bedroom(self):
        """
        This method returns the list of the bedrooms for a given postcode
        """
        a = self.parse_html()
        bedroom = a.find_all('span', class_= 'bedrooms')
        liste_bed = []
        for i in range(0,len(bedroom)):
            liste_bed.append(int(bedroom[i].text))
        return liste_bed
    
    def get_bathroom(self):
        """
        This method returns the list of the bathrooms for a given postcode
        """
        a = self.parse_html()
        bathroom = a.find_all('span', class_= 'bathrooms')
        liste_bath = []
        for i in range(0,len(bathroom)):
            liste_bath.append(int(bathroom[i].text))
        return liste_bath
    
    def get_property_type(self):
        """
        This method returns the list of the property types for a given postcode
        """
        a = self.parse_html()
        flat_type = a.find_all('b')
        return flat_type
    
    def get_description_tag(self):
        """
        This method returns a list of the markups with the property description for a given postcode
        """
        a = self.parse_html()
        description = a.find_all('p', class_='description')
        return description
    
    def get_description_list(self):
        a = self.get_description_tag()
        description_list = []
        for i in range(0,len(a)):
            description = a[i].text
            description = description.replace(" View more\n", "")
            description = description.replace("\n", "")
            description_list.append(description)
        #description_list.remove('This is a Sneak Peek because you are logged in to My Foxtons.')
        return description_list
    
    def data_frame(self):
        """
        This method returns a data frame that contains all the information scrapped on the web page for a given Postcode
        """

        # The attributes are scrapped using the following class method
        adresses = self.get_adress_list()
        prices = self.get_prices_list()
        bedroom = self.get_bedroom()
        bathroom = self.get_bathroom()
        description = self.get_description_list()
        links = self.get_links()
        website = ["Foxton" for i in range(0,len(adresses))]

        
        # The list are resized in the event of an array being to long or too short
        prices = prices[0:len(adresses)]
        bedroom = bedroom[0:len(adresses)]
        bathroom = bathroom[0:len(adresses)]
        description = description[0:len(adresses)]
        links = links[0:len(adresses)]

        # The attributes are assembled inside a data frame
        df = pd.DataFrame({'Adress': adresses, 'Price per month (£)': prices, 'Bedrooms':bedroom, 'Bathrooms':bathroom, 'Description':description, 'Link to the property': links, 'Scrapped on': website})
        return df



if __name__ == "__main__":
    postcode = input("Enter Postcode:")
    a = Scrapper_Foxton(postcode)
    print(a.data_frame())



















    