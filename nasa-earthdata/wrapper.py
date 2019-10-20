import os
import requests
import bs4


from credentials import CredentialsWrapper as creds


class SessionWithHeaderRedirection(requests.Session):
    AUTH_HOST = 'urs.earthdata.nasa.gov'

    def __init__(self, username, password):
        super().__init__()
        self.auth = (username, password)

    def rebuild_auth(self, prepared_request, response):
        headers = prepared_request.headers
        url = prepared_request.url

        if 'Authorization' in headers:
            original_parsed = requests.utils.urlparse(response.request.url)
            redirect_parsed = requests.utils.urlparse(url)

            if (original_parsed.hostname != redirect_parsed.hostname) and redirect_parsed.hostname !=\
                    self.AUTH_HOST and original_parsed.hostname != self.AUTH_HOST:
                del headers['Authorization']

        return


username, password = creds.get_nasa_earthdata_creds()
session = SessionWithHeaderRedirection(username, password)

datasets = {
    'AerosolIndex': ['https://omisips1.omisips.eosdis.nasa.gov/outgoing/OMAERUV'],
    'CarbonMonoxide': ['http://lance1.acom.ucar.edu/data/L2/'],
    'Ozone': ['https://omisips1.omisips.eosdis.nasa.gov/outgoing/OMTO3/'],
}


def save_topics(topics: list = None):
    if not topics:
        topics = ['AerosolIndex']

    get_urls = {}
    for topic in topics:
        urls = datasets[topic]
        get_urls[topic] = []
        for url in urls:
            response = session.get(url, stream=True)
            soup = bs4.BeautifulSoup(response.content, parser="lxml", features="lxml")
            for link in soup.findAll('a'):
                if link.text.endswith('.he5'):
                    get_urls[topic].append(f'{url}/{link.text}')

    for topic, urls in get_urls.items():
        for url in urls:
            filename = url[url.rfind('/') + 1:]
            directory = f'cache/nasa-earthdata/{topic}/'
            save_path = directory + filename

            try:
                response = session.get(url, stream=True)
                response.raise_for_status()

                if not os.path.exists(directory):
                    os.makedirs(directory, exist_ok=True)

                with open(save_path, 'wb') as fd:
                    for chunk in response.iter_content(chunk_size=1024 * 1024):
                        fd.write(chunk)
                    print(f'Saved {save_path}')

            except requests.exceptions.HTTPError as e:
                print(e)


if __name__ == '__main__':
    save_topics(['Ozone'])
