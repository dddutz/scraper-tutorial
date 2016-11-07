#!/usr/bin/env python

"""Web scraper application for supost.com.

This program searches supost.com for posts that contain certain given keywords.

Example:
    $ python3 supost_web_scraper.py

Attributes:
    OFFSET_INCREASE (int): number of pages to search per iteration in the
        program loop.
"""

import datetime                       # for date and time
import httplib2                       # for receiving web pages
from bs4 import BeautifulSoup         # for getting information from web pages

__author__ = "Derin Dutz, Kevin Ko"
__copyright__ = "Copyright 2016, Derin Dutz. All rights reserved."
__credits__ = ["Derin Dutz", "Kevin Ko"]
__license__ = "MIT"
__version__ = "1.0.1"
__status__ = "Development"

KEYWORDS = ["tree"]
OFFSET_INCREASE = 99  # amount to increase page offset


def main():
    """Runs the program."""
    matches = scrape_supost(KEYWORDS, 1)
    print(matches)


def scrape_supost(keywords, days_to_check):
    """Scrapes supost.com to find all posts which contains the given keywords.

    Args:
        keywords (list of str): keywords to search for.
        days_to_check (int): number of days back to search.

    Returns:
        A list of matches where each match is a tuple of keyword, link, and
        post title.
    """
    oldest_date = (datetime.date.today() -
                   datetime.timedelta(days=days_to_check))
    oldest_date_str = oldest_date.strftime("%a, %b %d")

    offset = 0
    matches = []
    link = "http://supost.com/search/index/5"

    while True:
        response, content = httplib2.Http().request(link)
        index_page = BeautifulSoup(content, "lxml")
        for link in index_page.find_all("a"):
            href = link.get("href").encode('utf-8')
            if ("post/index" in href):
                matches.extend(
                    scrape_post("http://supost.com" + href, keywords))

        # stops scraper when oldest date is found
        if (oldest_date_str in index_page.get_text().encode('utf-8')):
            return matches

        offset += OFFSET_INCREASE

        # updates the link with the new offset
        link = "http://supost.com/search/index/5?offset=" + str(offset)


def scrape_post(link, keywords):
    """Scrapes the post corresponding to the given link and searches for the
    given keywords.

    Args:
        link (str): link to scrape.
        keywords (list of str): keywords to search for.

    Returns:
        A list of matches where each match is a tuple of keyword, link, and
        post title.
    """
    print("scraping post: " + link + "...")
    matches = []
    response, content = httplib2.Http().request(link)
    post_page = BeautifulSoup(content, "lxml")
    for keyword in keywords:
        if keyword in post_page.get_text().encode('utf-8').lower():
            post_title = post_page.find("h2", {"id": "posttitle"}).text
            matches.append((keyword, link, post_title))
    return matches


if __name__ == "__main__":
    main()
