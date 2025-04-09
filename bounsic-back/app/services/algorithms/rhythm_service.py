from typing import List
import matplotlib.pyplot as plt
import os
import numpy as np
from fingerprint_service import FingerprintData, generate_fingerprint, readFingerprint

# Algorithm to get alike songs based on their sound
def get_alikes(song_name: str, bpm_w=0.8, bajo_w=0.8, medio_w=0.8, alto_w=0.8, min_alike=0.7):

    focus_song = readFingerprint(song_name)
    fingerprints = load_fingerprints(song_name)
    song_names = fingerprints.keys()

    total_weight = bpm_w + bajo_w + medio_w + alto_w

    bpm_w /= total_weight
    bajo_w /= total_weight
    medio_w /= total_weight
    alto_w /= total_weight
    goodSongs = []
    print(f"Searching recomendations for: {song_name}")
    for song in song_names:
        print("-----------------------------")
        print(f" | [ {song} ] |")
        bpm_score = 0
        bajos_score = 0
        medios_score = 0
        altos_score = 0
        total_score = 0
        current_song = fingerprints[song]

        bpm_score = ( 1 / ( 1 + (np.abs(focus_song["bpm"] - current_song["bpm"]) / 40)))

        # Compare frequency range
        # bajos_score = ( 1 / ( 1 + (np.abs(focus_song["distribution"]["bajos"] - current_song["distribution"]["bajos"]) / 100)))
        # medios_score = ( 1 / ( 1 + (np.abs(focus_song["distribution"]["medios"] - current_song["distribution"]["medios"]) / 100)))
        # altos_score = ( 1 / ( 1 + (np.abs(focus_song["distribution"]["altos"] - current_song["distribution"]["altos"]) / 100)))

        bajos_score = (np.min([focus_song["distribution"]["bajos"], current_song["distribution"]["bajos"]]) 
                       / np.max([focus_song["distribution"]["bajos"], current_song["distribution"]["bajos"]]))
        
        medios_score = (np.min([focus_song["distribution"]["medios"], current_song["distribution"]["medios"]]) 
                       / np.max([focus_song["distribution"]["medios"], current_song["distribution"]["medios"]]))
        
        altos_score = (np.min([focus_song["distribution"]["altos"], current_song["distribution"]["altos"]]) 
                       / np.max([focus_song["distribution"]["altos"], current_song["distribution"]["altos"]]))
        
        bpm_score = float("{:.4f}".format(bpm_score))
        bajos_score = float("{:.4f}".format(bajos_score))
        medios_score = float("{:.4f}".format(medios_score))
        altos_score = float("{:.4f}".format(altos_score))
        print(f"..bpmScore: {bpm_score}    ->  {bpm_score*bpm_w}   ({bpm_w})")
        print(f"bajos: {bajos_score}   ->  {bajos_score*bajo_w}   ({bajo_w})")
        print(f"medios: {medios_score}   ->  {medios_score*medio_w}   ({medio_w})")
        print(f"altos: {altos_score}   ->  {altos_score*alto_w}   ({alto_w})")

        total_score = (bpm_score*bpm_w) + (bajos_score*bajo_w) + (medios_score*medio_w) + (altos_score*alto_w)
        if total_score > min_alike:
            goodSongs.append({
                "name": song,
                "alike": float(round(total_score*100, 1))
            })

        print(f"\nSimilitud: {float('{:.3f}'.format(total_score))}")

    return goodSongs

def calculate_deviation(fp_songA: FingerprintData, fp_songB: FingerprintData):
    
    def process_single_fingerprint(fp: FingerprintData) -> Dict[str, np.ndarray]:
        bajos = []
        medios = []
        altos = []
        
        amp_bajos = []
        amp_medios = []
        amp_altos = []
        
        for segment in fp['frequencies']:
            freq = segment['frequencies']
            amp = segment['amplitudes']
            
            # Procesar bajos (20-200 Hz)
            if freq['bajo'] is not None:
                bajos.append(freq['bajo'])
                amp_bajos.append(amp['bajo'])
            
            # Procesar medios (200-4000 Hz)
            if freq['medio'] is not None:
                medios.append(freq['medio'])
                amp_medios.append(amp['medio'])
            
            # Procesar altos (>4000 Hz)
            if freq['alto'] is not None:
                altos.append(freq['alto'])
                amp_altos.append(amp['alto'])
        
        return {
            'bajos': np.array(bajos),
            'medios': np.array(medios),
            'altos': np.array(altos),
            'amp_bajos': np.array(amp_bajos),
            'amp_medios': np.array(amp_medios),
            'amp_altos': np.array(amp_altos),
            'bpm': fp['bpm'],
            'distribution': fp['distribution']
        }


def load_fingerprints(without: str, directory="fingerprints") -> dict[str, FingerprintData]: # key "name"
    jsonDir_path = os.path.join("app", "services", directory)
    fingerprints = {}

    for file in os.listdir(jsonDir_path):
        if file.endswith(".json"):
            song_name = os.path.splitext(file)[0]
            if (song_name == without): 
                continue
            try:
                # song = readFingerprint(song_name)
                # song[song_name] = song_name  # opcional: añade el nombre
                fingerprints[song_name] = readFingerprint(song_name)
                # fingerprints.append(song)
            except Exception as e:
                print(f"Error al leer {file}: {e}")            
            
    return fingerprints


def main():
    song_name = "lovers rock"
    recomendations = get_alikes(song_name)

    print(f"\nBest recomendations for {song_name}")
    for recom in recomendations:
        print(f"({recom['alike']}%) song: {recom['name']}\n")

if __name__ == "__main__":
    main()
