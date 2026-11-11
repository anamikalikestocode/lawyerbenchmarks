# Do legal AI benchmarks agree on which model is better?

Draft, 11 November 2026. On a draft branch, not on the site.

## The finding

Pick any two current AI models. Two legal benchmarks agree on which one is better 62% of the time. Two coding benchmarks agree 79% of the time, on the same pool of models. Guessing would give 50%.

| Comparison | Agreement on which of two models is better | 95% interval |
|---|---|---|
| The same benchmark, run by two evaluators | 85% to 94% | range across four reruns |
| Two different coding benchmarks (8 benchmarks, 28 pairings) | 79% | 71% to 85% |
| Two different legal benchmarks (5 benchmarks, 10 pairings) | 62% | 53% to 72% |

The gap between coding and legal is 17 points, with a 95% interval of 7 to 26. Coding came out at or below legal in 0.2% of resamples.

The same result as a rank correlation (Spearman, where 0 is an unrelated order and 1 is identical): legal benchmarks typically agree at 0.32 (interval 0.06 to 0.57), coding benchmarks at 0.74 (0.56 to 0.84). The gap is 0.41, with an interval of 0.15 to 0.66.

Legal benchmarks do agree more often than chance. They agree less than coding benchmarks do, and much less than one benchmark agrees with a rerun of itself. Harvey's LAB has been run by three evaluators (Vals, Artificial Analysis, Mercor), and those runs agree 85% to 92% of the time. Terminal-Bench 4, run by Vals and Artificial Analysis, agrees 94% of the time.

## The five legal benchmarks

| Benchmark | Publisher | Run by | Models of the 37 | Top model | Agreement with the other four | 95% interval |
|---|---|---|---|---|---|---|
| Legal Research Bench | Vals | Vals | 37 | Gemini 4 Carbon | 67% | 57% to 77% |
| APEX-Agents, corporate law | Mercor | Mercor | 30 | GPT-6 Astra | 63% | 53% to 74% |
| LAB | Harvey | Vals | 37 | Gemini 4 Argon | 62% | 51% to 73% |
| BAR | Legora | Legora | 15 | Claude Opus 5.5 | 58% | 42% to 72% |
| Legal AI Leaderboard | Certera | Certera | 24 | GPT-6.1 Sol | 57% | 47% to 71% |

The intervals overlap almost completely, so the order of the five says little. The score measures agreement with the other four, not quality: a low score means a benchmark ranks models differently, not that it is wrong.

Harvey wrote LAB, but its own published results cover only older models. Scores for current models come from other parties running it. Vals' run is used because it covers the most models and reports a margin of error for each score. Vals Legal Research is a separate benchmark with its own tasks.

| Pairing | Shared models | Agree on which of two models is better |
|---|---|---|
| Harvey LAB and Vals Legal Research | 37 | 75% |
| Mercor APEX law and Certera | 23 | 69% |
| Vals Legal Research and Mercor APEX law | 30 | 69% |
| Vals Legal Research and Legora BAR | 15 | 64% |
| Harvey LAB and Legora BAR | 15 | 62% |
| Harvey LAB and Mercor APEX law | 30 | 62% |
| Vals Legal Research and Certera | 24 | 60% |
| Mercor APEX law and Legora BAR | 15 | 54% |
| Legora BAR and Certera | 15 | 52% |
| Harvey LAB and Certera | 24 | 48% |

Every pairing is in `data/pairs.csv` and the scores used are in `data/scores.csv`.

## Method

- **Models.** The 37 models Vals ran on Harvey's LAB between 19 October and 9 November 2026. This set is defined by recency, not by score. Each pairing of benchmarks is compared on the models both tested, and needs at least 10 shared models.
- **Scores.** Each benchmark's own headline score, taken from the publisher's site on 11 November 2026. Where a source ran a model at several effort settings, the highest setting is used.
- **Agreement.** For two benchmarks, the share of model pairs they put in the same order, over the models both tested (ties dropped). A group's figure is the average over every pairing in the group. Spearman rank correlation is reported alongside, as the median over pairings.
- **Intervals.** Models were resampled with replacement and every statistic recomputed (2,000 times for the agreement shares, 3,000 for the correlations).
- **Coding reference.** Terminal-Bench 4, Vibe Code, Code Migration, IOI, ProgramBench and SWE-bench Multimodal (all as run by Vals), plus FrontierCode 2 and SciCode (Artificial Analysis).
- **Model names.** Sources label models differently. Names were matched by rule and then checked by hand. Three labels were treated as the same model as a differently named entry elsewhere: Reflection's Beam, Tencent's Hy4 and Nvidia's Nemotron 3.5 Super VL. Four further matches are less certain (Mistral Large 4, DeepSeek V4.1 Flash, Qwen 3.8 Max, Hy4), and the result is also reported without those models.

