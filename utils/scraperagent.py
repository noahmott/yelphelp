import requests

class ScraperAgent():
    """
    A class used to test a connection to the Yelp webpage.

    Methods
    --------

    testconnection(url):
        Sends a test request to the web page seeking a response
    
    """

    def __init__(self, header):
      """
      Constructs the request object using predefined headers

      Parameters
      ----------
          header : dic
              a json dictionary with header configurations
      """
      self.header=header

    def testconnection(self, url):
        """
        returns a response from the webpage

        Parameters
        ----------
        url : str
            starting page url

        Returns
        -------
        response code
        """
        response=requests.get(url, headers=self.header)
        return response