"""
We collect the dataset containing the information about the dinosaurs (A - Z) from the National History Museum's website.
"""
import string
import requests, re
from bs4 import BeautifulSoup

base_url = "https://www.nhm.ac.uk/discover/dino-directory/name/{}/gallery.html"
list_of_a_z = list(string.ascii_lowercase)
header = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}

class JurassicPark:
    def __init__(self, letter):
        self.letter = letter

    def read_a_page(self, link):
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup
    
    def get_dino_urls(self):
        lst_of_dinos = []
        url = base_url.format(self.letter)
        soup = self.read_a_page(url)
        dino_urls = soup.find_all('li', attrs={'class':'dinosaurfilter--dinosaur'})
        for ix, dino_url in enumerate(dino_urls):
            dino_link = str(dino_url).split('href')[-1].split('">\n')[0].replace('="', '')
            lst_of_dinos.append(dino_link)

        return lst_of_dinos
    
    def get_dino_data_per_url(self):
        dino_data = {}

        lst_of_dinos = self.get_dino_urls()
        for ix, dino in enumerate(lst_of_dinos):
            soup = self.read_a_page(dino)
            info = soup.find_all('div', attrs={'class':'row'})
            type_length = soup.find_all('dl', attrs={'class':'dinosaur--description dinosaur--list'})
            diet = soup.find_all('div', attrs={'class':'dinosaur--info-container small-12 medium-12 large-7 columns'})
            taxonomy = soup.find_all('div', attrs={'class':'dinosaur--taxonomy-container small-12 medium-12 large-12 columns'})

            print(ix, dino)
            print(type_length)
            print(diet)
            print(taxonomy)
            exit()

jr = JurassicPark("a")
jr.get_dino_data_per_url()