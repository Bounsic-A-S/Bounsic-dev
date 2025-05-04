from typing import List
import matplotlib.pyplot as plt
import os
import numpy as np
import random
from .fingerprint_service import FingerprintData, generate_fingerprint, readFingerprint

# Algorithm to get alike songs based on their sound
def get_alikes(target_song, database_songs, size: int, bpm_w=0.8, bajo_w=0.8, medio_w=0.8, alto_w=0.8, min_alike=0.7):
    total_weight = bpm_w + bajo_w + medio_w + alto_w
    resSongs = []

    bpm_w /= total_weight
    bajo_w /= total_weight
    medio_w /= total_weight
    alto_w /= total_weight
    target_fp = target_song["fingerprint"]
    # print(f"Searching recomendations for: {target_song['title']}")
    for song in database_songs:
        bpm_score = 0
        bajos_score = 0
        medios_score = 0
        altos_score = 0
        total_score = 0

        current_song = song["fingerprint"]

        if ("bpm" not in current_song or "bpm" not in target_fp):
            continue

        temp = np.abs(current_song["bpm"] - target_song["fingerprint"]["bpm"])
        if (temp > 20): 
            continue

        bpm_score = ( 1 / ( 1 + (temp / 40)))

        # Compare frequency range
        # bajos_score = ( 1 / ( 1 + (np.abs(target_song["distribution"]["bajos"] - current_song["distribution"]["bajos"]) / 60)))
        # medios_score = ( 1 / ( 1 + (np.abs(target_song["distribution"]["medios"] - current_song["distribution"]["medios"]) / 60)))
        # altos_score = ( 1 / ( 1 + (np.abs(target_song["distribution"]["altos"] - current_song["distribution"]["altos"]) / 60)))        

        def distribution_percent(dist_a, dist_b):
            if (dist_a > dist_b):
                r = dist_b / dist_a
            else:
                r = dist_a / dist_b
            return r

        bajos_score = distribution_percent(target_fp["distribution"]["bajos"], current_song["distribution"]["bajos"])
        medios_score = distribution_percent(target_fp["distribution"]["medios"], current_song["distribution"]["medios"])
        altos_score = distribution_percent(target_fp["distribution"]["altos"], current_song["distribution"]["altos"])
        
        # bpm_score = float("{:.4f}".format(bpm_score))
        # bajos_score = float("{:.4f}".format(bajos_score))
        # medios_score = float("{:.4f}".format(medios_score))
        # altos_score = float("{:.4f}".format(altos_score))

        # print(f"..bpmScore: {bpm_score}    ->  {bpm_score*bpm_w}   ({bpm_w})")
        # print(f"bajos: {bajos_score}   ->  {bajos_score*bajo_w}   ({bajo_w})")
        # print(f"medios: {medios_score}   ->  {medios_score*medio_w}   ({medio_w})")
        # print(f"altos: {altos_score}   ->  {altos_score*alto_w}   ({alto_w})")

        total_score = (bpm_score*bpm_w) + (bajos_score*bajo_w) + (medios_score*medio_w) + (altos_score*alto_w)
        if total_score > min_alike:
            resSongs.append(song)

    if (size < len(resSongs)):
        return random.sample(resSongs, size)
    else: 
        return resSongs

def load_fingerprints(without: str, directory="fingerprints") -> dict[str, FingerprintData]: # key "name"
    jsonDir_path = os.path.join("app", "services", directory)
    fingerprints = {}

    for file in os.listdir(jsonDir_path):
        if file.endswith(".json"):
            song_name = os.path.splitext(file)[0]
            if (song_name == without): 
                continue
            try:
                fingerprints[song_name] = readFingerprint(song_name)
            except Exception as e:
                print(f"Error al leer {file}: {e}")
                
    return fingerprints