"""
We collect the dataset containing the information about the dinosaurs (A - Z) from the National History Museum's website.
"""
import string
import requests, re
from bs4 import BeautifulSoup
from tqdm import tqdm

base_url = "https://www.nhm.ac.uk/discover/dino-directory/name/{}/gallery.html"
alphabets = list(string.ascii_lowercase)
header = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}

data_file = open('data.csv', 'w+')
data_file.write('name' + ',' + 'diet' + ',' + 'period' + ',' + 'lived_in' + ',' + 'type' + ',' + 'length'
                + ',' + 'taxonomy' + ',' + 'named_by' + ',' + 'species' + ',' + 'link' + '\n')

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
        lst_of_dinos = self.get_dino_urls()

        dinos = []

        for ix, dino in enumerate(lst_of_dinos):
            dino_data = {}
            
            diet_data = []
            taxonomy_data = []
            typ_length_data = []

            soup = self.read_a_page(dino)

            type_length = soup.find_all('dl', attrs={'class':'dinosaur--description dinosaur--list'})
            diet = soup.find_all('div', attrs={'class':'dinosaur--info-container small-12 medium-12 large-7 columns'})
            taxonomy = soup.find_all('div', attrs={'class':'dinosaur--taxonomy-container small-12 medium-12 large-12 columns'})
            name = dino.split('/')[-1].split('.')[0]
            
            type_ = str(type_length).split('<dd>')[-2].split('.html">')[-1].split('</a>')[0].strip()
            length = str(type_length).split('<dd>')[-1].split('</dd>')[0].strip()

            for vals in str(type_length).split('<dd>'):
                lines = vals.split('">')[-1].split('</dd>')[0].split('</a>')[0].strip()
                if not bool(BeautifulSoup(lines, "html.parser").find()):
                    if 'kg' not in lines:
                        typ_length_data.append(lines)

            for vals in str(diet).split('<dd>'):
                lines = vals.split('">')[-1].split('</a>')[0]
                period = vals.split('">')[-1].split(', ')[-1].split('</dd>')[0]
                if not bool(BeautifulSoup(lines, "html.parser").find()):
                    if lines not in period:
                        lines = lines + ' ' + period
                    diet_data.append(lines)

            for vals in str(taxonomy).split('<dd>'):
                lines = vals.split('">')[-1].split('</a>')[0].split('</dd>')[0]
                if not bool(BeautifulSoup(lines, "html.parser").find()):
                    taxonomy_data.append(lines)
           
            dino_data["name"] = name
            dino_data["diet"] = diet_data[0]
            dino_data["period"] = diet_data[1]
            try:
                dino_data["lived_in"] = diet_data[2]
            except:
                dino_data["lived_in"] = ""
            dino_data["type"] = typ_length_data[0]
            try:
                dino_data["length"] = typ_length_data[1]
            except:
                dino_data["length"] = ""
            dino_data["taxonomy"] = taxonomy_data[0]
            dino_data["named_by"] = taxonomy_data[1]
            try:
                dino_data["species"] = taxonomy_data[2]
            except:
                dino_data["species"] = ""
            dino_data['link'] = dino
            dinos.append(dino_data)
            print(dino_data)
            print('='*50)

        return dinos

for ix, alphabet in tqdm(enumerate(alphabets)):
    jr = JurassicPark(alphabet)
    dinos = jr.get_dino_data_per_url()
    
    for jx, dino in enumerate(dinos):
        name = dino["name"].replace(',', '')
        diet = dino["diet"].replace(',', '')
        period = dino["period"].replace(',', '')
        lived_in = dino["lived_in"].replace(',', '')
        typ = dino["type"].replace(',', '')
        length = dino["length"].replace(',', '')
        taxonomy = dino["taxonomy"].replace(',', '')
        named_by = dino["named_by"].replace(',', '')
        species = dino["species"].replace(',', '')
        link = dino["link"].replace(',', '')

        data_file.write(name + ',' + diet + ',' + period + ','
                + lived_in + ',' + typ + ',' + length + ',' + 
                taxonomy + ',' + named_by + ',' + species + ',' + link)
        data_file.write('\n')
    
data_file.close()