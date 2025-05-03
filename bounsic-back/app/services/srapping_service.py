import requests
from bs4 import BeautifulSoup
from pathlib import Path
import yt_dlp
import re
from app.provider import get_ffmpeg_path, SeleniumFacade
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
import random
from urllib.parse import urlparse

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def sanitize_filename(text):
    # Reemplaza los caracteres inválidos por guiones bajos o vacíos
    return re.sub(r'[<>:"/\\|?*]', '', text)

def clean_song_title(title):
    # Expresiones regulares para patrones comunes
    patterns_to_remove = [
        r'[\(\[].*?[\)\]]',  # Elimina texto entre paréntesis/corchetes
        r'[\ᴰᴴᵃᵇᶜ]',          # Elimina caracteres especiales como ᴴᴰ
        r'\b(HD|MV|Official Video|Video Oficial|Lyrics?|4K|FULL)\b',
        r'[^\w\s]',          # Elimina caracteres no alfanuméricos (excepto espacios)
        r'\s+',              # Reemplaza múltiples espacios con uno solo
    ]
    
    cleaned_title = title
    for pattern in patterns_to_remove:
        cleaned_title = re.sub(pattern, ' ', cleaned_title, flags=re.IGNORECASE)
    
    # Limpieza final
    cleaned_title = cleaned_title.strip()  # Elimina espacios al inicio/final
    return cleaned_title

def scrappingBueno(url):


    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extraer el título del video
    title = soup.find("title").text if soup.find("title") else "Título no encontrado"

    # Extraer la descripción del video
    description = soup.find("meta", {"name": "description"})
    description = description["content"] if description else "Descripción no encontrada"

    # Extraer la miniatura del video
    thumbnail = soup.find("link", {"rel": "image_src"})
    thumbnail = thumbnail["href"] if thumbnail else "Miniatura no encontrada"

    # Extraer el nombre del canal
    channel_name = soup.find("link", {"itemprop": "name"})
    channel_name = channel_name["content"] if channel_name else "Canal no encontrado"

    # Extraer la ID del canal
    channel_id = soup.find("meta", {"itemprop": "channelId"})
    channel_id = channel_id["content"] if channel_id else "ID de canal no encontrado"

    # Extraer la fecha de publicación
    publish_date = soup.find("meta", {"itemprop": "datePublished"})
    publish_date = publish_date["content"] if publish_date else "Fecha de publicación no encontrada"

    # Extraer etiquetas del video (tags)
    tags = soup.find("meta", {"name": "keywords"})
    tags = tags["content"].split(", ") if tags else ["No hay etiquetas"]

    # Imprimir toda la página (para inspeccionar)
    print(soup.prettify())

    return {
        "title": title,
        "description": description,
        "thumbnail": thumbnail,
        "channel_name": channel_name,
        "channel_id": channel_id,
        "publish_date": publish_date,
        "tags": tags
    }




async def descargar_audio(url, safe_name: str):
    base_path = Path(__file__).resolve().parent
    audio_dir = base_path / "audios"
    audio_dir.mkdir(parents=True, exist_ok=True)

    ffmpeg_path, ffprobe_path = get_ffmpeg_path(base_path)
    
    # Remove the file extension from safe_name for the outtmpl
    safe_name_without_ext = safe_name.rsplit('.', 1)[0]
    
    # Set the output template to directly use our safe_name
    output_path = str(audio_dir / safe_name_without_ext)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        # Use our safe filename directly in the output template
        'outtmpl': f"{output_path}.%(ext)s",
        'ffmpeg_location': str(ffmpeg_path),
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
            # The file should now be saved with the safe_name
            final_file = audio_dir / safe_name
            print(f"Archivo descargado como: {final_file}")
            
            if final_file.exists():
                return {
                    "audio": str(final_file),
                }
            else:
                # If the file doesn't exist with safe_name, let's check if it used the default naming
                video_title = info.get("title", "unknown").replace("/", "-")
                potential_file = audio_dir / f"{video_title}.mp3"
                if potential_file.exists():
                    # Try renaming as a fallback
                    potential_file.rename(final_file)
                    print(f"Archivo renombrado fallback a: {final_file}")
                    return {
                        "audio": str(final_file),
                    }
                
                print(f"¡Alerta! No se encontró el archivo descargado en: {final_file}")
        
        return None

    except Exception as e:
        print(f"Error en la descarga: {e}")
        return None

