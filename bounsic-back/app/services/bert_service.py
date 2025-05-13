import random
import requests
from app.provider import Songs_db_provider
from bson import ObjectId

class Bert_service:
  emotions = {
    "Amor": 0b0000000000000001,
    "Tristeza": 0b0000000000000010,
    "Desamor": 0b0000000000000100,
    "Esperanza": 0b0000000000001000,
    "Angustia": 0b0000000000010000,
    "Positivismo": 0b0000000000100000,
    "Celebración": 0b0000000001000000,
    "Autoaceptación": 0b0000000010000000,
    "Soledad": 0b0000000100000000,
    "Superficialidad": 0b0000001000000000,
    "Lujuria": 0b0000010000000000,
    "Reflexión": 0b0000100000000000,
    "Violencia": 0b0001000000000000,
  }
  
  @staticmethod
  async def analyze_lyrics(lyrics) -> int: 
    try:
      url = "https://bounsic.site:5000/bert/lyrics_analysis"
      headers = {"Content-Type": "application/json"}
      data = {"lyrics": lyrics}

      response = requests.post(url, json=data, headers=headers)
      response.raise_for_status()  # Lanza excepción si hay un error en la solicitud
      result = response.json()  # Obtiene la respuesta en JSON

      lyric_info = 0
      for emotion, values in result.items():
        if values["presente"]:
          lyric_info = lyric_info | Bert_service.emotions[emotion]

      return lyric_info

    except requests.RequestException as e:
      print(f"Error al realizar el fetch de la API: {e}")
      return 0
    
  def get_lyrics_recomendation(seed_song, size=10):
    songs_db_provider = Songs_db_provider()
    db_songs = songs_db_provider.get_all()
    res_songs = []
    inserted_ids = set()
    inserted_ids.add(seed_song["_id"])
    print(f"seed_id: {seed_song['_id']}")

    for song in db_songs:
      if (song["_id"] in inserted_ids):
        continue
      res = Bert_service.evaluate_lyrics(song["lyric_info"], seed_song["lyric_info"])
      if (res):
        res_songs.append(song)
        inserted_ids.add(song["_id"])

    # return res_songs
    return random.sample(res_songs, size)
  
  def evaluate_lyrics(lyric_a: int, lyric_b: int):
    return True if (lyric_a & lyric_b > 0) else 0