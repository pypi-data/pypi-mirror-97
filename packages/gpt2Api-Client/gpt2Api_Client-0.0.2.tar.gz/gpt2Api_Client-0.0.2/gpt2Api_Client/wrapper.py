"""
This is a wrapper for the GPT2 API

Author: Anirudh, TechWithAnirudh
Youtube: https://www.youtube.com/channel/UCmse86kaxJ3n1dDT_bXDukg
"""

__author__ = 'Anirudh, TechWithAnirudh'
__status__ = 'planning'

import requests, warnings

class Api():
    """
    Class for the wrapper.
    Attributes
    ----------
    Private:
        __log_dict : dict
            dict where logging messages are there
    Methods
    -------
    Private:
        __getApiUrl : method that gets the api url
        __requestResponse: main method that calls the Api and returns the JSON
        __log : method that displays the warning messages
    Public:
        UnconditionalSamples : Generates UnconditionalSamples
        ConditionalSamples : Generates ConditionalSamples
    """

    # TODO: Add Logging Fuctionality, Add User Interface

    def __init__(self, model='117M', logging=True):
        """
        Creates a new instance of Api
        Parameters
        ----------
        model : str
            The model that the wrapper should use
        logging : bool
            Log and show warnings
        """
        self.git_url = None
        self.__log_dict = {
            '1': 'WARNING: Samples are unfiltered and may contain offensive content.',
        }
        self.model = model
        self.logging = logging

    def setGitUrl(self, git_url):
        """
        This Collects The Link For The Github File That Contains The Link For The Api
        git_url : str
            url for the api url (Get that from the output from the colab console)
        """
        self.git_url = git_url

    def __getApiUrl(self):
        """
        Gets the api url
        """
        return requests.get(self.git_url).content

    def __requestResponse(self, start_paragraph, topic):
        """
        start_paragraph: str
            paragraph to start genereating from
        topic: str
            UnConditionalSamples or ConditionalSamples
        Main method that calls the Api and returns the JSON
        """
        if not self.git_url != None:
            raise Exception('setGitUrl Is Not Called!')
        final_url = f'{self.__getApiUrl()}/{topic}/{self.model}/{start_paragraph}'
        r = requests.post(final_url)
        return r.json

    def __log(self, msg_num):
        """
        msg_num: int
            index of the warning message
        Displays the warning messages
        """
        if self.logging:
            warnings.warn(self.__log_dict[str(msg_num)])

    def UnconditionalSamples(self, start_paragraph):
        """
        start_paragraph: str
            paragraph to start genereating from
        Generates UnConditionalSamples
        """
        self.__log(msg_num=1)
        return self.__requestResponse(start_paragraph, 'unconditS')
    
    def ConditionalSamples(self, start_paragraph):
        """
        start_paragraph: str
            paragraph to start genereating from
        Generates ConditionalSamples
        """
        return self.__requestResponse(start_paragraph, 'conditS')

if __name__ == '__main__':
    """
    Testing
    """
    start_paragraph = "Today was a fine day. I woke up and brushed my teeth. And Ate Breakfast. I was going to work When"
    api = Api()
    api.setGitUrl(input('Enter The Git URL: '))
    api.ConditionalSamples(start_paragraph)