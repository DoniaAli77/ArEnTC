# AR-EN-Synth-Topic

This repository contains the ArabicCS-Topic dataset, a large-scale Arabic–English code-switched corpus for topic classification. The dataset consists of 105,652 synthetic sentences spanning nine domains, generated under controlled prompting conditions to reflect realistic intra-sentential code-switching behavior between Arabic and English.

## Dataset Description

Each sentence is labeled with one of nine topic categories: **Business, Education, Finance, Health, Medical, Shopping, Social, Sports,** and **Technology**. Sentences were generated using GPT-4o mini with a target Arabic–English ratio of 70/30, a sentence length of 15–20 words, and phrase-level switching across diverse sentence structures. A preprocessing step was applied to normalize text, remove noise, deduplicate, and filter any monolingual artifacts, yielding a fully mixed-script corpus.

A full corpus-level analysis is provided in `corpus_analysis_rich.xlsx`, covering token distribution, switch point frequency, code-mixing index, run length analysis, vocabulary statistics, and per-topic breakdowns.

## Generation Protocol

Sentences were generated using the **GPT-4o mini** model via the OpenAI API 
in batches of 10 sentences per call, with temperature set to 0.7 for diversity. 
Each prompt specified the target topic, sentence length (15–20 words), 
Arabic–English ratio (~70% Arabic / 30% English), and encouraged phrase-level 
intra-sentential switching across varied sentence structures (statements, 
questions, conditionals, imperatives, cause-effect).

Generation was oversampled — targeting 12,000 sentences per topic to yield 
~10,000 unique ones after deduplication. Topic-specific keywords and complexity 
templates (simple, moderate, complex) were randomly sampled per batch to 
maximise lexical and structural diversity.

The full generation script is provided in `generation_script.py` for reproducibility.

## Our Paper

> *Prompting vs Ensemble Architectures for Arabic–English Code-Switched Classification*
> Donia Ali, Salma Haytham, Sandra George, Caroline Sabty
> German International University, Cairo, Egypt
> *(citation link will be added upon publication)*

## Cite Us

Citation will be added upon publication.

## Repository Contents

| File | Description |
|---|---|
| `AR-EN-CodeSwitch-Topic.xlsx` | Full cleaned dataset (105,652 sentences) |
| `corpus_analysis.xlsx` | Detailed corpus-level analysis (13 sheets) |
| `corpus_analysis_report.md` | Human-readable analysis report |
| `README.md` | This file |
