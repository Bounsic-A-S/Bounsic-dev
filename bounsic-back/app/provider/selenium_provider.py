from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
from functools import lru_cache
import time
import random
import pickle
import os
from selenium.webdriver import ActionChains


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
        """Inicializa el navegador Chrome con configuración anti-detección"""
        try:
            # Crear opciones de Chrome
            options = webdriver.ChromeOptions()
            
            # ===== CONFIGURACIÓN ESENCIAL =====
            # Modo headless (descomentar para producción)
            options.add_argument('--headless=new')  
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            # ===== EVITAR DETECCIÓN =====
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # ===== OPTIMIZACIONES =====
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-infobars')
            options.add_argument('--log-level=3')
            
            # ===== INICIALIZACIÓN ESTÁNDAR =====
            # Si tienes un chromedriver descargado manualmente, especifica la ruta aquí
            # chrome_path = "C:/ruta/a/tu/chromedriver.exe"  # Cambia esto a tu ruta
            # service = Service(chrome_path)
            
            # Si prefieres que selenium busque el chromdriver automáticamente:
            service = Service()
            
            cls._driver = webdriver.Chrome(service=service, options=options)
            
            # Stealth script
            cls._driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                """
            })
            
            logger.info("Navegador Chrome inicializado correctamente")
            
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
        driver = self.get_driver()
        try:
            # Formar la URL de búsqueda
            search_url = f"https://www.letras.com/?q={song_name}-{artist}"
            driver.get(search_url)
            self.load_cookies(url=search_url)


            # Buscar si está el CAPTCHA
            captcha_present = self.is_captcha_present(driver)
            
            if captcha_present:
                # Intentar clic en CAPTCHA si aparece
                if not self.click_basic_captcha(driver):
                    logger.warning("⚠️ No se pudo completar el CAPTCHA.")
                    return "No se pudo completar el CAPTCHA"
                # Después de resolver el CAPTCHA, esperar unos segundos adicionales
                time.sleep(random.uniform(1, 3))

            # Esperar a que los resultados sean visibles
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.gsc-webResult"))
            )

            # Obtener los resultados de búsqueda
            results = driver.find_elements(By.CSS_SELECTOR, "div.gsc-webResult.gsc-result a.gs-title")
            if results:
                return results[0].get_attribute("href")
            else:
                logger.warning("❌ No se encontraron resultados")
                return "letra no disponible en el momento"

        except TimeoutException:
            logger.warning("⚠️ Timeout: No se encontraron resultados visibles")
            return "Timeout: No se encontraron resultados visibles"
        except NoSuchElementException:
            logger.warning("❌ No se encontró el elemento de resultados")
            return "No se encontró el elemento de resultados"
        except Exception as e:
            logger.error(f"❌ Error inesperado: {str(e)}")
            return f"Error inesperado: {str(e)}"
        
    def is_captcha_present(self, driver):
        try:
            # Verificar si el iframe del reCAPTCHA está presente con find_elements (más rápido)
            if driver.find_elements(By.CSS_SELECTOR, "iframe[title='reCAPTCHA']"):
                return True
            return False
        except Exception as e:
            logger.warning(f"❌ Error al verificar el CAPTCHA: {e}")
            return False

    def click_basic_captcha(self, driver):
        try:
            # Esperar al iframe del reCAPTCHA
            iframe = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title='reCAPTCHA']"))
            )
            driver.switch_to.frame(iframe)

            # Esperar al checkbox dentro del iframe
            captcha_checkbox = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "recaptcha-anchor"))
            )

            # Clic usando ActionChains
            actions = ActionChains(driver)
            actions.move_to_element(captcha_checkbox).click().perform()

            logger.info("✅ CAPTCHA básico clickeado correctamente")

            # Volver al contenido principal
            driver.switch_to.default_content()
            return True

        except TimeoutException:
            logger.warning("⚠️ CAPTCHA no apareció en el tiempo esperado")
            return False
        except Exception as e:
            logger.warning(f"❌ Error al intentar clic en el CAPTCHA: {e}")
            return False
        
    def save_cookies(self, path="cookies.pkl"):
        with open(path, "wb") as f:
            pickle.dump(self._driver.get_cookies(), f)

    def load_cookies(self, url, path="cookies.pkl"):
        try:
            if os.path.exists(path):
                for cookie in pickle.load(open(path, "rb")):
                    try:
                        self._driver.add_cookie(cookie)
                    except Exception:
                        pass
            self._driver.get(url)
            self._driver.refresh()
        except Exception as e:
            logger.error(f"Error cargando cookies: {e}")