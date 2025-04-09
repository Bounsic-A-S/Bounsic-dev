import requests
from bs4 import BeautifulSoup
from pathlib import Path
import yt_dlp
import re
from app.provider import get_ffmpeg_path

def sanitize_filename(text):
    # Reemplaza los caracteres inválidos por guiones bajos o vacíos
    return re.sub(r'[<>:"/\\|?*]', '', text)

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

# 🔍 Scraping para buscar en YouTube
def buscar_en_youtube(query):

    ydl_opts = {
        "quiet": False,
        "verbose": True,
        "default_search": "ytsearch",
        "noplaylist": True,
        "cookiefile": "./cookies/cookies.txt",
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)
    
    if not info["entries"]:
        return None

    first_video = info["entries"][0]  # Primer resultado de la búsqueda
    video_url = first_video["webpage_url"]  # URL completa del video

    return video_url


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


