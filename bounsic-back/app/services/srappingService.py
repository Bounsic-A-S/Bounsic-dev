import requests
from bs4 import BeautifulSoup
import os
from pathlib import Path
import yt_dlp

def scrappingBueno():
    print('llega')
    url = "https://www.youtube.com/watch?v=_Yhyp-_hX2s"  # URL del video

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
    while base_path.name != "bounsic-back":
        base_path = base_path.parent

    audio_dir = base_path / "audios"
    audio_dir.mkdir(parents=True, exist_ok=True)

    ffmpeg_path = base_path / "ffmpeg-7.1-essentials_build/bin/ffmpeg.exe"

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': str(audio_dir / "%(title)s.%(ext)s"),
        'ffmpeg_location': str(ffmpeg_path)
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)  

            # 🔹 Obtener el nombre del archivo esperado
            video_title = info.get("title", "unknown").replace("/", "-")  # Evita caracteres inválidos
            downloaded_file = audio_dir / f"{video_title}.mp3"
            print(f"Archivo esperado: {downloaded_file}")

            # 🔹 Verificar si el archivo existe
            if downloaded_file.exists():
                return f"Archivo descargado: {downloaded_file}"
        
        return None  

    except Exception as e:
        print(f"Error en la descarga: {e}")
        return None


# 🔍 Scraping para buscar en YouTube
def buscar_en_youtube(query):
    ydl_opts = {
        "quiet": True,
        "default_search": "ytsearch",  # Hace una búsqueda en YouTube
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)
    
    if not info["entries"]:
        return None

    first_video = info["entries"][0]  # Primer resultado de la búsqueda
    video_url = first_video["webpage_url"]  # URL completa del video

    return video_url

