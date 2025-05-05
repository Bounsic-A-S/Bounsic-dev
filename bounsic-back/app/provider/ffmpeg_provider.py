import os
import platform

def get_ffmpeg_path(base_path):
    os_system = platform.system()

    if os_system == "Windows":
        ffmpeg_path = base_path.parent.parent / "ffmpeg-7.1-essentials_build/bin/ffmpeg.exe"
        ffprobe_path = base_path.parent.parent / "ffmpeg-7.1-essentials_build/bin/ffprobe.exe"
    elif os_system == "Darwin":  # macOS
        ffmpeg_path = "/usr/local/bin/ffmpeg"
        ffprobe_path = "/usr/local/bin/ffprobe"
    elif os_system == "Linux":
        ffmpeg_path = "/usr/bin/ffmpeg"
        ffprobe_path = "/usr/bin/ffprobe"
    else:
        raise Exception("Sistema operativo no soportado o no detectado.")

    if not os.path.exists(ffmpeg_path) or not os.path.exists(ffprobe_path):
        raise Exception(f"ffmpeg o ffprobe no encontrado en las rutas: {ffmpeg_path}, {ffprobe_path}")

    return ffmpeg_path, ffprobe_path


