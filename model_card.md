# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**

---

## 2. Intended Use  

**Goal:** VibeMatch suggests the 5 songs from a small catalog that best fit one listener's taste. It predicts which songs the listener is most likely to enjoy based on each song's genre, mood, energy, and how acoustic it sounds.

**Intended use:** Classroom exploration of how a content-based recommender turns data into ranked suggestions, and where it goes wrong. It assumes a user's taste can be described as one favorite genre, one favorite mood, a target energy level, and whether they like acoustic music.

**Not intended for:** Real listeners or a real music app. The catalog has only 18 made-up songs, the system doesn't learn from listening history, and every user gets the same fixed weights. It also shouldn't be used to decide which artists or genres get promoted, because its biases (see section 6) favor some genres over others.

---

## 3. How the Model Works  

VibeMatch gives every song in the catalog points, then lists the songs with the most points first.

- **Same genre as your favorite:** 2 points.
- **Same mood as your favorite:** 1 point.
- **Energy close to what you want:** up to 1 point. A perfect match gets the full point, and the further the song's energy is from your target, in either direction, the fewer points it gets. A song can be "too intense" just as easily as "too calm".
- **Acoustic fit:** half a point if the song is acoustic and you like acoustic music, or if it isn't and you don't.

The best possible score is 4.5. Each song comes with a list of reasons, like "genre match (+2.0)", so you can see exactly where its points came from.

**Changes from the starter logic:** The starter code returned the first five songs in the file with a placeholder explanation. I added the scoring and ranking, the reasons list, and the acoustic preference. The starter `UserProfile` already had a `likes_acoustic` field, but nothing used it.

---

## 4. Data  

- **Size:** 18 songs in `data/songs.csv`: the 10 starter songs plus 8 I added.
- **Genres and moods:** 15 genres and 14 moods. Lofi has 3 songs, pop has 2, and every other genre has just 1.
- **Features:** Each song has genre, mood, energy, tempo, valence, danceability, and acousticness. VibeMatch scores only genre, mood, energy, and acousticness.
- **What I added:** Songs in hip hop, bluegrass, classical, metal, edm, r&b, blues, and trip hop, with new moods like sad, angry, romantic, and euphoric. Two of them, *Back Porch Reel* and *Static Lullaby*, were picked so that loud songs aren't always electronic and quiet songs aren't always acoustic.
- **Limits:** All songs and numbers are made up. They don't come from real audio analysis.
- **Missing parts of taste:** Lyrics and language, artist popularity, release year, listening history, and the fact that most people like more than one genre. Because most genres have only one song, a fan of anything except lofi or pop runs out of genre matches after a single song.

---

## 5. Strengths  

- **Consistent tastes work well.** When all of a user's preferences point the same way, the results look right. Chill Lofi got three lofi songs, then calm ambient and jazz. Deep Intense Rock got *Storm Runner*, the only rock song, at #1 with a near-perfect score.
- **Opposite listeners get opposite lists.** The High-Energy Pop and Chill Lofi lists share no songs at all.
- **Energy works in both directions.** A calm listener isn't pushed toward loud songs just because loud songs have "higher" numbers.
- **Every score is explained.** When a result looks wrong, like *Gym Hero* for a happy pop fan, the reasons show exactly why it happened.

---

## 6. Limitations and Bias 

The biggest weakness is that genre is worth so much that it can override what the user actually asked for. A genre match alone (+2.0) is worth as much as a perfect mood match and a perfect energy match put together. In the "Sad but Hyped" test, the user asked for sad music and got *Neon Euphoria*, a euphoric EDM track, at #1, while the only sad song in the catalog came 5th. This creates a small filter bubble: users always get their one genre first, and because 12 of the 15 genres have just one song, the rest of the list gets filled with the same few loud songs. *Sunrise City*, *Gym Hero*, and *Storm Runner* each show up in 3 of the 5 test lists. Labels must also match exactly, so a pop fan gets no genre credit for "indie pop".

---

## 7. Evaluation  

### Profiles tested

I ran five profiles through `python -m src.main` and looked at the top 5 for each. Three are "normal" listeners. Two are edge cases meant to trick the scoring.

