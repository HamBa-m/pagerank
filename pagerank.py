import numpy as np
from crawl import crawl_page
import matplotlib.pyplot as plt

def pagerank(urls, max_iter=100, d=0.85):
    """
    Computes the PageRank scores for the given URLs using the power iteration method.
    """
    num_urls = len(urls)
    # Create a dictionary mapping URLs to indices in the transition matrix
    url_indices = {url: i for i, url in enumerate(urls)}
    # Create the transition matrix A
    A = np.zeros((num_urls, num_urls))
    for i, url in enumerate(urls):
        links = crawl_page(url)[1]
        for link in links:
            if link in url_indices:
                j = url_indices[link]
                A[j, i] = 1
        # Normalize the columns of A
        col_sums = A.sum(axis=0)
        non_zero_cols = np.where(col_sums != 0)[0]
        A[:, non_zero_cols] /= col_sums[non_zero_cols]
    # Initialize the PageRank vector
    p = np.ones(num_urls) / num_urls
    # Perform power iteration
    for _ in range(max_iter):
        new_p = np.zeros(num_urls)
        for i in range(num_urls):
            new_p[i] = (1 - d) / num_urls
            for j in np.where(A[:, i] != 0)[0]:
                new_p[i] += d * p[j] * A[j, i]
        p = new_p
    # plot the ranks of the urls as a bar chart with the url as the label of the bar
    u = [url.split('/')[-1] for url in urls]
    plt.bar(u, p)
    plt.xticks(rotation=90)
    plt.show()
    
    return p.tolist()
