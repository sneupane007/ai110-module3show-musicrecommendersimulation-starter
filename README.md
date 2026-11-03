# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

My version, **VibeMatch 1.0**, is a small content-based recommender. It loads 18 songs from `data/songs.csv` and scores each one against a user's taste profile: favorite genre, favorite mood, target energy, and whether they like acoustic music. It then prints the top 5 with the reasons behind each score. I tested it on five profiles, including two edge cases, and ran one weight experiment. The biggest finding is that genre is weighted so heavily it can override the mood a user asked for. See the [model card](model_card.md) for the full evaluation.

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
user_prefs = {"favorite_genre": "pop", "favorite_mood": "happy", "target_energy": 0.8, "likes_acoustic": False}
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

Output of `python -m src.main` with the default pop/happy profile:

```
Loading songs from data/songs.csv...
Loaded songs: 18

Profile: {'favorite_genre': 'pop', 'favorite_mood': 'happy', 'target_energy': 0.8, 'likes_acoustic': False}

Top recommendations:

1. Sunrise City by Neon Echo (pop, happy)
   Score: 4.48
   Because: genre match (+2.0), mood match (+1.0), energy closeness (+0.98), acoustic fit (+0.5)

2. Gym Hero by Max Pulse (pop, intense)
   Score: 3.37
   Because: genre match (+2.0), energy closeness (+0.87), acoustic fit (+0.5)

3. Rooftop Lights by Indigo Parade (indie pop, happy)
   Score: 2.46
   Because: mood match (+1.0), energy closeness (+0.96), acoustic fit (+0.5)

4. Concrete Crown by Lyric Theory (hip hop, confident)
   Score: 1.48
   Because: energy closeness (+0.98), acoustic fit (+0.5)

5. Night Drive Loop by Neon Echo (synthwave, moody)
   Score: 1.45
   Because: energy closeness (+0.95), acoustic fit (+0.5)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

- **Weight shift (genre 2.0 → 1.0, energy max 1.0 → 2.0):** The pop fan's list improved: *Rooftop Lights* (happy) moved above *Gym Hero* (intense). The "Sad but Hyped" list got worse, because the only sad song dropped out of the top 5. The other three profiles kept the same order. I put the original weights back afterward.
- **Different types of users:** I ran High-Energy Pop, Chill Lofi, and Deep Intense Rock, plus two edge cases: "Sad but Hyped" (edm, sad, energy 0.9) and "Genre Not in Catalog" (k-pop). Users whose preferences all agree got sensible lists. The conflicting user got a euphoric song at #1. The k-pop user, with no genre matches at all, got a more sensible list than the pop fan.
- **Expanding the dataset:** In the starter songs, energy and acousticness were almost perfectly linked (correlation −0.99), so the acoustic preference barely mattered. Adding 8 songs, including a loud acoustic one and a quiet electronic one, brought that down to −0.71, so the acoustic preference now changes the rankings.

Full outputs and profile-by-profile comparisons are in section 7 of the [model card](model_card.md).

---

## Limitations and Risks

- **Tiny, made-up catalog:** 18 songs, and 12 of the 15 genres have only one song.
- **Genre dominates:** A +2.0 genre match can beat a song with the right mood and energy. That's why *Gym Hero* beats *Rooftop Lights* for a happy pop fan.
- **Exact labels only:** "indie pop" gets no credit for "pop", and "chill" gets none for "relaxed".
- **Same songs everywhere:** *Sunrise City*, *Gym Hero*, and *Storm Runner* each appear in 3 of the 5 test lists.
- **Missing signals:** It doesn't use lyrics, language, popularity, or listening history, and each user can have only one favorite genre and mood.

More detail is in section 6 of the [model card](model_card.md).

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

✏️ *Draft. Rewrite in your own words.*

A recommender doesn't "know" music. It turns each song into a few labels and numbers, compares them to labels and numbers describing the user, and adds up points. Ranking is just sorting those totals. What makes it feel smart is the explanation: seeing "genre match (+2.0), mood match (+1.0)" makes a simple sum look like a judgment. Real platforms do the same basic thing at a much bigger scale, adding signals like skips, replays, and what other users with similar taste listen to.

Bias comes in through choices that look harmless. One weight (+2.0 for genre) meant a listener who asked for sad music got a euphoric song first. A catalog where most genres have one song means fans of those genres get worse lists than lofi or pop fans. Exact label matching means anyone whose taste falls between categories, like "indie pop", gets less credit. In a real app, the same kinds of choices could decide which artists get heard and which get buried.



