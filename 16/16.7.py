import urllib.request
from bs4 import BeautifulSoup

def parse_with_beautifulsoup():
    url = "http://vlada.cz"
    with urllib.request.urlopen(url) as response:
        html_code = response.read().decode("utf-8")

    soup = BeautifulSoup(html_code, "html.parser")

    title_tag = soup.find("title")
    if title_tag:
        print("Titulek stránky:", title_tag.get_text(strip=True))
    else:
        print("Tag <title> nebyl nalezen.")

    h1_tags = soup.find_all("h1")
    h2_tags = soup.find_all("h2")

    print("\nNadpisy H1:")
    for h1 in h1_tags:
        print("-", h1.get_text(strip=True))

    print("\nNadpisy H2:")
    for h2 in h2_tags:
        print("-", h2.get_text(strip=True))

    print("\nURL adresy všech odkazů <a href=...>:")
    for a_tag in soup.find_all("a", href=True):
        print("-", a_tag["href"])

if __name__ == "__main__":
    parse_with_beautifulsoup()
