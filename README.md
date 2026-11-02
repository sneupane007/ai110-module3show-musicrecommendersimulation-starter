# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

### How real recommenders work (and what mine does)

Big platforms like Spotify and YouTube mix two ideas. **Collaborative filtering** uses other people's behavior: if listeners who share your history also love a song you haven't heard, it gets suggested to you. **Content-based filtering** uses the songs themselves (genre, mood, tempo, energy, how acoustic they sound) and finds tracks similar to what you already like. Real systems feed in explicit signals (likes, saves, playlist adds), implicit signals (skips, replays, how long you listen), and audio features. They score a huge pool of candidates and then rank the best few. My version is a small **content-based** recommender only. There are no other users to learn from, so it compares each song's attributes to one user's taste profile. It prioritizes **genre** first, **mood** second, and then how **close** the song's energy is to what the user wants.

### Features used

**`Song`**

- `genre`: pop, lofi, rock, etc.
- `mood`: happy, chill, intense, etc.
- `energy`: 0.0 (calm) to 1.0 (intense)
- `acousticness`: 0.0 (electronic) to 1.0 (acoustic)
- `id`, `title`, `artist`: for display only, not scored

`tempo_bpm`, `valence`, and `danceability` are loaded but not scored. In this catalog, tempo and danceability rise and fall with energy (correlations of 0.92 and 0.72), so scoring them would mostly count energy twice.

**`UserProfile`**

- `favorite_genre`
- `favorite_mood`
- `target_energy`: a number from 0.0 to 1.0
- `likes_acoustic`: True or False

### Catalog

`data/songs.csv` has 18 songs: the 10 starter songs plus 8 I added (hip hop, bluegrass, classical, metal, edm, r&b, blues, trip hop) to cover genres and moods the starter file didn't have. Two of them break the "loud means electronic" pattern: *Back Porch Reel* is high energy but acoustic, and *Static Lullaby* is low energy but electronic.

### Default taste profile

```python
user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False}
```

### Algorithm Recipe

**Scoring rule (judges one song):**

| Check | Points |
|---|---|
| Song's genre equals the user's favorite genre | +2.0 |
| Song's mood equals the user's favorite mood | +1.0 |
| Energy closeness: `1 - abs(song energy - target energy)` | 0.0 to +1.0 |
| Acoustic fit: the song is acoustic (acousticness ≥ 0.5) and the user likes acoustic, or the song isn't and the user doesn't | +0.5 |

The highest possible score is 4.5. Every check that adds points also adds a reason, such as `genre match (+2.0)`, so the user can see why a song was picked. Genre is worth twice as much as mood because genre changes the whole sound of a song, while the same mood can show up in any genre. Energy uses closeness instead of "higher is better", so a song that is too intense loses points the same way as a song that is too calm.

**Ranking rule (orders the whole catalog):** score every song, sort from highest to lowest score, and return the top `k` (default 5). Songs with equal scores keep their order from the CSV.

### Data flow

```
User prefs ──► for each song in songs.csv: score_song(prefs, song) → (score, reasons)
           ──► sort every song by score, highest first
           ──► return the top k songs with their scores and reasons
```

### Biases I expect

- **Genre outweighs everything else.** A song in the right genre but the wrong mood can beat a song with the right mood and energy in a nearby genre. In a dry run of the pop/happy profile, *Gym Hero* (pop, intense) came 2nd, ahead of *Rooftop Lights* (indie pop, happy).
- **Exact labels only.** "indie pop" is not "pop", and "chill", "relaxed", and "peaceful" are all different moods. Labels that are close get no credit.
- **Uneven catalog.** Lofi has 3 songs, but 12 of the 15 genres have only one. A lofi fan gets several genre matches. A metal fan gets one, and the rest of their list is filled in by energy alone.
- **Middle-energy users get flatter results.** A user who wants energy 0.5 is never more than 0.47 away from any song in this catalog, while a user who wants 0.95 can be 0.77 away. For middle users, energy separates songs less, so genre decides even more.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



