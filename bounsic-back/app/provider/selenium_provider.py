import asyncio

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import logging
from functools import lru_cache


# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SeleniumFacade:
    _instance = None
    _driver = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SeleniumFacade, cls).__new__(cls)
            cls._initialize_driver()
        return cls._instance
    
    @classmethod
    def _initialize_driver(cls):
        """Inicializa el navegador una sola vez"""
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        
        try:
            cls._driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )
            logger.info("Navegador Chrome inicializado")
        except Exception as e:
            logger.error(f"Error al inicializar el navegador: {str(e)}")
            raise
    
    @classmethod
    def get_driver(cls):
        """Obtiene la instancia del navegador"""
        if cls._driver is None:
            cls._initialize_driver()
        return cls._driver
    
    @classmethod
    def close_driver(cls):
        """Cierra el navegador"""
        if cls._driver:
            cls._driver.quit()
            cls._driver = None
            logger.info("Navegador Chrome cerrado")
    

    @lru_cache(maxsize=100)
    def search_lyrics_link(self, song_name: str, artist: str) -> str:
        """
        Busca la canción en letras.com y retorna el enlace del primer resultado.
        """
        try:
            search_url = f"https://www.letras.com/?q={song_name}-{artist}"
            self.get_driver().get(search_url)

            first_result = WebDriverWait(self.get_driver(), 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.gsc-webResult.gsc-result a.gs-title"))
            )
            return first_result.get_attribute('href')
        
        except TimeoutException:
            return "No se encontraron resultados para la búsqueda"
        except Exception as e:
            return f"Error: {str(e)}"