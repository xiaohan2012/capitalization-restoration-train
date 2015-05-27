#  Capitalization Restoration
---------------------------

# Problem Definition

Given a capitalized news title, restore the title to its orginal format.

For example, given the following new title:

```
CIS FMs Hold Summit in Belarus on Oct 10
```

the goal is to restore it to:

```
CIS FMs hold summit in Belarus on Oct 10
```

# Experiment Models

Four models are evaluated:

- **CRF**: 1st order Linear-chain conditional random field(with variation in feature set)
- **HMM**: 1st order Hidden Markov Model
- **Baseline 1**: it determines the word capitalization on whether the word exists in dictionary or not. If capitalized word exists while uncapitalized one does not, the word is likely to be a proper noun. Thus capitalize it.
- **Baseline 2**: it determines the word capitalization on whether the word appears as capitalized(excluding leading sentence word case) in the document or not. It the above predicate it true, capitalize it. Otherwise, lowercase it.

# Evaluation Metric

Word-level accuracy is used as the evaluation metric.

# Dataset

55351 news titles from various news sites are used for model evaluation.


For HMM and CRF, the first 50000 titles are used for training while the rest are used for evaluation.

# Feature selection in CRF
The following feature types are used:

- Lexical(`LEXICAL`)
- Whether the word appears capitalized in the corresponding document, excluding the case it appears at the sentence beginning(`CAP`)
- Whether the leading character of the word is in the alphabets(`ALPHA`)
- Whether it appears as the first word in the title(`HEAD`)

To see the effects of different feature set combinations, the following combinations are considered

- `LEXICAL`
- `HEAD`
- `ALPHA`
- `CAP`
- `ALPHA + CAP`
- `LEXICAL + ALPHA`
- `LEXICAL + ALPHA + CAP`
- `LEXICAL + ALPHA + CAP +  HEAD`

# Result

The following table lists the accuracy of the four models:

| **Model**    | *Baseline 1* | *Baseline 2* | *HMM* | *CRF(best)* |
|--------------+--------------+--------------+-------+-------------|
| **Accuracy** |        0.793 |        0.924 | 0.887 |      0.9420 |

Where *CRF(best)* is the CRF with the highest accuracy.

The following table lists the accuracy of CRF model with various feature set configuration:


| **Features** |     `LEXICAL` |          `HEAD` |           `ALPHA` |                   `CAP` |
|--------------+---------------+-----------------+-------------------+-------------------------|
| **Accuracy** |        0.9147 |          0.5812 |            0.7777 |                  0.6949 |




| **Features** | `ALPHA + CAP` | `LEXICAL + CAP` | `LEXICAL + ALPHA` | `LEXICAL + ALPHA + CAP` |
|--------------+---------------+-----------------+-------------------+-------------------------|
| **Accuracy** |        0.8889 |          0.9334 |            0.9221 |                  0.9420 |
