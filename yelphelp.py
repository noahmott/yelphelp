
from bs4 import BeautifulSoup
import requests
import urllib
from datetime import datetime
import pandas as pd
import time
import re as re
from utils.scraperagent import ScraperAgent

class YelpHelp(ScraperAgent):

  headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
  
  def __init__(self):
    self.scrapertool=ScraperAgent(self.headers)

  def scrape_data(self, url, set_range=8, current_date_css_tag='css-chan6m', current_review_css_tag='raw__09f24__T4Ezm'):
    urllist=self.__collect_urls(url, set_range)
    #print(urllist)
    dates2=[]
    reviews=[]
    for url in urllist:
      #this sleep timer is so the page loads fully on each iteration. js sometimes loads slowly
      time.sleep(4)
      myurl=urllib.request.urlopen(url)
      soup=BeautifulSoup(myurl, 'html.parser')
      dates=soup.find_all('span', class_=current_date_css_tag)
      review=soup.find_all('span', class_=current_review_css_tag)
      for x in dates:
        try:
          datetimeobject=datetime.strptime(str(x.text), '%m/%d/%Y').date()
          dates2.append(datetimeobject)
        except Exception as e:
          pass
      for i in review[5::]:
        #This pattern match is to ignore specific text that has the same tag but not a review.
        if re.search("miles away from|start your review", i.text.lower()):
          print('found match and ignored')
          pass
        else:
          reviews.append(i.text)
    print('Dates: '+str(len(dates2)))
    print('Reviews: '+str(len(reviews)))
    if len(dates2)!=len(reviews):
      print('Check your data. You may have to run this again. Reviews and Dates are uneven')
    else:
      print('Data is even. All good!')
    constructeddf=pd.DataFrame()
    constructeddf['Date']=dates2
    constructeddf['Review']=pd.Series(reviews)
    return constructeddf

      
    
  def __collect_urls(self, url, set_range):   
    print('testing connection....')
    #print(type(self.scrapertool.testconnection(url)))
    if self.scrapertool.testconnection(url).status_code==200:
      print('Connection Good!')
      x=0
      urls=[url]
      for page in range(set_range):
        x+=10
        urls.append(url+'?start='+str(x))
      return urls