## Which benchmarks are in, and why

The five legal benchmarks in the charts were chosen by hand: the best-known ones with enough current models. To check that the choice does not drive the result, one written rule was also applied the same way to every field.

**The rule.** A benchmark counts if (1) it has its own published leaderboard with a score per model, (2) at least 15 of the 37 models are on it, (3) it is the latest version, and (4) it is counted once, using the run with the most of the 37 models when several evaluators ran it. Combined indices and breakdowns inside a general benchmark do not count. A field is reported only if at least three benchmarks qualify. Vals' benchmarks are assigned to fields by Vals' own labels.

Every legal candidate found, and what the rule does with it:

| Benchmark | Run by | Models of the 37 | Rule | In the hand-picked five |
|---|---|---|---|---|
| Harvey LAB (Vals run) | Vals | 37 | in | yes |
| Legal Research Bench (Vals) | Vals | 37 | in | yes |
| Mercor APEX, corporate law | Mercor | 30 | in | yes |
| Certera | Certera | 24 | in | yes |
| GDPx legal (SemiAnalysis) | SemiAnalysis | 20 | in | no, left out by choice |
| Immigration (Vals) | Vals | 19 | in | no, left out by choice |
| Legora BAR | Legora | 15 | in | yes |
| Contract Workflows (legalbenchmarks.ai) | legalbenchmarks.ai | 15 | in | no, left out by choice |
| Data Extraction (legalbenchmarks.ai) | legalbenchmarks.ai | 15 | in | no, left out by choice |
| GDP.pdf legal slice (AA) | Artificial Analysis | 34 | out: a breakdown inside a general benchmark, not its own leaderboard | no |
| Omniscience law slice (AA) | Artificial Analysis | 33 | out: a breakdown inside a general benchmark, not its own leaderboard | no |
| Harvey LAB (Mercor run) | Mercor | 27 | out: second run of a benchmark already listed | no |
| Harvey's Legal Agent Benchmark v1 (Vals) | Vals | 25 | out: older version of a benchmark already listed | no |
| Harvey LAB (AA run) | Artificial Analysis | 19 | out: second run of a benchmark already listed | no |
| DAYJOB law (Surge) | Fireworks copy | 14 | out: only 14 of the 37 models | no |
| LegalBench (Vals) | Vals | 13 | out: only 13 of the 37 models | no |
| SnorkelLegal | Snorkel | 11 | out: only 11 of the 37 models | no |
| PRBench legal (Scale) | Scale | 11 | out: only 11 of the 37 models | no |
| CorporateBench (Epiq) | Fireworks | 9 | out: only 9 of the 37 models | no |
| Dutch legal research DELTA | legalbenchmarks.ai | 5 | out: only 5 of the 37 models | no |
| CaseLaw v2 (Vals) | Vals | 1 | out: only 1 of the 37 models | no |

The legal figure under different choices:

| Choice | Benchmarks | Pairings | Agreement | 95% interval |
|---|---|---|---|---|
| The written rule | 9 | 36 | 63% | 57% to 70% |
| The hand-picked five (used in the charts) | 5 | 10 | 62% | 53% to 72% |
| Rule with a minimum of 10 models | 13 | 57 | 63% | 57% to 70% |
| Rule with a minimum of 20 models | 5 | 10 | 65% | 57% to 75% |
| Rule, one benchmark per publisher | 7 | 21 | 62% | 55% to 69% |
| Rule, plus the two Artificial Analysis slices | 11 | 55 | 63% | 57% to 69% |
| Rule, without Certera's votes | 8 | 28 | 64% | 56% to 72% |
| Rule, only benchmarks run by an independent evaluator or by vote | 7 | 21 | 62% | 56% to 69% |
| Only Harvey LAB, Vals Legal Research and Mercor APEX | 3 | 3 | 68% | 58% to 78% |

Every choice with five or more benchmarks gives 62% to 65%. The hand-picked five is at the low end of that range. With only three benchmarks the figure is 68%, the gap to coding shrinks to 10 points, and its interval (0 to 21) reaches zero. Mercor's corporate-law score is one job out of three inside APEX-Agents; it is counted because Mercor publishes it as its own leaderboard.

## Other fields, same pool of models, same rule

