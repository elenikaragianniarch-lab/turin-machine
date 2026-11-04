# Chapter 1 — Data-Driven Design Workflows
**Skills Tutor: Ioana Drogeanu**

## Overview
This chapter collects and processes four datasets about Turin through web scraping, 
API generation, machine learning, and visualisation. The datasets form the foundation 
for the cross-domain analysis in Chapter 2 and the computational design in Chapter 3.

## Structure

### Scraping/
- `britishpathe_turin.ipynb` — Scrapes British Pathé archive for Turin footage (205 clips)
- `VIDEOS.xlsx` — British Pathé dataset with titles, URLs, thumbnails, summaries
- `thumbnails_turin/` — 205 thumbnail images
- `imdb_turin.ipynb` — Scrapes IMDb for Turin films (286 films, genres, plot summaries)
- `films.csv` — IMDb dataset
- `fctp_industrial_turin.ipynb` — Scrapes FCTP industrial buildings catalogue (68 buildings)
- `fctp_industrial_turin.csv` — FCTP dataset

### API Interaction/
- `api_turin_dialogues.ipynb` — GPT-4o-mini generates Franco × Nietzsche dialogues at 24 locations
- `dialogues/` — 24 individual dialogue text files (one per location)

### Visualising_Plotting/
- `visualisations_turin.ipynb` — All visualisations: standard charts, advanced plots, architectural diagrams
- `OUTPUTS/` — Generated charts organised by dataset (british_pathe, imdb, fctp, dialogues, cross_dataset)

### Machine_Learning/
- `machine_learning.ipynb` — LSTM next-word prediction + DistilBERT fine-tuning on combined corpus
- `outputs/` — All training outputs:
  - `best_lstm_next_word.pt` — Best LSTM model weights (4.5MB)
  - `combined_corpus.csv` — Combined text corpus used for training
  - `distilbert_outputs.csv` — DistilBERT template filling results
  - `generated_seed_outputs.csv` — LSTM free generation from seed prompts
  - `generated_template_outputs.csv` — LSTM template filling results
  - `lstm_final_outputs.csv` — Final selected LSTM outputs
  - `selected_output_final.png` — LSTM vs DistilBERT comparison table
  - `training_loss_plot.png` — Training and validation loss curve
  - `vocab.json` — Model vocabulary

## Large files (not included)
- `fctp_images/` — 2254 FCTP building photographs
- `collection/` — 665 IMDb film stills
- `posters/` — 235 IMDb film posters
- `distilbert_finetuned/` — Fine-tuned DistilBERT model (255MB + 511MB checkpoint)

Large files (model weights, scene files, full image sets) are not included in this repository and are available on request.

