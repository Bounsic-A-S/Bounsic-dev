import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

def crawler(url, visited=None):
    if visited is None:
        visited = set()
    if url in visited or len(visited) >= 30:
        return visited
    
    visited.add(url)

    try:
        # Descargar el contenido de la página
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extraer y seguir enlaces
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(url, href)  # Primero construimos la URL completa
            # Ensure it's a valid song URL: "/artist/song/"
            if full_url.startswith("https://www.letras.com/"):
                if re.match(r"^https://www\.letras\.com/[\w-]+/[\w-]+/$", full_url):
                    if full_url not in visited:
                        print("Encontrado:", full_url)
                        visited.update(crawler(full_url, visited))  # Captura los nuevos resultados


    except Exception as e:
        print(f"Error al acceder a {url}: {e}")
    print("--------------------------------")
    print(visited)
    return visited

# crawler("https://www.letras.com/kendrick-lamar")