| Field | Benchmarks | Pairings | Agreement | 95% interval | Run by |
|---|---|---|---|---|---|
| Science | 3 | 3 | 84% | 72% to 92% | Vals |
| Coding | 9 | 36 | 79% | 71% to 84% | Vals, Artificial Analysis |
| Office work | 5 | 10 | 77% | 70% to 82% | Artificial Analysis, Mercor |
| Finance | 3 | 3 | 73% | 64% to 81% | Vals |
| Legal (written rule) | 9 | 36 | 63% | 57% to 70% | six different parties |
| Legal (hand-picked five) | 5 | 10 | 62% | 53% to 72% | four different parties |

Two fields have only two qualifying benchmarks, so one pairing each, and are not reported as fields: medicine (77%, interval 68% to 86%) and cyber (40%, interval 20% to 64%). Cyber's single pairing is lower than legal. An earlier draft showed medicine and merged a maths benchmark into science; both were inconsistent with the rule and have been removed. Maths and general knowledge have one qualifying benchmark each.

Science and finance were each run by a single evaluator, and legal benchmarks by four to six different parties. Where the evaluator differs, coding pairings agree 80% of the time (12 pairings), against 60% for legal (9 pairings). The one legal pairing run by the same evaluator (Harvey LAB and Vals Legal Research, both run by Vals) agrees 75% of the time.

A legal benchmark agrees with a coding benchmark 66% of the time (40 pairings), against 62% with another legal benchmark. The difference is 4 points with an interval of -2 to 10, so it is not clearly different from zero. There is no sign that the legal benchmarks share a ranking of their own beyond general model strength.

## The same models for every field

The comparisons above use the same pool of 37 models, but each pairing only uses the models both benchmarks tested, and legal pairings share fewer models (15 to 37) than coding pairings. To rule that out as the cause, every field was scored on exactly the same 15 models, the ones all five legal benchmarks tested.

| Field | Agreement on those 15 models | 95% interval | Gap to legal | Interval on the gap |
|---|---|---|---|---|
| Science | 83% | 69% to 93% | 26 points | 9 to 40 |
| Coding | 76% | 67% to 84% | 20 points | 6 to 32 |
| Office work | 74% | 64% to 83% | 18 points | 4 to 31 |
| Finance | 73% | 58% to 84% | 16 points | 2 to 28 |
| Legal | 57% | 47% to 67% | | |

The gap is at least as large on identical models. On this strictest comparison the legal interval includes 50%, so legal agreement cannot be clearly told apart from a coin flip there.

## Where the gap comes from

Vals reports a margin of error for every score, so for Vals-run benchmarks the effect of noise can be separated from real disagreement. The ceiling is how often two benchmarks would agree if they ranked models identically underneath and differed only by their reported noise.

| Field (Vals-run benchmarks only) | Ceiling from noise alone | Actual agreement | Shortfall |
|---|---|---|---|
| Science | 90% | 84% | 6 points |
| Coding | 87% | 80% | 7 points |
| Finance | 83% | 73% | 10 points |
| Legal | 83% | 68% | 14 points |

- **Noise caps every field well below 100%.** Current models score close together relative to the margins of error. Legal and finance have the same ceiling, so noise does not explain why legal is lower than finance.
- **With one evaluator, legal is close to finance.** 68% against 73%, on three legal pairings. One of them (Harvey LAB and Vals Immigration, 58%) accounts for most of the difference.
- **The larger drop comes when different parties build and run the benchmarks.** Legal falls from 68% within Vals to 60% across parties. Coding does not fall (78% within one evaluator, 80% across).

The cross-party drop is consistent with each party applying its own standard of good legal work, and also with differences in setup, such as Legora testing inside its own product and Certera collecting votes on chat answers. The data cannot separate the two. Pairings of the three rubric-graded agent benchmarks (Harvey, Vals, Mercor) agree more than pairings involving Certera or Legora.

## Tasks or standard?

Two benchmarks can disagree because they set different tasks or because they judge answers differently. These checks hold one fixed and change the other (figures from `scripts/tasks_vs_standard.py`).

| What changes | Agreement on which of two models is better |
|---|---|
| Nothing: one benchmark split into random halves (LAB, Vals Legal Research) | 87% |
| Area of law: LAB's deal-work practice areas against its disputes and regulatory ones | 90% |
| Who runs it: LAB run by Vals, Artificial Analysis and Mercor | 85% to 92% |
| The scoring rule: LAB scored all-or-nothing against per criterion | 88% |
| Kind of work: Legora's task families (draft, review, extract and so on), 9 models | 73%, against 80% for the same family in two editions |
| One rule about what counts as good: LAB with and without the penalty for made-up facts, 25 models | 79% |
| The whole benchmark: two different legal benchmarks | 62% |

