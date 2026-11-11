# Do legal AI benchmarks agree on which model is best?

Draft, 11 November 2026. Not committed to the site.

## The finding

Six legal benchmarks rank the same current models. Two of them typically agree at 0.32 (Spearman rank correlation, where 0 is an unrelated order and 1 is an identical order). Eight coding benchmarks on the same models typically agree at 0.72.

| | Benchmarks | Pairs | Median agreement | 95% interval |
|---|---|---|---|---|
| Legal | 6 | 15 | 0.32 | 0.07 to 0.56 |
| Coding | 8 | 28 | 0.72 | 0.54 to 0.84 |

The gap is 0.41, with a 95% interval of 0.15 to 0.65. Coding came out at or below law in 0.03% of resamples.

This is not because legal benchmarks are unrepeatable. Harvey's LAB has been run by three evaluators (Vals, Artificial Analysis, Mercor), and their rankings agree at 0.83 to 0.95. A coding benchmark run by two evaluators (Terminal-Bench 4, Vals and Artificial Analysis) agrees at 0.96.

## The six legal benchmarks

| Benchmark | Publisher | Models of the 37 | Top model | Average agreement with the other five |
|---|---|---|---|---|
| GDPx, legal domain | SemiAnalysis | 20 | Muse Wonder Full | 0.40 |
| Legal Research Bench | Vals | 37 | Gemini 4 Carbon | 0.39 |
| APEX-Agents, corporate law | Mercor | 29 | GPT-6 Astra | 0.38 |
| Legal AI Leaderboard | Certera | 23 | GPT-6.1 Sol | 0.23 |
| LAB (Vals' run) | Harvey | 37 | Gemini 4 Argon | 0.22 |
| BAR | Legora | 15 | Claude Opus 5.5 | 0.21 |

Every pair, with the number of shared models, is in `data/pairs.csv`. The scores used are in `data/scores.csv`.

## Method

- **Models.** The 37 models Vals ran on Harvey's LAB between 19 October and 9 November 2026. This set was chosen because it is defined by recency, not by score. Each pair of benchmarks is compared on the models both tested, and a pair needs at least 10 shared models.
- **Scores.** Each benchmark's own headline score, taken from the publisher's site on 11 November 2026. Where a source ran a model at several effort settings, the highest setting is used.
- **Agreement.** Spearman rank correlation between two benchmarks' scores.
- **Intervals.** Models were resampled with replacement 3,000 times and every statistic recomputed.
- **Coding reference.** Terminal-Bench 4, Vibe Code, Code Migration, IOI, ProgramBench and SWE-bench Multimodal (all as run by Vals), plus FrontierCode 2 and SciCode (Artificial Analysis).

## Inclusion rule

A legal benchmark is included if its publisher posts it on its own site, it gives a score per model, and it covers at least 15 of the 37 models. Certera and GDPx meet the rule. Left out:

- **Vals Immigration:** 19 models, and Vals already has one benchmark in the set.
- **Surge DAYJOB law:** not yet published by Surge, 14 models.
- **Snorkel legal and Scale PRBench legal:** 11 models each.
- **legalbenchmarks.ai (two benchmarks):** 15 models each, left out by choice as small and little known.
- **GDP.pdf legal slice, LegalBench, LEXam, RedlineBench, GDPval:** too few current models, or a slice of a general benchmark.

With all twelve legal benchmarks that had current models, the median agreement is the same 0.32 (53 pairs, interval 0.15 to 0.54).

## Robustness

| Check | Legal | Coding | Gap |
|---|---|---|---|
| Main result | 0.32 | 0.72 | 0.41 |
| Coding reference limited to four benchmarks | 0.32 | 0.70 | 0.39 |
| Four models with uncertain name matches removed | 0.31 | 0.75 | 0.44 |
| Kendall's tau instead of Spearman | 0.23 | 0.56 | 0.32 |
| All models any source tested, not just the 37 | 0.32 | 0.77 | 0.45 |
| Only pairs sharing 15 or more models | 0.32 | 0.72 | 0.40 |
| Leaving out any one legal benchmark | 0.27 to 0.41 | 0.72 | 0.31 to 0.46 |

## Limits

- **It shows that the rankings differ, not why.** Legal work may be several distinct skills (research, drafting, review), in which case low agreement is expected and not a flaw in any benchmark.
- **The benchmarks measure different things.** Certera is blind votes by legal professionals on their own prompts. The others are rubric-graded tasks. Legora and GDPx run each model inside a product or lab harness, so a score reflects the model plus that setup.
- **Some are small.** GDPx's legal domain is 20 tasks and no model fully passes any of them, so it reports partial scores. Legora publishes only scores relative to its average, with many ties.
- **Overlaps are small.** Pairs share between 11 and 37 models. Individual bars have wide intervals, and three of the six cross zero.
- **Margins of error are mostly unpublished.** Only Vals publishes a standard error per model, so noise in each benchmark could not be removed pair by pair. The LAB reruns are the evidence that noise alone does not explain the result.
- **Effort settings differ between sources.** Vals ran Claude Fable 5.2 at high effort and others ran it at max. The same mismatch applies to the coding reference, where agreement stayed high.
- **Coding benchmarks are not a gold standard.** They are a reference from a field where benchmarks are broadly trusted.

## Other observations from the data

- **LAB's scoring rule shrinks scores without reordering models.** On Vals' run, models pass 73% to 96% of individual rubric criteria but only 2% to 27% of whole tasks. The two rankings agree at 0.88.
- **LAB's ranking changes when hallucinations are penalised.** Artificial Analysis zeroes any task with a material hallucination. Its ungated and gated rankings agree at 0.75. Gemini 4 Argon falls from 20.8% to 3.9%. Artificial Analysis published this itself in October.
- **The hallucination check depends on the checking model.** In Artificial Analysis' own comparison on 20 tasks, the count of material hallucinations ranged from 1.4 to 23.5 per task depending on which model did the checking. It uses the strictest, GPT-6 Sol.

## Files

- `legal-benchmarks-agreement.png`: the chart.
- `data/pairs.csv`, `data/scores.csv`, `data/final.json`: results.
- `scripts/`: the analysis code. Raw downloaded leaderboards (about 400 MB) are in `/home/user/benchstudy/raw`, outside this folder.
