import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_html(url):
    """
    Stáhne HTML z dané URL a vrátí je jako text (dekódovaný řetězec).
    """
    with urllib.request.urlopen(url) as response:
        return response.read().decode("utf-8", errors="replace")

def parse_page(url):
    """
    Pomocná funkce pro stažení a zparsování stránky:
    - Vrací titulkový text (str)
    - Vrací seznam absolutních URL adres nalezených v odkazech <a href="...">
    """
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")

    title_tag = soup.find("title")
    title_text = title_tag.get_text(strip=True) if title_tag else "Bez titulku"

    links = []
    for a_tag in soup.find_all("a", href=True):
        absolute_link = urljoin(url, a_tag["href"])
        links.append(absolute_link)

    return title_text, links

def main():
    main_url = "http://vlada.cz"

    main_title, main_links = parse_page(main_url)

    print(f"Titulek hlavní stránky: {main_title}")

    print(f"Počet odkazů na hlavní stránce: {len(main_links)}\n")

    for i, link in enumerate(main_links, start=1):
        try:
            link_title, link_links = parse_page(link)
            print(f"{i}. Odkaz: {link}")
            print(f"   Titulek: {link_title}")
            print(f"   Počet odkazů na podstránce: {len(link_links)}\n")
        except Exception as e:
            print(f"{i}. Odkaz: {link}")
            print(f"   Nepodařilo se načíst stránku: {e}\n")

if __name__ == "__main__":
    main()
