from base_scraper import BaseScraper

class QualiScraper(BaseScraper):
    def __init__(self, year: str):
        super().__init__(year)
        self.output_prefix = "quali_laps"

    def fetch_sessions(self):
        """
        Fetch qualifying sessions for the given year.
        """
        url = f"https://api.openf1.org/v1/sessions?session_name=Qualifying&year={self.year}"
        data = self.fetch_json(url)
        return data if isinstance(data, list) else []

def main():
    year = input("Enter a year for Qualifying sessions (e.g. 2023): ").strip()
    if not year.isdigit():
        print("Invalid year entered!")
        return
    scraper = QualiScraper(year)
    scraper.run()

if __name__ == "__main__":
    main()
