import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

# Points from the Algorithm Recipe in README.md
GENRE_POINTS = 2.0
MOOD_POINTS = 1.0
ENERGY_POINTS = 1.0  # max points, scaled by how close the energy is
ACOUSTIC_POINTS = 0.5

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k Song objects for this user, best match first."""
        return sorted(self.songs, key=lambda song: score_song(asdict(user), asdict(song))[0], reverse=True)[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return the song's score and the reasons behind it as one readable string."""
        score, reasons = score_song(asdict(user), asdict(song))
        return f"Score {score:.2f}: " + ", ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Read the songs CSV into a list of dicts, converting numeric columns to int/float."""
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline="") as f:
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            for key in ("energy", "tempo_bpm", "valence", "danceability", "acousticness"):
                row[key] = float(row[key])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against the user's preferences and return (score, reasons)."""
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs["favorite_genre"]:
        score += GENRE_POINTS
        reasons.append(f"genre match (+{GENRE_POINTS})")

    if song["mood"] == user_prefs["favorite_mood"]:
        score += MOOD_POINTS
        reasons.append(f"mood match (+{MOOD_POINTS})")

    energy_points = ENERGY_POINTS * (1 - abs(song["energy"] - user_prefs["target_energy"]))
    score += energy_points
    reasons.append(f"energy closeness (+{energy_points:.2f})")

    if (song["acousticness"] >= 0.5) == user_prefs["likes_acoustic"]:
        score += ACOUSTIC_POINTS
        reasons.append(f"acoustic fit (+{ACOUSTIC_POINTS})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort highest score first, and return the top k as (song, score, explanation)."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, ", ".join(reasons)))
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]
