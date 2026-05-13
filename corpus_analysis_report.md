# Corpus-Level Analysis Report
## Arabic–English Code-Switched Dataset

**Dataset:** `ArEnTC.xlsx`  
**Total Sentences:** 105,652  
**Topics:** Business, Education, Finance, Health, Medical, Shopping, Social, Sports, Tech  

---

## 1. Corpus Overview

| Metric | Value |
|---|---|
| Total sentences | 105,652 |
| Total tokens | 1,479,407 |
| Unique token types | 15,661 |
| Type-token ratio | 0.0106 |
| Mean sentence length | 14.0 tokens (σ = 1.5) |
| Median sentence length | 14 tokens |
| Mean character length | 86.9 characters (σ = 9.5) |

---

## 2. Script Distribution

| Metric | Value |
|---|---|
| Arabic tokens | 1,091,718 (73.8%) |
| Latin tokens | 387,656 (26.2%) |
| Sentences with Arabic as dominant script | 104,813 (99.2%) |

Arabic is the matrix language in 99.2% of sentences, consistent with the intended 70/30 Arabic–English generation ratio.

---

## 3. Code-Switch Point Analysis

| Metric | Value |
|---|---|
| Mean switches per sentence | 3.69 (σ = 0.89) |
| Median switches per sentence | 4 |
| Maximum switches in a sentence | 9 |
| Sentences with ≥3 switch points | 92,918 (87.9%) |

### Switch Point Position Distribution
| Position | Percentage |
|---|---|
| Early (first third of sentence) | 30.8% |
| Mid (middle third) | 39.1% |
| Late (final third) | 30.1% |

Switch points are distributed without strong positional bias, consistent with intra-sentential switching patterns in naturalistic Arabic–English corpora.

---

## 4. Script Run Length Analysis

| Metric | Arabic Runs | Latin Runs |
|---|---|---|
| Mean run length | 3.80 tokens | 1.86 tokens |
| Median run length | 3 tokens | 2 tokens |
| Maximum run length | 17 tokens | 16 tokens |

### Latin Run Length Distribution
| Run Length | Percentage |
|---|---|
| 1 token (single insertion) | 20.7% |
| 2 tokens (short phrase) | 73.1% |
| 3+ tokens (longer span) | 6.2% |

73.1% of English insertions are exactly two tokens long (typically noun phrases or domain terms), mirroring structural constraints observed in real Arabic–English code-switched speech.

---

## 5. Code-Mixing Index (CMI)

CMI is defined as the proportion of non-dominant-language tokens relative to total language-bearing tokens per sentence.

| Metric | Value |
|---|---|
| Mean CMI | 0.264 (σ = 0.080) |
| Sentences with CMI > 0.10 | 97.7% |
| Sentences with CMI > 0.20 | 77.9% |
| Sentences with CMI > 0.30 | 32.4% |

A mean CMI of 0.264 indicates moderate-to-high intra-sentential mixing throughout the corpus.

---

## 6. Per-Topic Statistics

| Topic | Sentences | Avg Tokens | Avg Switches | Arabic% | Latin% | CMI | Unique Latin Types |
|---|---|---|---|---|---|---|---|
| Business | 11,714 | 14.00 | 3.71 | 73% | 27% | 0.26 | 1,841 |
| Education | 11,763 | 14.02 | 3.69 | 74% | 26% | 0.26 | 1,765 |
| Finance | 11,671 | 14.01 | 3.69 | 74% | 26% | 0.26 | 1,790 |
| Health | 11,706 | 14.01 | 3.69 | 73% | 26% | 0.26 | 1,769 |
| Medical | 11,914 | 14.00 | 3.69 | 73% | 27% | 0.26 | 1,788 |
| Shopping | 11,649 | 13.99 | 3.69 | 73% | 27% | 0.26 | 1,770 |
| Social | 11,819 | 14.00 | 3.70 | 74% | 26% | 0.26 | 1,811 |
| Sports | 11,678 | 13.99 | 3.69 | 74% | 26% | 0.26 | 1,778 |
| Tech | 11,738 | 13.99 | 3.69 | 74% | 26% | 0.26 | 1,754 |
| **Total** | **105,652** | **14.0** | **3.69** | **73.8%** | **26.2%** | **0.264** | — |

Topic distributions are balanced across all nine domains, with each class containing between 11,649 and 11,914 sentences. The uniformity across topics reflects the controlled generation protocol, where identical length and ratio constraints were applied to all categories.

---

## 7. Generation Protocol Summary

| Parameter | Specification |
|---|---|
| Generation model | GPT-4o mini |
| Target sentence length | 15–20 words |
| Arabic–English ratio | ~70% Arabic / 30% English |
| Switching type | Intra-sentential and inter-sentential |
| Switching level | Primarily phrase-level |
| Sentence structures | Statements, questions, conditional structures |
| Topic keyword injection | Dynamic per topic |
| Preprocessing | Normalization, noise removal, deduplication, monolingual filtering |

---

## Notes

- All 105,652 sentences in the released corpus are verified code-switched (contain both Arabic and English tokens).
- CMI formula: `(total_language_tokens − dominant_language_tokens) / total_language_tokens`
- Script classification is token-level based on Unicode character ranges (Arabic: U+0600–U+06FF and extended blocks; Latin: A–Z, a–z).
- Switch point defined as an adjacent token-pair boundary where script changes between Arabic and Latin.

