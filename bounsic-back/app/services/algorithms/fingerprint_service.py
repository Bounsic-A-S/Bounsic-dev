import os
from typing import List, TypedDict, cast
import librosa
import json
import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
# from app.provider import AZURE_CONNECTION_STRING, AZURE_CONTAINER_NAME
# from azure.storage.blob import BlobServiceClient
# from app.provider import db

class FrequencyRangesData(TypedDict):
    bajos: List[float]
    medios: List[float]
    altos: List[float]
class FrequencyData(TypedDict):
    time: List[float]
    frequencies: FrequencyRangesData
    amplitudes: FrequencyRangesData
class DistributionData(TypedDict):
    bajos: float
    medios: float
    altos: float
class FingerprintData(TypedDict):
    bpm: float
    data: FrequencyData
    distribution: DistributionData

async def generate_fingerprint(audioPath:str ,segment_duration: float = 0.5, top_n_freqs: int = 1):
    try:
        song_path = audioPath
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
        # Frequencies  1    2    3    4    5    ...   n_frames
        # ---------------------------------------------------
        # 0 Hz       [dB1, dB2, dB3, dB4, dB5, ...]
        # 100 Hz     [dB1, dB2, dB3, dB4, dB5, ...]
        # 200 Hz     [dB1, dB2, dB3, dB4, dB5, ...]
        # ...        ...  ...  ...  ...  ...  ... 
        # sr/2       [dB1, dB2, dB3, dB4, dB5, ...]
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
            "data": frequenciesData,
            "distribution": distribution
        }

        # save_json(fingerprint=fingerprint, songName=songName)
        return fingerprint
        
    except FileNotFoundError as e:
        print(f"File error: {str(e)}")
        return {}
    except Exception as e:
        print(f"Error generating fingerprint: {str(e)}")
        return {}

def _analyze_frequencies(D_dB, frequencies, frames_per_segment, top_n_freqs, hop_length, sr):
    fingerprint = []
    max_global = np.max(D_dB)
    freq_distribution = [0, 0, 0, 0] # [Total, bajos, medios, altos]

    # Times segments taken
    freq_times = []
    # Frequencies in ranges
    freq_bajos = []
    freq_medios = []
    freq_altos = []
    # Amplitudes of frequencies
    amp_bajos = []
    amp_medios = []
    amp_altos = []

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

            # Bajos
            if low_peak:
                freq_bajos.append(float(round(frequencies[low_peak], 1)))
                amp_bajos.append(float(round(avg_spectrum[low_peak], 2)))
            else:
                freq_bajos.append(0)
                amp_bajos.append(0)
            # Medios
            if mid_peak:
                freq_medios.append(float(round(frequencies[mid_peak], 1)))
                amp_medios.append(float(round(avg_spectrum[mid_peak], 2)))
            else:
                freq_medios.append(0)
                amp_bajos.append(0)
            # Altos
            if high_peak:
                freq_altos.append(float(round(frequencies[high_peak], 1)))
                amp_altos.append(float(round(avg_spectrum[high_peak], 2)))
            else:
                freq_altos.append(0)
                amp_altos.append(0)

            freq_times.append(float(round(t * hop_length   / sr, 3)))

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

            if high_peak:
                freq_distribution[3] += 1

    distribution = {
        "bajos": float(round((freq_distribution[1] / freq_distribution[0]) * 100, 2)),
        "medios": float(round((freq_distribution[2] / freq_distribution[0]) * 100, 2)),
        "altos": float(round((freq_distribution[3] / freq_distribution[0]) * 100, 2))
    }
    
    data = {
        "times": freq_times,
        "frequencies": {
            "bajos": freq_bajos,
            "medios": freq_medios,
            "altos": freq_altos
        },
        "amplitudes": {
            "bajos": amp_bajos,
            "medios": amp_medios,
            "altos": amp_altos
        }
    }
    return data, distribution

def save_json(fingerprint, songName: str):
    json_path = os.path.join("app", "services", "fingerprints", f"{songName}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(fingerprint, f, indent=4)

    # Use json.dumps to store in data base
    print(f"✅ Huella digital guardada en: {json_path}")

def readFingerprint(songName: str) -> FingerprintData:
    json_path = os.path.join("app", "services", "fingerprints", f"{songName}.json")
    with open(json_path, "r", encoding="utf-8") as file:
        raw_data = json.load(file)
    return cast(FingerprintData, raw_data)

# Old function, Not adapted to new fingerprint
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