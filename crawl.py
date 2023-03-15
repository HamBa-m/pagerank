from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import re

def get_links(html, base_url):
    """
    Parses an HTML string and returns a list of links contained within it.
    """
    links = []
    pattern = re.compile(r'<a\s+(?:[^>]*?\s+)?href="([^"]*)"')
    for match in pattern.finditer(html):
        link = match.group(1).strip()
        if link.startswith('#'):
            continue
        parsed_link = urlparse(link)
        if not parsed_link.scheme and not parsed_link.netloc:
            link = base_url[:-7] + link
        links.append(link)
    return links

def crawl_page(url):
    """
    Crawls a web page and returns its HTML content and a list of links to other pages.
    """
    try:
        print('Crawling page: {}'.format(url))
        with open(url.replace('file://', '')) as f:
            html = f.read().lower()
    except IOError:
        print('Could not open file: {}'.format(url))
        return None, []
    links = get_links(html, url)
    print('Found {} links'.format(len(links)))
    return html, links


# # test it from a file on the hard disk

# fhand = open('www/p1.html')
# html = fhand.read()
# soup = BeautifulSoup(html, "html.parser")
# tags = soup('a')
# urls = []
# for tag in tags:
#     urls.append(tag.get('href', None))
# print(urls)