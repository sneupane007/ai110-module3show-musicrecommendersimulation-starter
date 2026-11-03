"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs

PROFILES = {
    # Default "pop/happy" taste profile
    "High-Energy Pop": {"favorite_genre": "pop", "favorite_mood": "happy", "target_energy": 0.8, "likes_acoustic": False},
    "Chill Lofi": {"favorite_genre": "lofi", "favorite_mood": "chill", "target_energy": 0.35, "likes_acoustic": True},
    "Deep Intense Rock": {"favorite_genre": "rock", "favorite_mood": "intense", "target_energy": 0.9, "likes_acoustic": False},
    # Edge case: conflicting preferences (sad mood, but very high energy)
    "Sad but Hyped": {"favorite_genre": "edm", "favorite_mood": "sad", "target_energy": 0.9, "likes_acoustic": False},
    # Edge case: favorite genre does not exist in the catalog
    "Genre Not in Catalog": {"favorite_genre": "k-pop", "favorite_mood": "happy", "target_energy": 0.8, "likes_acoustic": False},
}


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for name, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print(f"\n=== {name} ===")
        print(f"Profile: {user_prefs}")
        print("\nTop recommendations:\n")
        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"{rank}. {song['title']} by {song['artist']} ({song['genre']}, {song['mood']})")
            print(f"   Score: {score:.2f}")
            print(f"   Because: {explanation}")
            print()


if __name__ == "__main__":
    main()
