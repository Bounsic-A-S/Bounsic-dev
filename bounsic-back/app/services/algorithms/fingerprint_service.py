import os
from typing import List, TypedDict
import librosa
import json
import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
# from app.provider import AZURE_CONNECTION_STRING, AZURE_CONTAINER_NAME
# from azure.storage.blob import BlobServiceClient
# from app.provider import db

class FrequencyRanges(TypedDict):
    bajos: float
    medios: float
    altos: float
class FrequencyData(TypedDict):
    time: float
    frequencies: FrequencyRanges
    amplitudes: FrequencyRanges
class FingerprintData(TypedDict):
    bpm: float
    frequencies: List[FrequencyData]
    distribution: FrequencyRanges

def generate_fingerprint(songName: str, segment_duration: float = 0.5, top_n_freqs: int = 1):
    try:
        songName = songName.lower()
        song_path = os.path.join("app", "services", "songs", f"{songName}.mp3")
        if not os.path.exists(song_path):
            raise FileNotFoundError(f"Audio file not found: {song_path}")

        # Read and normalize audio
        y, sr = librosa.load(song_path, sr=None)
        y = librosa.util.normalize(y)
        bpm, _ = librosa.beat.beat_track(y=y, sr=sr)

        # Calculate STFT
        n_fft = 2048  # More frequency bins
        hop_length = n_fft // 4
        D = np.abs(librosa.stft(y, n_fft=n_fft, hop_length=hop_length))
        # Frecuencia  1    2    3    4    5    ...   n_frames
        # ---------------------------------------------------
        # 0 Hz       [dB1, dB2, dB3, dB4, dB5, ...]  
        # 100 Hz     [dB1, dB2, dB3, dB4, dB5, ...]  
        # 200 Hz     [dB1, dB2, dB3, dB4, dB5, ...]  
        # ...        ...  ...  ...  ...  ...  ...   
        # sr/2       [dB1, dB2, dB3, dB4, dB5, ...]  

        # D_normalized = D / np.max(D)  # Normaliza en escala lineal
        D_dB = librosa.amplitude_to_db(D, ref=0)
        
        # Segment size
        frames_per_segment = int(segment_duration * sr / hop_length)
        
        frequencies = librosa.fft_frequencies(sr=sr, n_fft=n_fft)

        bpm = float(np.array(bpm).item())
        frequenciesData, distribution = _analyze_frequencies(
            D_dB=D_dB, 
            frequencies=frequencies,
            frames_per_segment=frames_per_segment,
            top_n_freqs=top_n_freqs,
            hop_length=hop_length,
            sr=sr
        )
        fingerprint = {
            "bpm": float(round(bpm, 2)),
            "frequencies": frequenciesData,
            "distribution": distribution
        }

        save_json(fingerprint=fingerprint, songName=songName)
        return True
        
    except FileNotFoundError as e:
        print(f"File error: {str(e)}")
        return False
    except Exception as e:
        print(f"Error generating fingerprint: {str(e)}")
        return False

