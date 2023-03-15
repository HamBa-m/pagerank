from bs4 import BeautifulSoup
from flask import Flask, request, render_template
import os
import re
from urllib.parse import urlparse

app = Flask(__name__, static_folder='static', template_folder='templates')

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

from pagerank import pagerank

def search(query):
    """
    Searches for pages containing the given query string within the local web network starting from the given root URL.
    Ranks the results using the PageRank algorithm.
    """
    visited_urls = set()
    matching_urls = []
    mat_url = []
    queue = []
    for i in range(1,10):
        queue.append('file://' + os.getcwd().replace('\\', '/') + '/www/p{}.html'.format(i))
    query = query.lower()
    while queue:
        url = queue.pop(0)
        if url in visited_urls:
            continue
        visited_urls.add(url)
        html, links = crawl_page(url)
        if html is None:
            continue
        print("Searching for '{}' in {}".format(query, url))
        if query in html:
            matching_urls.append(url)
            soup = BeautifulSoup(html, 'html.parser')
            title_tag = soup.find('title')
            if title_tag:
                t = title_tag.text.strip()
            else:
                t =  ''
            content = soup.text
            mat_url.append({"url": url, "snippet": content[:500] , "title": t})
        for link in links:
            if link not in visited_urls:
                queue.append(link)
    pr_scores = pagerank(matching_urls, max_iter=1000, d=0.85)
    ranked_urls = [url for pr, url in sorted(zip(pr_scores, matching_urls), reverse=True)]
    # add the rank to the mat_url list
    for i in range(len(mat_url)):
        mat_url[i]["rank"] = pr_scores[i]
    # sort the mat_url list
    mat_url = sorted(mat_url, key=lambda k: k['rank'], reverse=True)
    return ranked_urls, mat_url

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search_results():
    query = request.args.get('query')
    if not query:
        return 'Please enter a search query.'
    else:
        root_url = 'file://' + os.getcwd().replace('\\', '/') + '/www/p1.html'
        matching_urls, mat_url = search(query)
        if not matching_urls:
            return 'No results found.'
        else:
            return render_template('results.html', query=query, urls=mat_url, num_results=len(matching_urls))

if __name__ == '__main__':
    app.run(debug=True)
