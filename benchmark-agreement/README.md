# Do legal AI benchmarks agree on which model is better?

Draft, 11 November 2026. On a draft branch, not on the site.

## The finding

Pick any two current AI models. Two legal benchmarks agree on which one is better 60% of the time. Two coding benchmarks agree 78% of the time, on the same models. Guessing would give 50%.

| Comparison | Agreement on which of two models is better | 95% interval |
|---|---|---|
| The same benchmark, run by two evaluators | 85% to 93% | range across four reruns |
| Two different coding benchmarks (8 benchmarks, 28 pairings) | 78% | 70% to 84% |
| Two different legal benchmarks (5 benchmarks, 10 pairings) | 60% | 52% to 69% |

The gap between coding and legal is 18 points, with a 95% interval of 8 to 27. Coding came out at or below law in none of 2,000 resamples. Counting only pairings where the two benchmarks were run by different evaluators gives 59% for legal and 78% for coding.

The same result as a rank correlation (Spearman, where 0 is an unrelated order and 1 is identical): legal benchmarks typically agree at 0.30 (interval 0.03 to 0.53), coding benchmarks at 0.72 (0.54 to 0.84). The gap is 0.43, with an interval of 0.18 to 0.69.

Legal benchmarks do agree more often than chance. They agree less than coding benchmarks do, and much less than one benchmark agrees with a rerun of itself. Harvey's LAB has been run by three evaluators (Vals, Artificial Analysis, Mercor), and those runs agree 85% to 92% of the time. Terminal-Bench 4, run by Vals and Artificial Analysis, agrees 93% of the time.

## The five legal benchmarks

