# Importation of the required libraries

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


# Importation of the files Scrapper_Foxton.py, Scrapper_Dexters.py and Scrapper_Hampton.py
# These files are required by the class scrapper Alpha
# Scrapper Alpha uses them to get the 3 data frames that contain the search results for each websites
import Scrapper_Foxton as sf
import Scrapper_Dexters as sd
import Scrapper_Hampton as sh

class Scrapper_Alpha(object):
    def __init__(self,post_code, price_min, price_max, bedroom, bathroom):
        """
        The class needs a post code, a minimum and maximum price, a minimum number of bedrooms and a minimum number of bathrooms to be initialized
        """
        self.post_code = post_code
        self.price_min = price_min
        self.price_max = price_max
        self.bedroom = bedroom
        self.bathroom = bathroom
        
    def scrap_foxton(self):
        """
        This methods creates a Scrapper_Foxton object and use it to return a data frame that contains the search results for a given post code on Foxton.co.uk
        """
        a = sf.Scrapper_Foxton(self.post_code)
        return a.data_frame()
    
    def scrap_dexters(self):
        """
        This methods calls the function Scr_Dexters and returns a data frame that contains the search results for a given post code on Dexters.co.uk
        """
        a = sd.Scr_Dexters(self.post_code)
        return a
    
    def scrap_hamptons(self):
        """
        This methods calls the function Scr_Dexters and returns a data frame that contains the search results for a given post code on Hamptons.co.uk
        """
        a = sh.Scr_hamptons(self.post_code)
        return a
    
    def fusion_df(self):
        """
        This method gets three data frame using the three above method and combine these data frames into a single data frame
        The data frame contains all the information scrapped on the three websites
        """
        a = self.scrap_foxton()
        b = self.scrap_dexters()
        c = self.scrap_hamptons()
        
        return pd.concat([a,b,c], ignore_index=True)
    
    def filter_df(self):
        """
        This method gets the data frame that contains all the information scrapped on the three websites
        Then, the method filters the data frame according to the attributes of the object (minimum and maximum price, minimum number of bedrooms, 
        minimum number of bathrooms)
        """
        df = self.fusion_df()
        df1 = df.loc[df['Price per month (£)'] >= self.price_min]
        df2 = df1.loc[df1['Price per month (£)'] <= self.price_max]
        df3 = df2.loc[df2['Bedrooms']>=self.bedroom]
        df4 = df3.loc[df3['Bathrooms']>=self.bathroom]
        
        return df4


if __name__ == "__main__":
    postcode = input("Enter Postcode:")
    price_min = input("Enter minimum price:")
    price_max = input("Enter maximum price:")
    bedroom = input("Enter minimum number of bedrooms:")
    bathroom = input("Enter minimum number of bathrooms:")

    price_min = int(price_min)
    price_max = int(price_max)
    bedroom = int(bedroom)
    bathroom = int(bathroom)


    a = Scrapper_Alpha(postcode,price_min,price_max,bedroom,bathroom)
    print(a.filter_df())


