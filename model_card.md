# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

The biggest weakness is that genre is worth so much that it can override what the user actually asked for. A genre match alone (+2.0) is worth as much as a perfect mood match and a perfect energy match put together. In the "Sad but Hyped" test, the user asked for sad music and got *Neon Euphoria*, an euphoric EDM track, at #1, while the only sad song in the catalog came 5th. This creates a small filter bubble: users always get their one genre first, and because 12 of the 15 genres have just one song, the rest of the list gets filled with the same few loud songs. *Sunrise City*, *Gym Hero*, and *Storm Runner* each show up in 3 of the 5 test lists. Labels must also match exactly, so a pop fan gets no genre credit for "indie pop".

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
- **Sad but Hyped vs. Genre Not in Catalog:** Neither user has a perfect song. The sad fan's genre exists, so the +2.0 pushes an euphoric song to #1. The k-pop fan's genre doesn't exist, so mood decides and the list feels more reasonable. Oddly, having your genre in the catalog made the result worse here.

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

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