| Profile | Genre | Mood | Energy | Likes acoustic |
|---|---|---|---|---|
| High-Energy Pop (default) | pop | happy | 0.8 | no |
| Chill Lofi | lofi | chill | 0.35 | yes |
| Deep Intense Rock | rock | intense | 0.9 | no |
| Sad but Hyped (edge case: conflicting) | edm | sad | 0.9 | no |
| Genre Not in Catalog (edge case) | k-pop | happy | 0.8 | no |

```
=== High-Energy Pop ===
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

```
=== Chill Lofi ===
Profile: {'favorite_genre': 'lofi', 'favorite_mood': 'chill', 'target_energy': 0.35, 'likes_acoustic': True}

Top recommendations:

1. Library Rain by Paper Lanterns (lofi, chill)
   Score: 4.50
   Because: genre match (+2.0), mood match (+1.0), energy closeness (+1.00), acoustic fit (+0.5)

2. Midnight Coding by LoRoom (lofi, chill)
   Score: 4.43
   Because: genre match (+2.0), mood match (+1.0), energy closeness (+0.93), acoustic fit (+0.5)

3. Focus Flow by LoRoom (lofi, focused)
   Score: 3.45
   Because: genre match (+2.0), energy closeness (+0.95), acoustic fit (+0.5)

4. Spacewalk Thoughts by Orbit Bloom (ambient, chill)
   Score: 2.43
   Because: mood match (+1.0), energy closeness (+0.93), acoustic fit (+0.5)

5. Coffee Shop Stories by Slow Stereo (jazz, relaxed)
   Score: 1.48
   Because: energy closeness (+0.98), acoustic fit (+0.5)
```

```
=== Deep Intense Rock ===
Profile: {'favorite_genre': 'rock', 'favorite_mood': 'intense', 'target_energy': 0.9, 'likes_acoustic': False}

Top recommendations:

1. Storm Runner by Voltline (rock, intense)
   Score: 4.49
   Because: genre match (+2.0), mood match (+1.0), energy closeness (+0.99), acoustic fit (+0.5)

2. Gym Hero by Max Pulse (pop, intense)
   Score: 2.47
   Because: mood match (+1.0), energy closeness (+0.97), acoustic fit (+0.5)

3. Neon Euphoria by Pulsewave (edm, euphoric)
   Score: 1.45
   Because: energy closeness (+0.95), acoustic fit (+0.5)

4. Iron Verdict by Grave Static (metal, angry)
   Score: 1.43
   Because: energy closeness (+0.93), acoustic fit (+0.5)

5. Sunrise City by Neon Echo (pop, happy)
   Score: 1.42
   Because: energy closeness (+0.92), acoustic fit (+0.5)
```

```
=== Sad but Hyped ===
Profile: {'favorite_genre': 'edm', 'favorite_mood': 'sad', 'target_energy': 0.9, 'likes_acoustic': False}

Top recommendations:

1. Neon Euphoria by Pulsewave (edm, euphoric)
   Score: 3.45
   Because: genre match (+2.0), energy closeness (+0.95), acoustic fit (+0.5)

2. Storm Runner by Voltline (rock, intense)
   Score: 1.49
   Because: energy closeness (+0.99), acoustic fit (+0.5)

3. Gym Hero by Max Pulse (pop, intense)
   Score: 1.47
   Because: energy closeness (+0.97), acoustic fit (+0.5)

4. Iron Verdict by Grave Static (metal, angry)
   Score: 1.43
   Because: energy closeness (+0.93), acoustic fit (+0.5)

5. Empty Station Blues by Hollis Grey (blues, sad)
   Score: 1.43
   Because: mood match (+1.0), energy closeness (+0.43)
```

```
=== Genre Not in Catalog ===
Profile: {'favorite_genre': 'k-pop', 'favorite_mood': 'happy', 'target_energy': 0.8, 'likes_acoustic': False}

Top recommendations:

1. Sunrise City by Neon Echo (pop, happy)
   Score: 2.48
   Because: mood match (+1.0), energy closeness (+0.98), acoustic fit (+0.5)

2. Rooftop Lights by Indigo Parade (indie pop, happy)
   Score: 2.46
   Because: mood match (+1.0), energy closeness (+0.96), acoustic fit (+0.5)

