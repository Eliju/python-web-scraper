from urllib.request import urlopen
import re


def open_url():
    url = "https://www.imdb.com/search/title/?genres=sci-fi"

    page = urlopen(url)
    html = page.read().decode("utf-8")

    titles = get_titles(html)
    years = get_years(html)
    print(html)
    print(len(titles))
    print(len(years))


def get_titles(html):
    pattern = "<a href=./title/tt.*?/.\n>.*?</a>"
    return get_elements(html, pattern)


def get_years(html):
    pattern = "<span class=.lister-item-year text-muted unbold.>.*?</span>"
    return get_elements(html, pattern)


def get_elements(html, pattern):
    match_results = re.findall(pattern, html, re.IGNORECASE | re.MULTILINE)
    elements = [re.sub("<.*?>", "", element) for element in [re.sub("<.*?\n>", "", element) for element in match_results]]
    return elements
