import http.client
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
import os
import re
class MyParser(HTMLParser):
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.images = []
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            for attr in attrs:
                if attr[0] == 'src':
                    self.images.append(urljoin(self.base_url, 
attr[1]))
        elif tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    self.links.append(urljoin(self.base_url, 
attr[1]))
def download(url):
    parser = MyParser(url)
    conn = http.client.HTTPConnection(urlparse(url).netloc)
    conn.request("GET", urlparse(url).path)
    r = conn.getresponse()
    html_content = r.read().decode('UTF-8')
    parser.feed(html_content)
    os.makedirs('images', exist_ok=True) # Create 'images' 
directory if it doesn't exist
    for img_url in parser.images:
        img_domain = urlparse(img_url).netloc
        img_path = urlparse(img_url).path
        img_conn = http.client.HTTPConnection(img_domain)
        img_conn.request("GET", img_path)
        img_data = img_conn.getresponse().read()
        img_conn.close()
        img_name = os.path.basename(img_url)
        with open(os.path.join('images', img_name), 'wb') as 
img_file:
            img_file.write(img_data)
    for link in parser.links:
        if urlparse(link).netloc == urlparse(url).netloc:
            download(link)
download('http://rokot.ibst.psu/anatoly/')