3. Concrete Crown by Lyric Theory (hip hop, confident)
   Score: 1.48
   Because: energy closeness (+0.98), acoustic fit (+0.5)

4. Night Drive Loop by Neon Echo (synthwave, moody)
   Score: 1.45
   Because: energy closeness (+0.95), acoustic fit (+0.5)

5. Storm Runner by Voltline (rock, intense)
   Score: 1.39
   Because: energy closeness (+0.89), acoustic fit (+0.5)
```

### Why "Gym Hero" keeps showing up for Happy Pop listeners

*Gym Hero* is labeled "pop", and the recommender gives 2 points just for matching the genre. That's twice what it gives for matching "happy". *Gym Hero* is an intense workout song, not a happy one, but its pop label alone is worth more than *Rooftop Lights*' happy mood, because *Rooftop Lights* is labeled "indie pop" and gets no genre credit. So the system decides "pop, wrong mood" is a better fit than "happy, almost pop". Most people would disagree.

### Why a song ranked first: *Neon Euphoria* for "Sad but Hyped"

*Neon Euphoria* scored 3.45: +2.0 for being EDM, +0.95 because its energy (0.95) is very close to 0.9, and +0.5 for not being acoustic. The only sad song, *Empty Station Blues*, scored just 1.43: +1.0 for the mood, but only +0.43 for energy (0.33 is far from 0.9) and nothing for acoustic fit, because it is an acoustic song. The genre bonus alone was bigger than everything the sad song earned.

### Comparing the profiles

- **High-Energy Pop vs. Chill Lofi:** The lists share no songs. Pop gets upbeat electronic songs near 0.8 energy, and lofi gets quiet acoustic songs near 0.35. This makes sense because all four preferences flip.
- **High-Energy Pop vs. Deep Intense Rock:** Both lists have *Gym Hero* at #2, for different reasons. The pop fan gets it for the genre, the rock fan for the "intense" mood. Both users want loud, non-acoustic music, so their lists overlap.
- **High-Energy Pop vs. Sad but Hyped:** Both want high energy, but the pop fan's top songs are actually happy, while the sad fan's #1 is euphoric. When the mood can't be matched, the genre and energy points take over.
- **High-Energy Pop vs. Genre Not in Catalog:** These two profiles differ only in genre. Without the +2.0 pop bonus, *Gym Hero* drops off the list and *Rooftop Lights* moves up to #2. This shows the genre bonus is the only thing keeping *Gym Hero* near the top for the pop fan.
- **Chill Lofi vs. Deep Intense Rock:** The lists share no songs and sit at opposite ends of the energy scale (0.28 to 0.42 for lofi, 0.82 to 0.97 for rock). This is what you'd expect from opposite listeners.
- **Chill Lofi vs. Sad but Hyped:** The lofi list holds together well because genre, mood, energy, and acoustic preference all point the same way. The sad fan's preferences pull against each other, so their list is a mix of songs that each match only one thing.
- **Chill Lofi vs. Genre Not in Catalog:** The lofi fan gets three genre matches because lofi has the most songs, and the top score is 4.50. The k-pop fan gets none, and the top score is 2.48. How good your list can be depends on how many songs your genre has.
- **Deep Intense Rock vs. Sad but Hyped:** Four of the five songs are the same in both lists (*Storm Runner*, *Gym Hero*, *Neon Euphoria*, *Iron Verdict*), because both users want energy 0.9 and nothing acoustic. The genre match decides which of them is #1: *Storm Runner* for rock, *Neon Euphoria* for EDM. Past the genre match, energy is doing almost all the work.
- **Deep Intense Rock vs. Genre Not in Catalog:** After *Storm Runner*, the rock list is a grab bag of loud songs (pop, edm, metal) that only match on energy. The k-pop list at least keeps "happy" songs in its top 2, because mood is the strongest signal left.
- **Sad but Hyped vs. Genre Not in Catalog:** Neither user has a perfect song. The sad fan's genre exists, so the +2.0 pushes a euphoric song to #1. The k-pop fan's genre doesn't exist, so mood decides and the list feels more reasonable. Oddly, having your genre in the catalog made the result worse here.

### What surprised me

- The k-pop listener, whose favorite genre isn't in the catalog at all, got a more sensible list than the pop listener.
- For "Sad but Hyped", the only sad song came last in the top 5, behind three songs that aren't sad at all.
- Three songs (*Sunrise City*, *Gym Hero*, *Storm Runner*) each appeared in 3 of the 5 lists.

✏️ *Draft. Rewrite in your own words.* For the Chill Lofi profile the results feel right: two chill lofi tracks, then a focused lofi track, then ambient and jazz. That's what I'd want for studying. The High-Energy Pop list feels a little off, because *Gym Hero* at #2 is a workout song, not a happy one.

### Experiment: weight shift (genre halved, energy doubled)

I changed genre from +2.0 to +1.0 and the energy maximum from +1.0 to +2.0, then reran all five profiles. The highest possible score stays 4.5 (1.0 + 1.0 + 2.0 + 0.5). Every song still scored between 0.56 and 4.50, so the math stayed valid. Afterward I put the original weights back.

| Profile | Original top 5 | Experiment top 5 | Better or just different? |
|---|---|---|---|
| High-Energy Pop | Sunrise City, **Gym Hero**, **Rooftop Lights**, Concrete Crown, Night Drive Loop | Sunrise City, **Rooftop Lights**, **Gym Hero**, Concrete Crown, Night Drive Loop | **Better.** The happy song now beats the intense one. |
| Sad but Hyped | Neon Euphoria, Storm Runner, Gym Hero, Iron Verdict, **Empty Station Blues** | Neon Euphoria, Storm Runner, Gym Hero, Iron Verdict, **Sunrise City** | **Worse.** The only sad song dropped out and a happy song took its place. |
| Chill Lofi, Deep Intense Rock, Genre Not in Catalog | (same order in both runs) | (same order in both runs) | **Same.** Only the scores changed. |

Making energy stronger fixed the *Gym Hero* problem for the pop fan, but it hurt the user whose mood and energy disagree, because energy now outweighs mood even more. The change made the results different, not better overall. Each profile needs a different balance, which a single set of weights can't give everyone.

---

## 8. Future Work  

1. **Partial credit for related labels.** Group genres and moods into families (pop and indie pop; chill, relaxed, and peaceful) and give partial points for a near match, so a near miss isn't scored like a total miss. Also let users pick more than one favorite genre.
2. **Weights that fit the user.** The experiment showed that one set of weights can't work for everyone: halving genre helped the pop fan but hurt the "Sad but Hyped" fan. Learning weights from each user's likes and skips would fix that better than any fixed numbers.
3. **More variety in the top 5.** Limit how many songs from one genre or artist can appear, so the same few loud songs (*Gym Hero*, *Storm Runner*) don't fill every high-energy list.

---

## 9. Personal Reflection  

✏️ *Draft. Rewrite in your own words.*

**Biggest learning moment:** Seeing "Sad but Hyped" get a euphoric song at #1. I chose the weights thinking genre was the strongest signal, but I hadn't thought about what happens when a user's genre exists and their mood doesn't. One number (+2.0) decided what that user heard.

**How AI helped, and when I had to double-check:** The AI assistant helped me research how real platforms recommend music, generate new songs for the CSV, write the scoring code, and come up with edge-case profiles I wouldn't have thought of. I still had to check its work. When it analyzed the starter data, it found that acousticness and energy were almost perfectly linked (−0.99), so the acoustic preference would barely matter until we added songs that broke that pattern. It also wrote one comparison in this model card that didn't match the real output. That was caught only because every claim was checked against a fresh run before committing. The lesson for me: always compare the AI's description of results to the actual results.

**What surprised me:** How much four simple rules can feel like a real recommendation. The reasons ("genre match, mood match, energy close") make it seem thoughtful, even though the system knows nothing about music. I was also surprised that the k-pop user, whose genre isn't in the catalog at all, got a more sensible list than the pop fan.

**How it changed how I see music apps:** Now when an app keeps suggesting the same kind of song, I wonder which weight is doing it.

**What I'd try next:** Add partial credit for related genres and moods, then add a simple collaborative filter using a few made-up users' likes, to see how the lists change compared to content alone.