| Benchmark | Publisher | Models of the 37 | Top model | Agreement with the other four | 95% interval |
|---|---|---|---|---|---|
| Legal Research Bench | Vals | 37 | Gemini 4 Carbon | 66% | 56% to 75% |
| APEX-Agents, corporate law | Mercor | 29 | GPT-6 Astra | 62% | 52% to 72% |
| LAB (Vals' run) | Harvey | 37 | Gemini 4 Argon | 60% | 49% to 71% |
| BAR | Legora | 15 | Claude Opus 5.5 | 58% | 42% to 72% |
| Legal AI Leaderboard | Certera | 23 | GPT-6.1 Sol | 55% | 45% to 68% |

The intervals overlap almost completely, so the order of the five says little. Every pairing is in `data/pairs.csv` and the scores used are in `data/scores.csv`.

| Pairing | Shared models | Agree on which of two models is better |
|---|---|---|
| Harvey LAB and Vals Legal Research | 37 | 75% |
| Mercor APEX law and Certera | 22 | 67% |
| Vals Legal Research and Mercor APEX law | 29 | 67% |
| Vals Legal Research and Legora BAR | 15 | 64% |
| Harvey LAB and Legora BAR | 15 | 62% |
| Harvey LAB and Mercor APEX law | 29 | 59% |
| Vals Legal Research and Certera | 23 | 57% |
| Mercor APEX law and Legora BAR | 15 | 54% |
| Legora BAR and Certera | 15 | 52% |
| Harvey LAB and Certera | 23 | 45% |

## Method

- **Models.** The 37 models Vals ran on Harvey's LAB between 19 October and 9 November 2026. This set is defined by recency, not by score. Each pairing of benchmarks is compared on the models both tested, and needs at least 10 shared models.
- **Scores.** Each benchmark's own headline score, taken from the publisher's site on 11 November 2026. Where a source ran a model at several effort settings, the highest setting is used.
- **Agreement.** For two benchmarks, the share of model pairs they put in the same order, over the models both tested (ties dropped). A group's figure is the average over every pairing in the group. Spearman rank correlation is reported alongside, as the median over pairings.
- **Intervals.** Models were resampled with replacement and every statistic recomputed (2,000 times for the agreement shares, 3,000 for the correlations).
- **Coding reference.** Terminal-Bench 4, Vibe Code, Code Migration, IOI, ProgramBench and SWE-bench Multimodal (all as run by Vals), plus FrontierCode 2 and SciCode (Artificial Analysis).

## What was left out

Artificial Analysis has no legal benchmark of its own. Its legal leaderboard is a run of Harvey's LAB, so it appears in the rerun comparison, not as a separate benchmark.

Left out by choice, as small or little known: SemiAnalysis GDPx (legal domain, 20 tasks, every model scores zero on its headline measure), the two legalbenchmarks.ai benchmarks, Vals Immigration (Vals already has one benchmark in the set).

Left out for too few current models, or because they are a slice of a general benchmark: Surge DAYJOB law, Snorkel legal, Scale PRBench legal, the GDP.pdf legal slice, LegalBench, LEXam, RedlineBench, GDPval.

With all twelve legal benchmarks that had current models, the median rank correlation is 0.32 (53 pairings, interval 0.15 to 0.54), close to the 0.30 from the five.

## Robustness (Spearman rank correlation)

| Check | Legal | Coding | Gap |
|---|---|---|---|
| Main result | 0.30 | 0.72 | 0.43 |
| Coding reference limited to four benchmarks | 0.30 | 0.70 | 0.41 |
| Four models with uncertain name matches removed | 0.31 | 0.75 | 0.44 |
| Kendall's tau instead of Spearman | 0.21 | 0.56 | 0.35 |
| All models any source tested, not just the 37 | 0.30 | 0.77 | 0.47 |
| Only pairings sharing 15 or more models | 0.30 | 0.72 | 0.43 |
| Leaving out any one legal benchmark | 0.18 to 0.35 | 0.72 | 0.37 to 0.54 |

## Limits

- **It shows that the rankings differ, not why.** Legal work may be several distinct skills (research, drafting, review), in which case lower agreement is expected and is not a flaw in any benchmark.
- **The benchmarks measure different things.** Certera is blind votes by legal professionals on their own prompts. The others are rubric-graded tasks. Legora runs each model inside its own product, so a score reflects the model plus that setup.
- **Five benchmarks is a small set.** There are ten pairings, and three of them involve Legora, which shares only 15 models with the others and publishes only scores relative to its average, with many ties.
- **Margins of error are mostly unpublished.** Only Vals publishes a standard error per model, so noise in each benchmark could not be removed pairing by pairing. The LAB reruns are the evidence that noise alone does not explain the result.
- **Effort settings differ between sources.** Vals ran Claude Fable 5.2 at high effort and others ran it at max. The same mismatch applies to the coding reference, where agreement stayed high.
- **Coding benchmarks are not a gold standard.** They are a reference from a field where benchmarks are broadly trusted.

## Possible reasons (not tested)

- **Different work:** research (Vals), producing documents from files (Harvey), corporate tasks (Mercor), chat answers judged by lawyers (Certera).
- **Different grading:** Harvey's LAB is all-or-nothing against long checklists, with a median of 54 criteria per task. Others average partial credit or count votes.
- **Different setups:** Legora tests inside its own product.
- **Noise:** small overlaps and tied scores.

## Other observations from the data

- **LAB's scoring rule shrinks scores without reordering models.** On Vals' run, models pass 73% to 96% of individual rubric criteria but only 2% to 27% of whole tasks. The two rankings have a rank correlation of 0.88.
- **LAB's ranking changes when hallucinations are penalised.** Artificial Analysis zeroes any task with a material hallucination. Its ungated and gated rankings have a rank correlation of 0.75, and Gemini 4 Argon falls from 20.8% to 3.9%. Artificial Analysis published this itself in October.
- **The hallucination check depends on the checking model.** In Artificial Analysis' own comparison on 20 tasks, the count of material hallucinations ranged from 1.4 to 23.5 per task depending on which model did the checking. It uses the strictest, GPT-6 Sol.

## Files

- `legal-benchmarks-agreement.png`: the chart.
- `data/pairs.csv`, `data/scores.csv`, `data/final.json`, `data/concord.json`: results.
- `scripts/`: the analysis code (`final.py`, `concord.py`, `chart2.py` produce the numbers and chart above). Raw downloaded leaderboards (about 400 MB) are not in the repo.