def buscar_en_youtube(query):
    
    print("DEBUG: Archivo cookies existe:", os.path.exists("cookies/cookies.txt"))
    print("DEBUG: Archivos en carpeta cookies:", os.listdir("cookies"))

    ydl_opts = {
        "quiet": False,
        "verbose": True,
        "default_search": "ytsearch",
        "noplaylist": True,
        "cookiesfromfile": "./cookies/www.youtube.com_cookies.txt",
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)
        
        if not info["entries"]:
            return None

        video = info["entries"][0]
        print(f"DEBUG: Video encontrado - {video['title']}")

        # Extraer artista y título (heurística simple)
        video_title = video.get("title", "")
        artist = query.split()[0]  # Primera palabra de la query como artista
        title = " ".join(query.split()[1:])  # Resto como título

        # Si el título de YouTube contiene "-", dividirlo
        if "-" in video_title:
            parts = [p.strip() for p in video_title.split("-", 1)]
            if len(parts) == 2:
                artist, title = parts

        return {
            "url": video["webpage_url"],
            "title": title,
            "artist": artist
        }

    except Exception as e:
        print(f"ERROR en buscar_en_youtube: {str(e)}")
        return None


def descargar_imagen(url, title):
    response = requests.get(url, stream=True)
    
    if response.status_code == 200:
        # 🔹 Extraer la extensión de la imagen de la URL
        match = re.search(r"\.(jpg|jpeg|png|gif)", url)
        extension = match.group(1) if match else "jpg"  # Si no encuentra extensión, usa jpg

        # 🔹 Definir el directorio base
        base_path = Path(__file__).resolve().parent
        while base_path.name != "bounsic-back":
            base_path = base_path.parent

        image_dir = base_path / "images"  # Directorio para imágenes
        image_dir.mkdir(parents=True, exist_ok=True)

        # 🔹 Sanitizar nombres
        title = sanitize_filename(title)

        # 🔹 Generar el nombre del archivo: "Título - Artista.ext"
        image_filename = f"{title}.{extension}"
        image_path = image_dir / image_filename  # Definir la ruta completa

        # 🔹 Guardar imagen
        with open(image_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        return str(image_path)  # Devuelve la ruta de la imagen

    return None  # Retorna None si la descarga falla


def limpiar_url(url):
    parsed = urlparse(url)
    partes = parsed.path.split("/")
    nueva_ruta = "/".join(partes[:3]) if len(partes) >= 3 else parsed.path
    return f"{parsed.scheme}://{parsed.netloc}{nueva_ruta}"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.105 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
]

BASE_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": "https://www.google.com/",
    "DNT": "1"
}


async def get_lyrics(song_name: str, artist: str):
    facade = SeleniumFacade()
    search_url = await get_lyrics1(song_name, artist, facade)
    if not search_url:
        return None
    url = limpiar_url(search_url)
    print(url)

    lyrics = await get_lyrics_bs(url)
    if lyrics:
        print(f"⚠️ Letra obtenida (BeautifulSoup): {song_name}")
        return lyrics

    driver = facade.get_driver()
    lyrics = await get_lyrics_selenium(url, driver)
    if lyrics:
        print(f"✅ Letra obtenida (Selenium): {song_name}")
        return lyrics

    print(f"❌ Letra no encontrada: {song_name}")
    return None

async def get_lyrics_bs(url):
    try:
        headers = {
            **BASE_HEADERS,
            "User-Agent": random.choice(USER_AGENTS)
        }
        response = requests.get(url, headers=headers, timeout=8)
        soup = BeautifulSoup(response.text, "html.parser")
        lyric_div = soup.find("div", class_="lyric-original")
        if lyric_div:
            return "\n\n".join(p.get_text("\n") for p in lyric_div.find_all("p")).strip()
        return None
    except Exception as e:
        print(f"❌ Error con BeautifulSoup: {e}")
        return None

async def get_lyrics_selenium(url, driver):
    try:
        driver.get(url)
        lyric_div = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.lyric-original"))
        )
        html = lyric_div.get_attribute("innerHTML")
        soup = BeautifulSoup(html, "html.parser")
        return "\n\n".join(p.get_text("\n") for p in soup.find_all("p")).strip()
    except Exception as e:
        print(f"❌ Error con Selenium: {e}")
        return None


# Executor global
executor = ThreadPoolExecutor(max_workers=6)

async def get_lyrics1(song_name: str, artist: str, facade: SeleniumFacade):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, facade.search_lyrics_link, song_name, artist)



