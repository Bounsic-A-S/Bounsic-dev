import requests
from pathlib import Path
import yt_dlp
import re
from app.provider import get_ffmpeg_path
import asyncio
from playwright.async_api import async_playwright



def sanitize_filename(text):
    # Reemplaza los caracteres inválidos por guiones bajos o vacíos
    return re.sub(r'[<>:"/\\|?*]', '', text)

async def scrappingBueno(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(url, timeout=30000)
        await page.wait_for_selector("h1.title", timeout=10000)

        # ============ Meta info ============
        title = await page.title()
        description = await page.get_attribute('meta[name="description"]', "content") or "No encontrada"
        thumbnail = await page.get_attribute('link[rel="image_src"]', "href") or "No encontrada"
        channel_name = await page.get_attribute('link[itemprop="name"]', "content") or "No encontrado"
        channel_id = await page.get_attribute('meta[itemprop="channelId"]', "content") or "No encontrado"
        publish_date = await page.get_attribute('meta[itemprop="datePublished"]', "content") or "No encontrada"
        keywords = await page.get_attribute('meta[name="keywords"]', "content")
        tags = keywords.split(", ") if keywords else ["No hay etiquetas"]

        # ============ Datos visibles en pantalla ============
        title_text = await page.locator("h1.title").text_content() or "No disponible"
        views_text = await page.locator("span.view-count").text_content() or "No disponible"
        likes_text = await page.locator("yt-formatted-string#text.style-scope.ytd-toggle-button-renderer").nth(0).text_content() or "No disponible"
        channel_url = await page.locator("ytd-channel-name a").get_attribute("href") or "No disponible"
        subscriber_count = await page.locator("yt-formatted-string#owner-sub-count").text_content() or "No disponible"

        # ============ HTML para inspección ============
        body_html = await page.content()

        await browser.close()

        return {
            "meta": {
                "title": title,
                "description": description,
                "thumbnail": thumbnail,
                "channel_name": channel_name,
                "channel_id": channel_id,
                "publish_date": publish_date,
                "tags": tags
            },
            "rendered": {
                "title_text": title_text,
                "views_text": views_text,
                "likes_text": likes_text,
                "channel_url": f"https://www.youtube.com{channel_url}",
                "subscriber_count": subscriber_count
            },
            "debug_html_snippet": body_html[:3000]  # Primeros 3000 caracteres del HTML para explorar
        }



def descargar_audio(url):
    base_path = Path(__file__).resolve().parent

    audio_dir = base_path / "audios"
    image_dir = base_path / "images"

    audio_dir.mkdir(parents=True, exist_ok=True)
    image_dir.mkdir(parents=True, exist_ok=True)


    ffmpeg_path, ffprobe_path = get_ffmpeg_path(base_path)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': str(audio_dir / "%(title)s.%(ext)s"),
        'ffmpeg_location': str(ffmpeg_path),
    }

    

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

            video_title = info.get("title", "unknown").replace("/", "-")

            
            downloaded_file = audio_dir / f"{video_title}.mp3"
            print(f"Archivo esperado: {downloaded_file}")


            image_url = info.get("thumbnail")
            if image_url:
                image_path = image_dir / f"{video_title}.jpg"
                response = requests.get(image_url)
                if response.status_code == 200:
                    with open(image_path, "wb") as thumb_file:
                        thumb_file.write(response.content)
                    print(f"Thumbnail guardado en: {image_path}")
                else:
                    print("No se pudo descargar la imagen")

            if downloaded_file.exists():
                return {
                    "audio": str(downloaded_file),
                    "thumbnail": str(image_path) if image_url else None
                }
        return None

    except Exception as e:
        print(f"Error en la descarga: {e}")
        return None


async def buscar_en_youtube(query):
    async with async_playwright() as p:  
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(f"https://www.youtube.com/results?search_query={query}")
        await page.wait_for_selector("ytd-video-renderer a#video-title", timeout=10000)

        first_result = await page.query_selector("ytd-video-renderer a#video-title")
        url = "https://www.youtube.com" + await first_result.get_attribute("href")

        await browser.close()
        return url





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


