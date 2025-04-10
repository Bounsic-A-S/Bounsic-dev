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
        print("🚀 Iniciando navegador...")
        browser = await p.chromium.launch(headless=False)  # Cambiado a False para depuración
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        page = await context.new_page()
        
        try:
            print(f"🌐 Navegando a URL: {url}")
            await page.goto(url, timeout=60000)
            
            # Espera a que el contenido principal esté visible
            print("⏳ Esperando a que cargue el contenido...")
            try:
                await page.wait_for_selector("h1.title", state="visible", timeout=30000)
                print("✅ Contenido principal cargado")
            except Exception as e:
                print(f"❌ No se encontró h1.title: {str(e)}")
                print("📄 HTML de la página (primeros 1000 caracteres):")
                print((await page.content())[:1000])
                raise

            # ============ [DEBUG] Mostrar metadatos disponibles ============
            print("\n🔍 Buscando metadatos...")
            meta_tags = await page.query_selector_all('meta')
            print(f"📊 {len(meta_tags)} meta tags encontrados en la página")
            for i, tag in enumerate(meta_tags[:10]):  # Mostrar solo los primeros 10
                name = await tag.get_attribute("name") or await tag.get_attribute("itemprop") or "sin nombre"
                content = await tag.get_attribute("content") or "sin contenido"
                print(f"  {i+1}. {name} = {content}")

            # ============ Función auxiliar con depuración ============
            async def get_meta_attr(selector, attr, nombre=""):
                try:
                    print(f"\n🔎 Buscando: {nombre} ({selector})")
                    element = await page.query_selector(selector)
                    if not element:
                        print(f"⚠️ Elemento no encontrado: {selector}")
                        return "No encontrado"
                    
                    value = await element.get_attribute(attr)
                    print(f"✔️ Encontrado: {value}")
                    return value or "No encontrado"
                except Exception as e:
                    print(f"❌ Error al obtener {selector}: {str(e)}")
                    return "No encontrado"

            # ============ Meta info ============
            print("\n📦 Extrayendo metadatos...")
            title = await page.title()
            print(f"📌 Título de la página: {title}")
            
            description = await get_meta_attr('meta[name="description"]', "content", "Descripción")
            thumbnail = await get_meta_attr('link[rel="image_src"]', "href", "Miniatura")
            channel_name = await get_meta_attr('link[itemprop="name"]', "content", "Nombre del canal")
            channel_id = await get_meta_attr('meta[itemprop="channelId"]', "content", "ID del canal")
            publish_date = await get_meta_attr('meta[itemprop="datePublished"]', "content", "Fecha de publicación")
            
            keywords = await get_meta_attr('meta[name="keywords"]', "content", "Palabras clave")
            tags = keywords.split(", ") if keywords and keywords != "No encontrado" else ["No hay etiquetas"]

            # ============ [DEBUG] Mostrar selectores importantes ============
            print("\n👀 Verificando selectores clave:")
            selectores_clave = {
                "Título visible": "h1.title",
                "Visitas": "span.view-count",
                "Likes": "yt-formatted-string#text.style-scope.ytd-toggle-button-renderer",
                "URL del canal": "ytd-channel-name a",
                "Suscriptores": "yt-formatted-string#owner-sub-count"
            }
            
            for nombre, selector in selectores_clave.items():
                exists = await page.query_selector(selector)
                print(f"  {'✅' if exists else '❌'} {nombre.ljust(15)}: {selector}")

            # ============ Datos visibles ============
            print("\n📊 Extrayendo datos visibles...")
            title_locator = page.locator("h1.title")
            title_text = await title_locator.text_content() if await title_locator.count() > 0 else "No disponible"
            print(f"  Título: {title_text}")

            views_locator = page.locator("span.view-count")
            views_text = await views_locator.text_content() if await views_locator.count() > 0 else "No disponible"
            print(f"  Visitas: {views_text}")

            likes_locator = page.locator("yt-formatted-string#text.style-scope.ytd-toggle-button-renderer").nth(0)
            likes_text = await likes_locator.text_content() if await likes_locator.count() > 0 else "No disponible"
            print(f"  Likes: {likes_text}")

            channel_url_locator = page.locator("ytd-channel-name a")
            channel_url = await channel_url_locator.get_attribute("href") if await channel_url_locator.count() > 0 else "No disponible"
            print(f"  URL del canal: {channel_url}")

            subs_locator = page.locator("yt-formatted-string#owner-sub-count")
            subscriber_count = await subs_locator.text_content() if await subs_locator.count() > 0 else "No disponible"
            print(f"  Suscriptores: {subscriber_count}")

            # ============ HTML para inspección ============
            body_html = await page.content()
            print("\n🔧 Extracción completada")

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
                    "channel_url": f"https://www.youtube.com{channel_url}" if channel_url != "No disponible" else "No disponible",
                    "subscriber_count": subscriber_count
                },
                "debug_html_snippet": body_html[:3000]
            }

        except Exception as e:
            print(f"\n🔥 ERROR CRÍTICO: {str(e)}")
            print("🔄 Intentando capturar HTML para diagnóstico...")
            try:
                error_html = await page.content()
                with open("error_debug.html", "w", encoding="utf-8") as f:
                    f.write(error_html)
                print("📄 Se guardó HTML de error en 'error_debug.html'")
            except:
                print("❌ No se pudo capturar el HTML")
            
            await browser.close()
            return {
                "error": str(e),
                "message": "Consulta el archivo error_debug.html para diagnóstico"
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


