import requests
from bs4 import BeautifulSoup

def scrapping (url):
    print("HOLAAAAAAAAAAAA")
    response = requests.get(url)

    response

    soup = BeautifulSoup(response.text, 'html.parser')

    titulo = soup.title.text
    print("Título de la página:", titulo)


    enlaces = soup.find_all('a')
    for enlace in enlaces:
        print(enlace.get('href'))