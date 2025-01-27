import urllib.request

def main():
    url = "http://vlada.cz"

    with urllib.request.urlopen(url) as response:
        html_code = response.read().decode("utf-8")


    print(html_code)

if __name__ == "__main__":
    main()
