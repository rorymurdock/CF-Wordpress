import json
import lxml.html
from reqREST import REST

with open('url.json') as json_file:
    url = json.load(json_file)

url = url['url']

REST = REST(url=url, protocol='http')

print('Using URL: %s' % url)

def test_wordpress():
    site = REST.get('')
    assert site.status_code == 200

    tree = lxml.html.fromstring(site.text)
    assert tree.xpath('//title')[0].text_content()) == "Blog Title – Just another WordPress site"