For reference, random halves of Terminal-Bench 4 (coding) agree 90% of the time and of Vals' Finance Agent 81%. Inside one benchmark, legal tasks are as consistent as coding tasks.

On the same LAB answers, ranking models by rubric pass rate and ranking them by fewest made-up facts agree 55% of the time. Area of law and the evaluator make no measurable difference. Kind of work costs a few points on thin data. A change in what counts as a good answer moves rankings the most of the things that could be isolated. Legora's comparison rests on 9 models, and the made-up-facts check is done by a single AI judge.

## Robustness (Spearman rank correlation)

| Check | Legal | Coding | Gap |
|---|---|---|---|
| Main result | 0.32 | 0.74 | 0.41 |
| Coding reference limited to four benchmarks | 0.32 | 0.73 | 0.41 |
| Four models with uncertain name matches removed | 0.35 | 0.76 | 0.41 |
| Kendall's tau instead of Spearman | 0.23 | 0.56 | 0.33 |
| All models any source tested, not just the 37 | 0.33 | 0.77 | 0.44 |
| Only pairings sharing 15 or more models | 0.32 | 0.74 | 0.41 |
| Leaving out any one legal benchmark | 0.21 to 0.41 | 0.74 | 0.32 to 0.53 |

On the agreement-share measure:

| Check | Legal | Coding |
|---|---|---|
| Main result | 62% | 79% |
| Harvey LAB taken from Mercor's run instead of Vals' | 61% | 79% |
| Harvey LAB taken from Artificial Analysis' run, ungated | 61% | 79% |
| Harvey LAB taken from Artificial Analysis' run, hallucination-gated | 62% | 79% |
| Pairings run by the same evaluator | 75% (1 pairing) | 78% (16 pairings) |
| Pairings run by different evaluators | 60% (9 pairings) | 80% (12 pairings) |
| Every field on the same 15 models | 57% | 76% |

## Limits

- **It shows that the rankings differ, not why.** Legal work may be several distinct skills (research, drafting, review), in which case lower agreement is expected and is not a flaw in any benchmark.
- **The benchmarks measure different things.** Certera is blind votes by legal professionals on their own prompts. The others are rubric-graded tasks. Legora runs each model inside its own product, so a score reflects the model plus that setup.
- **Five benchmarks is a small set.** There are ten pairings, and four of them involve Legora, which shares only 15 models with the others and publishes only scores relative to its average, with many ties.
- **Margins of error are mostly unpublished.** Only Vals publishes a standard error per model, so noise could be separated from real disagreement only for Vals-run benchmarks.
- **Effort settings differ between sources.** Vals ran Claude Fable 5.2 at high effort and others ran it at max. The same mismatch applies to the coding reference, where agreement stayed high.
- **The other fields are thin.** Science and finance have three benchmarks each, all run by Vals.
- **Coding benchmarks are not a gold standard.** They are a reference from a field where benchmarks are broadly trusted.
- **It is one month of data.**

## Other observations from the data

- **LAB's scoring rule shrinks scores without reordering models.** On Vals' run, models pass 73% to 96% of individual rubric criteria but only 2% to 27% of whole tasks. The two rankings have a rank correlation of 0.88.
- **LAB's ranking changes when hallucinations are penalised.** Artificial Analysis zeroes any task with a material hallucination. Its ungated and gated rankings have a rank correlation of 0.75, and Gemini 4 Argon falls from 20.8% to 3.9%. Artificial Analysis published this itself in October.
- **The hallucination check depends on the checking model.** In Artificial Analysis' own comparison on 20 tasks, the count of material hallucinations ranged from 1.4 to 23.5 per task depending on which model did the checking. It uses the strictest, GPT-6 Sol.

## Files

- `slide1-benchmark-of-benchmarks.png`, `slide2-benchmark-of-legal-benchmarks.png`: the two slides. `slide1-no-footer.png` and `slide2-no-footer.png` are the same without the footer line.
- `option1-winners.png`, `option2-ten-dots.png`, `benchmark-of-legal-benchmarks-50.png`, `benchmark-of-legal-benchmarks.png`, `legal-benchmarks-agreement.png`: earlier chart versions, redrawn from the same numbers.
- `data/`: results. `pairs.csv` and `scores.csv` are the pairings and scores for the five legal benchmarks; the `.json` files hold every figure quoted here.
- `scripts/`: the analysis code. `make_readme.py` builds this file from the result files. Raw downloaded leaderboards (about 400 MB) are not in the repo.
