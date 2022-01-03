import requests
import logging


"""The script returns the json structure of data for Metropolitan Museum api"""


logging.basicConfig(filename='logging_statements.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')


class MuseumApiURL:
    """
        A class for extracting MUSEUM API data in json format.

        Attributes: api_url - url of the rest api is passed while creating the instance of the class.
        constructor: __init__() to initializes the parameters of the instance created.

        Methods:
            get_object_id() - get the list of object_ids from the url
            :returns - list of object_ids
            get_object() - get each artifact data
            :returns - list of dictionary of each artifact
    """

    def __init__(self, api_url):
        self.api_url = api_url
        self.object_id = None
        self.artifact = None

    def get_object_id(self):
        self.object_id = requests.get(url=self.api_url)
        var = self.object_id.json()
        object_ids = var['objectIDs'][:10]
        return object_ids

    def get_object(self, object_id: list):
        artifacts = []
        try:
            for i in object_id:
                self.artifact = requests.get(url=self.api_url + "/{}".format(i))
                artifact = self.artifact.json()
                artifacts.append(artifact)
            return artifacts
        except (requests.ConnectionError, requests.HTTPError) as ce:
            logging.error('Connection is poor ' + str(ce))