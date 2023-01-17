import requests

class ScraperAgent():

  def __init__(self, header):
    self.header=header

  def testconnection(self, url):
    response=requests.get(url, headers=self.header)
    return response