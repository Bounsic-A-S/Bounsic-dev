from typing import List
import matplotlib.pyplot as plt
import os
import numpy as np
from fingerprint_service import FingerprintData, generate_fingerprint, readFingerprint

# Algorithm to get alike songs based on their sound
def get_alikes(song_name: str, bpm_w=1, bajo_w=1, medio_w=1, alto_w=1):
    focus_song = readFingerprint(song_name)
    fingerprints = load_fingerprints(song_name)
    song_names = fingerprints.keys()
    bpm_w /= 3
    bajo_w /= 3
    medio_w /= 3
    goodSongs = []
    print(f"Searching recomendations for: {song_name}")
    for song in song_names:
        print("--------------------------")
        print(f"    - {song}")
        bpm_score = 0
        bajos_score = 0
        medios_score = 0
        altos_score = 0
        total_score = 0
        current_song = fingerprints[song]

        # Compare bpm
        bpm_score = (focus_song["bpm"] - current_song["bpm"])
        if (bpm_score < 0): bpm_score *= -1
        bpm_score = 4 / bpm_score

        # bpm_score = abs(focus_song["bpm"] - current_song["bpm"])
        # bpm_score = np.exp(-(bpm_score ** 2) / (2 * (25 ** 2)))



        # Compare frequency range
        if (focus_song["distribution"]["bajos"] < current_song["distribution"]["bajos"]):
            bajos_score = (focus_song["distribution"]["bajos"] / current_song["distribution"]["bajos"])
        else: 
            bajos_score = (current_song["distribution"]["bajos"] / focus_song["distribution"]["bajos"])

        if (focus_song["distribution"]["medios"] < current_song["distribution"]["medios"]):
            medios_score = (focus_song["distribution"]["medios"] / current_song["distribution"]["medios"])
        else: 
            medios_score = (current_song["distribution"]["medios"] / focus_song["distribution"]["medios"])

        if (focus_song["distribution"]["altos"] < current_song["distribution"]["altos"]):
            altos_score = (focus_song["distribution"]["altos"] / current_song["distribution"]["altos"])
        # else: 
            # altos_score = (current_song["distribution"]["altos"] / focus_song["distribution"]["altos"])
        
        
        # alto_w /= 4
        # bpm_score = float(round(bpm_score, 3))
        # bajos_score = float(round(bajos_score, 3))
        # medios_score = float(round(medios_score, 3))
        
        # print(f"bpmScore: {bpm_score}    ->  {bpm_score*bpm_w}   ({bpm_w})")
        # print(f"bajos: {bajos_score}   ->  {bajos_score*bajo_w}   ({bajo_w})")
        # print(f"medios: {medios_score}   ->  {medios_score*medio_w}   ({medio_w})")

        total_score = (bpm_score*bpm_w) + (bajos_score*bajo_w) + (medios_score*medio_w) + (altos_score*alto_w)
        
        print(f"Similitud: {float(round(total_score*100, 1))}%")
        # print(f"{song}: {fingerprints[song]['bpm']}  ,  {fingerprints[song]['distribution']}")

    return 0

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
    song_name = "genesis"
    get_alikes(song_name)

if __name__ == "__main__":
    main()
