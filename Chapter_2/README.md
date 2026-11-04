# Chapter 2 — Projecting Between Domains
**Skills Tutor: Ioana Drogeanu**

## Overview
This chapter vectorises the four Turin datasets and trains two Self-Organising Maps 
to find semantic correspondences across text and image domains.

## Structure

### Vectorization/
- `vectorisation_turin.ipynb` — Vectorises all four datasets:
  - Text: TF-IDF, Word2Vec (SVD), Sentence Embeddings (MiniLM)
  - Images: HOG, CLIP (ViT-B-32)
  - Includes t-SNE comparison plots for all methods
- `dialogue_vectorisation.ipynb` — Dialogue-only vectorisation:
  - TF-IDF heatmap per location
  - Word2Vec semantic neighbours
  - PCA Conceptual Map of Turin (24 locations in semantic space)
  - Geographic keyword map
- `Outputs/comparison/` — t-SNE comparison plots (text and image methods)
- `Outputs/dialogues/` — Dialogue vectorisation outputs and conceptual maps
- `Outputs/image/` — Image vectorisation plots (HOG, CLIP)
- `Outputs/text/` — Text vectorisation plots (TF-IDF, Word2Vec, Sentence Embeddings)

### SOM/
- `som_turin.ipynb` — Two Self-Organising Maps using NumpySOM:
  - Text SOM 20×20 trained on sentence embeddings (573 documents)
  - Image SOM 18×18 trained on CLIP embeddings (2757 images)
  - QE and TE monitoring across 20 epochs with best epoch selection
  - PCA-RGB visualisation using two methods for both SOMs
  - 10 text search examples + 10 image search examples (activation maps)
- `text_som/` — Text SOM visualisations (QE/TE plots, source map, PCA-RGB, visual grid)
- `image_som/` — Image SOM visualisations (QE/TE plots, source map, PCA-RGB, visual grid)
- `search_examples/` — 20 search activation maps (10 text + 10 image)

## Large files (not included)
- `sentence_embeddings.npy` — Text vectors (573 × 384)
- `clip_vectors.npy` — Image vectors (2757 × 512)
- `hog_vectors.npy` — HOG image vectors
- `word2vec_avg_vectors.npy` — Word2Vec averaged vectors
- `text_som_weights.npy` — Trained Text SOM weights
- `image_som_weights.npy` — Trained Image SOM weights

Large files (model weights, scene files, full image sets) are not included in this repository and are available on request.
