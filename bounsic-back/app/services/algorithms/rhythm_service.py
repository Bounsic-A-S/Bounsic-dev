import matplotlib.pyplot as plt
from typing import List, Tuple
# from app.services.algorithms.fingerprint_service import readFingerprint

from fingerprint_service import generate_fingerprint, readFingerprint

def graph_frequencies(song_name: str, artist: str, usar_segundo_valor=False):
    """
    Grafica los valores de una lista de tuplas.
    
    :param datos: Lista de tuplas (float, float)
    :param usar_segundo_valor: Si True, grafica el segundo valor de cada tupla, si False el primero.
    """
    datos = readFingerprint(song_name)
    x = list(range(len(datos)))  # Índices como eje X
    y = [valor[1] if usar_segundo_valor else valor[0] for valor in datos]

    plt.figure(figsize=(10, 5))
    plt.plot(x, y, marker='o', linestyle='-', color='b')
    plt.xlabel('')
    plt.ylabel('Frequencie value')
    plt.title(f'{song_name} - ({artist})')
    plt.grid(True)
    plt.show()

# Algorithm to get alike songs based on their sound
def get_alikes(songName: str):



    return 0


def main():
    song_name = "Genesis"
    artist = "Grimes"
    generate_fingerprint(song_name)
    graph_frequencies(song_name, artist)

if __name__ == "__main__":
    main()
