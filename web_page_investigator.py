from urllib.request import urlopen
import re


def open_url():
    url = "https://www.imdb.com/search/title/?genres=sci-fi"

    page = urlopen(url)
    html = page.read().decode("utf-8")
    pattern = '<a href="/title/tt.*?/".>.*?</a>'
    pattern = "<a href=./title/tt.*?/.\n>.*?</a>"
    match_results = re.findall(pattern, html, re.IGNORECASE|re.MULTILINE)
    titles = [re.sub("<.*?>", "", title) for title in [re.sub("<.*?\n>", "", title) for title in match_results]]

    print(html)
    print(titles)