def _analyze_frequencies(D_dB, frequencies, frames_per_segment, top_n_freqs, hop_length, sr):
    fingerprint = []
    max_global = np.max(D_dB)
    freq_distribution = [0, 0, 0, 0] # [Total, bajos, medios, altos]

    for t in range(0, D_dB.shape[1], frames_per_segment):
        segment = D_dB[:, t:t+(frames_per_segment)]
        # Average spectrum over the segment duration

        avg_spectrum = np.max(segment, axis=1)
        
        # Find dominant peaks
        pks, _ = find_peaks(
            avg_spectrum, 
            height=np.percentile(avg_spectrum, 95),
            # distance=10  # Minimum distance between peaks
        )
        avg_spectrum_norm = (avg_spectrum / max_global) * 100

        if len(pks) > 0:

            low_peaks = []
            mid_peaks = []
            high_peaks = []

            for p in pks:
                freq = frequencies[p]
                if freq < 200:
                    low_peaks.append(p)
                elif freq < 4000:
                    mid_peaks.append(p)
                else:
                    high_peaks.append(p)

            def get_dominant_peak(peaks):
                if not peaks:
                    return None
                return max(peaks, key=lambda p: avg_spectrum[p])
            
            low_peak = get_dominant_peak(low_peaks)
            mid_peak = get_dominant_peak(mid_peaks)
            high_peak = get_dominant_peak(high_peaks)

            # Get top N frequencies by amplitude
            # top_freq = max(pks, key=lambda p: avg_spectrum[p])
            # top_freqs = sorted(pks, key=lambda p: avg_spectrum[p], reverse=True)[:top_n_freqs]
            # actualFreq = float(round(frequencies[top_freqs[0]], 1))

            fingerprint.append({
                "time": float(round(t * hop_length   / sr, 3)),
                'frequencies': {
                    'bajo': float(round(frequencies[low_peak], 1)) if low_peak else None,
                    'medio': float(round(frequencies[mid_peak], 1)) if mid_peak else None,
                    'alto': float(round(frequencies[high_peak], 1)) if high_peak else None
                },
                'amplitudes': {
                    'bajo': float(round(avg_spectrum[low_peak], 2)) if low_peak else None,
                    'medio': float(round(avg_spectrum[mid_peak], 2)) if mid_peak else None,
                    'alto': float(round(avg_spectrum[high_peak], 2)) if high_peak else None
                }
                # "frequencies": actualFreq,
                # "amplitudes": float("{:.2f}".format(avg_spectrum_norm[top_freqs[0]]))
            })

            # [20Hz ---------------200Hz--------------------4000Hz----------------24kHz]
            # |        Bajos         |         Medios         |       Agudos        |

            if (low_peak):
                if (mid_peak):
                    if (avg_spectrum[low_peak] > avg_spectrum[mid_peak]):
                        freq_distribution[1] += 1
                    else:
                        freq_distribution[2] += 1
                freq_distribution[0] += 1
            elif (mid_peak):
                freq_distribution[0] += 1
                freq_distribution[2] += 1


            # if low_peak:
            # if mid_peak:
            if high_peak:
                # freq_distribution[0] += 1
                freq_distribution[3] += 1
                # freq_distribution[0] += 1
            # if (actualFreq <= 200):
            #     freq_distribution[1] += 1
            # elif (actualFreq <= 4000):
            #     freq_distribution[2] += 1
            # else:
            #     freq_distribution[3] += 1
            # Total++
            
        else: print("   NO")
    distribution = {
        "bajos": float(round((freq_distribution[1] / freq_distribution[0]) * 100, 2)),
        "medios": float(round((freq_distribution[2] / freq_distribution[0]) * 100, 2)),
        "altos": float(round((freq_distribution[3] / freq_distribution[0]) * 100, 2))
    }

    return fingerprint, distribution

def save_json(fingerprint, songName: str):
    json_path = os.path.join("app", "services", "fingerprints", f"{songName}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(fingerprint, f, indent=4)

    # Use json.dumps 
    print(f"✅ Huella digital guardada en: {json_path}")

# Read json
def readFingerprint(songName: str) -> FingerprintData:

    json_path = os.path.join("app", "services", "fingerprints", f"{songName}.json")
    with open(json_path, 'r', encoding='utf-8') as archivo:
        datos = json.load(archivo)

    data = {
        "bpm": datos.get("bpm"),
        "frequencies": datos.get("frequencies", []),
        "distribution": datos.get("distribution")
    }
    return data

def graph_fingerpint(songName: str):
    datos = readFingerprint(songName.split(" - ")[0].strip())
    frecuencia_data = datos["frequencies"]

    tiempos = [p["time"] for p in frecuencia_data]
    frecuencias = [p["frequencies"] for p in frecuencia_data]

    plt.figure(figsize=(12, 6))
    plt.plot(tiempos, frecuencias, color='royalblue', linewidth=1.5)
    plt.title(f'{songName}')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Frecuencia (Hz)')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():

    generate_fingerprint("era mentira")
    # data = readFingerprint("stop")

    # song_name = "era mentira"
    # graph_fingerpint(song_name)
    directory = os.path.join("app", "services", "songs")
    files = [f for f in os.listdir(directory) if f.lower().endswith(".mp3")]

    for f in files:
        song_name = os.path.splitext(f)[0]
        print(f"🎵 Generando huella para: {song_name}")
        success = generate_fingerprint(song_name)
        if success:
            print(f"✅ Huella generada para '{song_name}'")
        else:
            print(f"❌ Error al generar huella para '{song_name}'")
    print("🧩 Procesamiento finalizado.")
    
if __name__ == "__main__":
    main()
