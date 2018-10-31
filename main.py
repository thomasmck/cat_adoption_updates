import urllib.request as urllib
from bs4 import BeautifulSoup
import csv
import smtplib
from settings import email, password, recipients

class WebScraper:
    """
    Default class searches bluecross website and emails using gmail
    """
    def scrape_website(self):
        """
        Scrape websites for cat names
        returns:
        [[<cat name>, <cat page url>],..]
        """
        # Should make this dynamically update the location and other params
        cat_page = "https://www.bluecross.org.uk/rehome/cat?f[0]=field_centre_single:154&f[1]=field_reserved:0&f[2]=field_species_single:9&view_name=find-a-pet&facet_field=field_species_single&display_name=page"
        # Extra headers required to not get 403, used ones from https://stackoverflow.com/questions/13303449/urllib2-httperror-http-error-403-forbidden
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'none',
               'Accept-Language': 'en-US,en;q=0.8',
               'Connection': 'keep-alive'}

        req = urllib.Request(cat_page, headers=hdr)
        page = urllib.urlopen(req)
        soup = BeautifulSoup(page, "html.parser")

        cat_names_raw = soup.find_all('h3', attrs={'class': 'item__title'})
        cat_urls_raw = soup.find_all('a', attrs={'class': 'item__link'})
        cat_names = [x.text.strip() for x in cat_names_raw]
        cat_urls = [x['href'] for x in cat_urls_raw]
        print(cat_names)
        return zip(cat_names, cat_urls)

    def check_existing(self, cat_names):
        """
        Check cat names against existing ones
        Notify when a cat is listed/de-listed
        """
        with open('cat_list.csv', mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            existings_cats = [x[0] for x in csv_reader if x != []]
            return [x for x in cat_names if x[0] not in existings_cats]

    def write_new(self, new_cats):
        with open('cat_list.csv', mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            for cat in new_cats:
                print("Write row: {}".format(cat))
                csv_writer.writerow([cat[0]])

    def send_email(self, new_cats):
        """
        Send email about new cats
        """
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(email, password)

        msg = "Subject: Cat Updates\n\n"
        for new_cat in new_cats:
            msg += new_cat[0] + ": https://www.bluecross.org.uk" + new_cat[1] + "\n"
        print(msg)
        for recipient in recipients:
            server.sendmail(email, recipient, msg)

    def run(self):
        cat_names = self.scrape_website()
        new_cats = self.check_existing(cat_names)
        if new_cats:
            self.write_new(new_cats)
            self.send_email(new_cats)

class WebScraperWoodGreen(WebScraper):
    def scrape_website(self):
        """
        Scrape websites for cat names
        returns:
        [[<cat name>, <cat page url>],..]
        """
        cat_page = "https://www.bluecross.org.uk/rehome/cat?f[0]=field_centre_single:154&f[1]=field_reserved:0&f[2]=field_species_single:9&view_name=find-a-pet&facet_field=field_species_single&display_name=page"
        # Extra headers required to not get 403, used ones from https://stackoverflow.com/questions/13303449/urllib2-httperror-http-error-403-forbidden
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'none',
               'Accept-Language': 'en-US,en;q=0.8',
               'Connection': 'keep-alive'}

        req = urllib.Request(cat_page, headers=hdr)
        page = urllib.urlopen(req)
        soup = BeautifulSoup(page, "html.parser")

        cat_names_raw = soup.find_all('h3', attrs={'class': 'item__title'})
        cat_urls_raw = soup.find_all('a', attrs={'class': 'item__link'})
        cat_names = [x.text.strip() for x in cat_names_raw]
        cat_urls = [x['href'] for x in cat_urls_raw]
        print(cat_names)
        return zip(cat_names, cat_urls)


if __name__ == "__main__":
    scraper = webScraper()
    scraper.run()