import os
import platform

def get_ffmpeg_path(base_path):
    os_system = platform.system()

    if os_system == "Windows":
        ffmpeg_path = base_path / "ffmpeg-7.1-essentials_build/bin/ffmpeg.exe"
    elif os_system == "Darwin":  # macOS
        ffmpeg_path = "/usr/local/bin/ffmpeg"
    elif os_system == "Linux": #linux
        ffmpeg_path = "/usr/bin/ffmpeg"
    else:
        raise Exception("Sistema operativo no soportado o no detectado.")

    if not os.path.exists(ffmpeg_path):
        raise Exception(f"ffmpeg no encontrado en la ruta: {ffmpeg_path}")

    return ffmpeg_path
