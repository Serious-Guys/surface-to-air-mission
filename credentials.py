import json
from utils import Singleton


class Credentials(metaclass=Singleton):

    def __init__(self):
        self.load()

    def load(self, filename="credentials.json"):
        with open(filename, 'r') as f:
            self.json = json.load(f)


credentials = Credentials()


class CredentialsWrapper:

    @staticmethod
    def get_nasa_earthdata_creds() -> tuple:
        """
        :return: tuple of username and password
        """
        temp = credentials.json["apis"]["nasa.earthdata.gov"]
        return temp["username"], temp["password"]

    @staticmethod
    def get_copernicus_creds() -> tuple:
        """
        :return: tuple of username and password
        """
        temp = credentials.json["apis"]["scihub.copernicus.eu"]
        return temp["username"], temp["password"]
