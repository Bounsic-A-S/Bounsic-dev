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
            options = webdriver.ChromeOptions()
            options.add_argument('--headless=new')  
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-infobars')
            options.add_argument('--log-level=3')
            
            service = Service()  # Ajusta esto si tienes un chromedriver específico
            cls._driver = webdriver.Chrome(service=service, options=options)
            cls._driver.set_page_load_timeout(15)
            logger.info("✅ Navegador Chrome inicializado correctamente")
            
        except Exception as e:
            logger.error(f"❌ Error al inicializar el navegador: {str(e)}")
            raise

    @classmethod
    def get_driver(cls):
        """Obtiene la instancia del navegador, reiniciando si está cerrada"""
        if cls._driver is None or cls._driver.session_id is None:
            logger.warning("⚠️ Sesión de Selenium cerrada. Reiniciando...")
            cls._initialize_driver()
        return cls._driver
    
    @classmethod
    def close_driver(cls):
        """Cierra el navegador"""
        if cls._driver:
            cls._driver.quit()
            cls._driver = None
            logger.info("✅ Navegador Chrome cerrado")
    
    @lru_cache(maxsize=100)
    def search_lyrics_link(self, song_name: str, artist: str) -> str:
        driver = self.get_driver()
        try:
            search_url = f"https://www.letras.com/?q={song_name}-{artist}"
            driver.get(search_url)
            self.load_cookies(url=search_url)

            if self.is_captcha_present(driver):
                if not self.click_basic_captcha(driver):
                    logger.warning("⚠️ No se pudo completar el CAPTCHA.")
                    return "No se pudo completar el CAPTCHA"
                time.sleep(random.uniform(1, 3))

            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.gsc-webResult"))
            )
            results = driver.find_elements(By.CSS_SELECTOR, "div.gsc-webResult.gsc-result a.gs-title")
            if results:
                return results[0].get_attribute("href")
            else:
                logger.warning("❌ No se encontraron resultados")
                return "letra no disponible en el momento"

        except (TimeoutException, NoSuchElementException):
            logger.warning("❌ No se encontraron resultados visibles")
            return "No se encontraron resultados visibles"
        except Exception as e:
            logger.error(f"❌ Error inesperado: {str(e)}")
            self.handle_driver_error()
            return f"Error inesperado: {str(e)}"

    def handle_driver_error(self):
        """Reinicia la sesión de Selenium en caso de error"""
        logger.warning("⚠️ Reiniciando sesión de Selenium...")
        self.close_driver()
        self._initialize_driver()
    
    def is_captcha_present(self, driver):
        try:
            return bool(driver.find_elements(By.CSS_SELECTOR, "iframe[title='reCAPTCHA']"))
        except Exception as e:
            logger.warning(f"❌ Error al verificar el CAPTCHA: {e}")
            return False

    def click_basic_captcha(self, driver):
        try:
            iframe = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title='reCAPTCHA']"))
            )
            driver.switch_to.frame(iframe)
            captcha_checkbox = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "recaptcha-anchor"))
            )
            actions = ActionChains(driver)
            actions.move_to_element(captcha_checkbox).click().perform()
            logger.info("✅ CAPTCHA básico clickeado correctamente")
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
