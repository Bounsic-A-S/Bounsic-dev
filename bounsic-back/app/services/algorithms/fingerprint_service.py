import os
import librosa
import json
import numpy as np
from scipy.signal import find_peaks
# from app.provider import AZURE_CONNECTION_STRING, AZURE_CONTAINER_NAME
# from azure.storage.blob import BlobServiceClient
# from app.provider import db

def generate_fingerprint(songName: str):
    try:
        archivo_audio = os.path.join("app", "services", "songs", f"{songName}.mp3")
        songName = os.path.splitext(os.path.basename(archivo_audio))[0]

        # Read audio
        y, sr = librosa.load(archivo_audio, sr=None)
        
        D = np.abs(librosa.stft(y))
        D_dB = librosa.amplitude_to_db(D, ref=np.max)

        frequencies = librosa.fft_frequencies(sr=sr) # Get frequencies in Hz
        fingerprint = _analyze_frequencies(D_dB=D_dB, frequencies=frequencies)

        save_json(fingerprint=fingerprint, songName=songName)
        return True
    except:
        print("Error generating fingerprint.")
        return False

def _analyze_frequencies(D_dB, frequencies):
    fingerprint = []

    # Iterar sobre cada fragmento amplio del espectrograma
    for t in range(0, D_dB.shape[1], 100):  # 100 windows
        espectro_tiempo = D_dB[:, t]  # Espectro en el tiempo t
        picos, _ = find_peaks(espectro_tiempo, height=np.percentile(espectro_tiempo, 97))
        
        # Save only 2 frequencies per time fragment
        if len(picos) > 0:
            top_frequencies = sorted(picos, key=lambda p: espectro_tiempo[p], reverse=True)[:2]
            fingerprint.append([round(frequencies[p], 1) for p in top_frequencies])

    return fingerprint

def save_json(fingerprint, songName: str):
    saveIn = "fingerprints"
    os.makedirs(saveIn, exist_ok=True)

    ruta_json = os.path.join("app", "services", saveIn, f"{songName}.json")
    with open(ruta_json, "w", encoding="utf-8") as f:
        json.dump(fingerprint, f, indent=4)

    print(f"✅ Huella digital guardada en: {ruta_json}")

def readFingerprint(songName: str) -> list[tuple[float, float]]:
    ruta_json = os.path.join("app", "services", "fingerprints", f"{songName}.json")
    
    with open(ruta_json, "r", encoding="utf-8") as file:
        fingerprint_data = json.load(file)

    frequency_pairs = [tuple(pair) for pair in fingerprint_data]

    # print("Primeros pares de frecuencias:")
    # for pair in frequency_pairs[:5]:
    #     print(f"F1: {pair[0]} Hz, F2: {pair[1]} Hz")
    return frequency_pairs

# def main():
#     # generate_fingerprint()
#     readFingerprint()
# if __name__ == "__main__":
#     main()
