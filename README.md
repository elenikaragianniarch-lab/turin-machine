# Turin Machine

**Two AI characters walk Turin and talk. Their words become a spatial vocabulary that builds architecture, sentence by sentence.**

Individual project by **Eleni Karagianni**, RC11, MArch Urban Design, The Bartlett (UCL), 2025–26. Skills tutor: Ioana Drogeanu.

Portfolio: https://eleni-portfolio-beige.vercel.app/#turin-machine · Process blog: https://eleni-karagiannii.tumblr.com

---

## What it does

Turin Machine reads the city through four very different datasets, lets two persona-driven LLM agents walk and talk through it, and turns their language into 3D form.

- **Nietzsche**, the philosopher who lived in Turin, reads the city through concepts, critique and feeling.
- **Franco**, the blind detective from Dario Argento's *The Cat o' Nine Tails*, reads it through sound, touch and uncertainty.

Their conversations at 24 walk locations are vectorised, compared with images and archive material through Self-Organising Maps and CLIP, and finally used as a vocabulary that drives a parametric Blender system and an audio-reactive TouchDesigner network.

```
datasets ──► persona agents ──► vectorisation + SOMs ──► word vocabulary ──► Blender / TouchDesigner
(archive,     (GPT-4o mini,      (TF-IDF, MiniLM,          (43 words,           (42 variations,
 films,        24 walk            CLIP, NumpySOM)           soft / medium /      sentence accumulation,
 buildings,    locations)                                   chaotic)             audio-driven form)
 dialogues)
```

## Repository

| Folder | What's inside |
|---|---|
| [`Chapter_1/`](Chapter_1) | Data collection: scraping notebooks (British Pathé, IMDb, Film Commission Torino), the OpenAI API dialogue generator, LSTM next-word prediction and DistilBERT fine-tuning, visualisations |
| [`Chapter_2/`](Chapter_2) | Projecting between domains: TF-IDF, Word2Vec (SVD), MiniLM sentence embeddings, HOG and CLIP image vectors, a pure-NumPy SOM (text 20×20, image 18×18), cross-domain search examples |
| [`Chapter_3/`](Chapter_3) | Design: CLIP matching of visual fragments to walk locations, the Blender word-driven system, the sentence accumulation script, the TouchDesigner audio network |

Each chapter has its own README with details.

## Highlights

- **24 generated dialogues** between two persona agents, constrained by the cultural datasets (`Chapter_1/API Interaction/dialogues/`).
- **Own SOM implementation** in NumPy, trained on 573 sentence embeddings and 2,757 CLIP image embeddings.
- **Cross-modal retrieval:** 49 visual fragments matched to walk locations through CLIP and TF-IDF keywords.
- **Language as geometry:** in `Chapter_3/Blender/blender_word_driven_system.py`, 43 words from the dialogues drive 42 geometric variations; `sentence_script.py` compounds transformations word by word through a sentence.
- **Sound as data:** a recorded walk drives real-time deformation in TouchDesigner.

## Running it

Each notebook has its own `pip install` cell. Main dependencies: pandas, numpy, matplotlib, torch, open_clip_torch, sentence-transformers, scikit-learn, scikit-image, requests, beautifulsoup4, selenium, openai, python-dotenv. The Blender scripts run inside Blender's scripting workspace.

To regenerate dialogues, put your own key in a `.env` file:

```
OPENAI_API_KEY=your-key-here
```

`.env` is git-ignored and never committed.

## Data

Raw scraped data (British Pathé thumbnails and metadata, IMDb film data, Film Commission Torino building data) is **not included**, because it belongs to those sources. The scraping notebooks show exactly how it was collected. Model weights, embeddings, Blender scenes and full image sets are also left out for size and are available on request.

## Contact

Eleni Karagianni · eleni.karagianni.arch@gmail.com · [LinkedIn](https://www.linkedin.com/in/elenikaragiannii/)
