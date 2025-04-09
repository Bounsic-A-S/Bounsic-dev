import os
import librosa
import json
import numpy as np
from scipy.signal import find_peaks
# from app.provider import AZURE_CONNECTION_STRING, AZURE_CONTAINER_NAME
# from azure.storage.blob import BlobServiceClient
# from app.provider import db


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

        print(f"sr: {sr}")
        print(f"BPM: {bpm}")

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
        print(f"max: {np.max(D)}")
        # D_normalized = D / np.max(D)  # Normaliza en escala lineal
        D_dB = librosa.amplitude_to_db(D, ref=0)
        
        # Segment size
        frames_per_segment = int(segment_duration * sr / hop_length)
        
        frequencies = librosa.fft_frequencies(sr=sr, n_fft=n_fft)

        # for i, freq in enumerate(frequencies[:500]): # Max frequencie: 240000.00 Hz   
        #     print(f"Fila {i} corresponde a {freq:.2f} Hz")

        print(f"Frames per segment: {frames_per_segment}")
        print(f"Top n frequencies: {top_n_freqs}")
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
        segment = D_dB[:, t:t+(frames_per_segment-1)]
        # Average spectrum over the segment duration
        avg_spectrum = np.mean(segment, axis=1)

        # Find dominant peaks
        pks, _ = find_peaks(
            avg_spectrum, 
            height=np.percentile(avg_spectrum, 95),
            distance=10  # Minimum distance between peaks
        )
        avg_spectrum_norm = (avg_spectrum / max_global) * 100

        if len(pks) > 0:
            # Get top N frequencies by amplitude
            top_freqs = sorted(pks, key=lambda p: avg_spectrum[p], reverse=True)[:top_n_freqs]
            actualFreq = float(round(frequencies[top_freqs[0]], 1))
            fingerprint.append({
                "time": float(round(t * hop_length   / sr, 3)),
                "frequencies": actualFreq,
                "amplitudes": float("{:.2f}".format(avg_spectrum_norm[top_freqs[0]]))
            })

            #                           Frequencies range
            # [20Hz ---------------200Hz--------------------4000Hz----------------24kHz]
            # |        Bajos         |         Medios         |       Agudos        |
            if (actualFreq <= 200):
                freq_distribution[1] += 1
            elif (actualFreq <= 4000):
                freq_distribution[2] += 1
            else:
                freq_distribution[3] += 1
            # Total++
            freq_distribution[0] += 1
        
    print(f"Total freq = {freq_distribution[0]}")
    distribution = {
        "bajos": float(round((freq_distribution[1] / freq_distribution[0]) * 100, 2)),
        "medios": float(round((freq_distribution[2] / freq_distribution[0]) * 100, 2)),
        "altos": float(round((freq_distribution[3] / freq_distribution[0]) * 100, 2))
    }

    return fingerprint, distribution

def save_json(fingerprint, songName: str):

    ruta_json = os.path.join("app", "services", "fingerprints", f"{songName}.json")
    with open(ruta_json, "w", encoding="utf-8") as f:
        json.dump(fingerprint, f, indent=4)

    # Use json.dumps 
    print(f"✅ Huella digital guardada en: {ruta_json}")

def readFingerprint(songName: str) -> list[tuple[float, float]]: # Fix to new fingerprint
    songName = songName.lower()
    ruta_json = os.path.join("app", "services", "fingerprints", f"{songName}.json")
    
    with open(ruta_json, "r", encoding="utf-8") as file:
        fingerprint_data = json.load(file)

    frequency_pairs = [tuple(pair) for pair in fingerprint_data]

    return frequency_pairs

def main():
    generate_fingerprint("oblivion")
    
if __name__ == "__main__":
    main()
