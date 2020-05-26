import requests
from pprint import pprint
 
your_api_key = ''

ids = []
filepath = 'wsvd_list_original.txt'
with open(filepath) as fp:
    for cnt, line in enumerate(fp):
        url = 'https://www.googleapis.com/youtube/v3/videos?id={}&key={}&part=status'.format(line.strip(), your_api_key)
        url_get = requests.get(url)
        if len(url_get.json()['items']) > 0:
            ids.append(line)
            print(line.strip())