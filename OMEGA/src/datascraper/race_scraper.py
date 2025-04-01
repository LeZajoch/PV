from base_scraper import BaseScraper

class RaceScraper(BaseScraper):
    def __init__(self, year: str):
        super().__init__(year)
        self.output_prefix = "race_laps"

    def fetch_sessions(self):
        """
        Fetch race sessions for the given year.
        """
        url = f"https://api.openf1.org/v1/sessions?session_type=Race&year={self.year}"
        data = self.fetch_json(url)
        return data if isinstance(data, list) else []

def main():
    year = input("Enter a year for Race sessions (e.g. 2023): ").strip()
    if not year.isdigit():
        print("Invalid year entered!")
        return
    scraper = RaceScraper(year)
    scraper.run()

if __name__ == "__main__":
    main()
