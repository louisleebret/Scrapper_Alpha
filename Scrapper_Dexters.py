# Importation of the required libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re



# Definition of the class Scrapper_Dexters
class Scrapper_Dexters(object):
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
    
    def get_prices_tag(self):
        """
        This method returns a list of the property prices markups for a given URL
        """
        a = self.parse_html()
        price_tag = a.find_all('span', class_="price")
        return price_tag
    
    def get_prices_list(self):
        """
        This method returns a list of the property prices for a given URL
        """
        a = self.get_prices_tag()
        price_list = []
        for i in range(0,len(a)):
            price = a[i].text
            price = price[8:]
            price = price.replace("w","")
            price = price.replace("£","")
            price = price.replace("/","")
            price = price.replace("Pcm","")
            price = price.replace("(Tenant Info)","")
            price = price.replace("Let","")
            price = price.replace(" ","")
            price = price.replace(",","")
            price = price.replace("P","")
            price=int(price)
            price_list.append(price)
        return price_list
    
    def get_adress_tag(self):
        """
        This method returns a list of the property adresses markup for a given URL
        """
        a = self.parse_html()
        adress_tag = a.find_all('div',class_='result-content')
        return adress_tag
    
    
    def get_adress_list(self):
        """
        This method returns a list of the property adresses for a given URL
        """
        a = self.get_adress_tag()
        adress_list = []
        for i in range(0,len(a)):
            adress = a[i].text
            adress = adress[1:]
            position =adress.index('\n')
            adress = adress[:position] 
            adress = re.sub(r"(\w)([A-Z])", r"\1, \2", adress[:-3])+adress[-3:]#Separate the road and neighbourhood
            adress_list.append(adress)
        return adress_list
    
    def get_links_tag(self):
        """
        This method returns a list of the property links markups for a given URL
        """
        a = self.parse_html()
        links_tag = a.find_all('div', class_='result-content')
        return links_tag
    
    def get_links(self):
        """
        This method returns a list of the property links for a given URL
        """
        a=self.get_links_tag()
        links_list=[]
        for i in range(0,len(a)):
            link=a[i].a['href']
            link=f'https://www.dexters.co.uk{link}'
            links_list.append(link)
        return links_list
    
    
    def get_description_tag(self):
        """
        This method returns a list of the property description markups for a given URL
        """
        a = self.parse_html()
        description_tag = a.find_all('div', class_='result-entry')
        return description_tag
    
    def get_description(self):
        """
        This method returns a list of the property description for a given URL
        """
        a=self.get_description_tag()
        description_list=[]
        for i in range(0,len(a)):
            description = a[i].text
            description_list.append(description)
        return description_list
    
    def get_bedroom_tag(self):
        """
        This method returns a list of the property bedroom markups for a given URL
        """
        a = self.parse_html()
        bedroom_tag = a.find_all('ul', class_='list-info')
        return bedroom_tag
    
    def get_bedroom(self):
        """
        This method returns a list of the property bedrooms for a given URL
        """
        a=self.get_bedroom_tag()
        bedroom_list=[]
        for i in range(0,len(a)):
            bedroom = a[i].text
            bedroom = bedroom[1:3]
            bedroom = int(bedroom)
            bedroom_list.append(int(bedroom))
        return bedroom_list  

    def get_bathroom_tag(self):
        """
        This method returns a list of the property bathroom markups for a given URL
        """
        a = self.parse_html()
        bathroom_tag = a.find_all('ul', class_='list-info')
        return bathroom_tag
    
    def get_bathroom(self):
        """
        This method returns a list of the property bedrooms for a given URL
        """
        a=self.get_bathroom_tag()
        bathroom_list=[]
        for i in range(0,len(a)):
            bathroom = a[i].text
            bathroom = bathroom.replace('\n','')
            bathroom = bathroom[2:]
            bathroom = bathroom.replace('Bedrooms','')
            bathroom = bathroom.replace('Bedroom','')
            bathroom = bathroom[0]
            if bathroom=='B':
                bathroom = '1'
            bathroom = int(bathroom)
            bathroom_list.append(bathroom)
        return bathroom_list
    
    def data_frame(self):
        """
        This method returns a data frame that contains all the information scrapped on the web page for a given URL
        """

        # The attributes are scrapped using the following class method
        adresses = self.get_adress_list()
        prices = self.get_prices_list()
        bedroom = self.get_bedroom()
        bathroom = self.get_bathroom()
        description = self.get_description()
        link = self.get_links()
        
        # The list are resized in the event of an array being to long or too short
        prices = prices[0:len(adresses)]
        bedroom = bedroom[0:len(adresses)]
        description= description[0:len(adresses)]
        link = link[0:len(adresses)]
        bathroom = bathroom[0:len(adresses)]
        website = ["Dexters" for i in range(0,len(adresses))]

        # The attributes are assembled inside a data frame
        df = pd.DataFrame({'Adress': adresses, 'Price per month (£)': prices, 'Bedrooms':bedroom,'Bathrooms':bathroom, 'Description': description, 'Link to the property':link,'Scrapped on':website})
        return df
    




def Scr_Dexters(post_code):
    """
    This function uses the class Scrapper Hampton to scrap the first three page of the website at a given postcode. The function return a data frame 
    that contains all the information scrapped on these three pages
    """
    
    URL_p1=f'https://www.dexters.co.uk/property-lettings/properties-to-rent-in-{post_code}/'
    URL_p2=f'https://www.dexters.co.uk/property-lettings/properties-to-rent-in-{post_code}/page-2'
    URL_p3=f'https://www.dexters.co.uk/property-lettings/properties-to-rent-in-{post_code}/page-3'
        
    c= Scrapper_Dexters(URL_p1)
    e= Scrapper_Dexters(URL_p2)
    f= Scrapper_Dexters(URL_p3)
        
    df1= c.data_frame()
    df2= e.data_frame()
    df3 = f.data_frame()
        
    a = pd.concat([df1,df2,df3], ignore_index=True)
    a = a.drop_duplicates(subset=None, keep='first', inplace=False) #delete duplicates 
    return a



if __name__ == "__main__":
    postcode = input("Enter Postcode:")
    a = Scr_Dexters(postcode)
    print(a)

    