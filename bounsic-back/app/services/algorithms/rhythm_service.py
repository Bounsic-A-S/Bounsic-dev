from typing import List
import matplotlib.pyplot as plt
import os
import numpy as np
from fingerprint_service import FingerprintData, generate_fingerprint, readFingerprint
from scipy import interpolate
from scipy.stats import ks_2samp

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
        # print("-----------------------------")
        # print(f" | [ {song} ] |")
        bpm_score = 0
        bajos_score = 0
        medios_score = 0
        altos_score = 0
        total_score = 0
        current_song = fingerprints[song]

        bpm_score = ( 1 / ( 1 + (np.abs(focus_song["bpm"] - current_song["bpm"]) / 40)))

        # Compare frequency range
        # bajos_score = ( 1 / ( 1 + (np.abs(focus_song["distribution"]["bajos"] - current_song["distribution"]["bajos"]) / 60)))
        # medios_score = ( 1 / ( 1 + (np.abs(focus_song["distribution"]["medios"] - current_song["distribution"]["medios"]) / 60)))
        # altos_score = ( 1 / ( 1 + (np.abs(focus_song["distribution"]["altos"] - current_song["distribution"]["altos"]) / 60)))        

        def distribution_percent(dist_a, dist_b):
            return (np.min([dist_a, dist_b]) 
                       / np.max([dist_a, dist_b]))

        bajos_score = distribution_percent(focus_song["distribution"]["bajos"], current_song["distribution"]["bajos"])
        medios_score = distribution_percent(focus_song["distribution"]["medios"], current_song["distribution"]["medios"])
        altos_score = distribution_percent(focus_song["distribution"]["altos"], current_song["distribution"]["altos"])
        
        bpm_score = float("{:.4f}".format(bpm_score))
        bajos_score = float("{:.4f}".format(bajos_score))
        medios_score = float("{:.4f}".format(medios_score))
        altos_score = float("{:.4f}".format(altos_score))
        # print(f"..bpmScore: {bpm_score}    ->  {bpm_score*bpm_w}   ({bpm_w})")
        # print(f"bajos: {bajos_score}   ->  {bajos_score*bajo_w}   ({bajo_w})")
        # print(f"medios: {medios_score}   ->  {medios_score*medio_w}   ({medio_w})")
        # print(f"altos: {altos_score}   ->  {altos_score*alto_w}   ({alto_w})")

        total_score = (bpm_score*bpm_w) + (bajos_score*bajo_w) + (medios_score*medio_w) + (altos_score*alto_w)
        if total_score > min_alike:
            goodSongs.append({
                "name": song,
                "alike": float(round(total_score*100, 1))
            })

    return goodSongs

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
    recomendations = get_alikes(song_name)

    print(f"\nBest recomendations for {song_name}")
    for recom in recomendations:
        print(f"({recom['alike']}%) song: {recom['name']}\n")

if __name__ == "__main__":
    main()
