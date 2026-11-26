# Preregistered protocol for H2

**Version:** 1.0.0 · **Date:** 2026-11-26 · **Status:** template, not yet executed

This document is a preregistration template for the strong hypothesis:
a conscious observer's intention biases a live physical random source.
It is deliberately specific. Change it only by a dated amendment, and
report every amendment.

## 0. Scope

- **Tested:** H2 — human intention changes the distribution of a live
  physical source.
- **Not tested:** H1 — the deterministic selection rule biases a classical
  source. H1 is already falsified for the reference architecture; see
  [`MATH.md`](MATH.md) and [`RESULTS-v1.md`](RESULTS-v1.md).
- **Not tested:** every conceivable form of "observer effect". The protocol
  fixes one operationalization and one primary endpoint.

## 1. Research question

When a target pair is chosen by a human participant, is it hit faster than
a target pair chosen by a verifiable random process, using the same live
source, the same alphabet, and the same selection rule?

## 2. Hypotheses and endpoint

- **H0:** $T_{\text{human}}$ and $T_{\text{machine}}$ have the same
  distribution.
- **H2:** $T_{\text{human}}$ is stochastically smaller than
  $T_{\text{machine}}$.

**Primary endpoint.** For each matched pair of trials, record whether the
human-target trial is faster:

$$q = \Pr(T_{\text{human}} < T_{\text{machine}}).$$

H0: $q=0.5$. H2: $q>0.5$. The primary analysis is a one-sided exact sign
test at $\alpha=0.05$.

## 3. Design

| Element | Specification |
|---|---|
| Source | Live quantum random number generator (certified device or auditable public quantum randomness service) |
| Alphabet | $\{-20,\ldots,20\}$, $m=41$; target probability $p=1/1681$ for a uniform source |
| Selection rule | The rule in [`../src/python/crlab/experiment.py`](../src/python/crlab/experiment.py), fixed before data collection |
| Human arm | Participant chooses $(c,d)$ before the trial, without seeing source output |
| Machine arm | Target drawn from a pre-committed list produced by a verifiable public randomness beacon, independent of the experimental source |
| Matching | One human-target trial and one machine-target trial per pair; order randomized in blocks of two |
| Blinding | The analyst does not receive arm labels until the dataset and analysis script are frozen |
| Trials | 5,000 matched pairs (10,000 trials), fixed sample |

### Why target choice, not per-draw selection

The original rule updates an auxiliary pair that is never read by the
stopping predicate. Asking a human to press "keep" on every draw therefore
cannot change $T$ through the program; only an anomalous correlation
between the human's mental state and the live source could show up. The
target choice is the scalable way to encode the participant's intention in
the original paradigm. A per-draw human-selection arm is included as an
**exploratory** condition in section 9.

## 4. Source requirements

1. The source must be physical and live during the trial. A prerecorded
   file is not acceptable for the confirmatory experiment: it cannot react
   to the observer.
2. The source must be independent of the participant, the operator, and the
   analyst.
3. Run a health check before and after each session (NIST SP 800-90B,
   dieharder, or the manufacturer's certified test suite). Log the results.
4. Log either every raw value or a cryptographic commitment to the raw
   stream. Publish the commitment before unblinding.
5. Document the source model, firmware version, sampling rate, and failure
   modes.

## 5. Sample size and stopping

The sign-test calculation in [`MATH.md`](MATH.md) gives:

- $q=0.52$: $N\approx4{,}900$ pairs for 80% power at two-sided
  $\alpha=0.05$ (a conservative calculation for the one-sided primary test).
- $q=0.51$: $N\approx19{,}600$ pairs.

The protocol fixes the smallest effect of interest at $q=0.52$ and
$N=5{,}000$ pairs. Two interim analyses are planned at 50% and 75% of the
information, with O'Brien-Fleming boundaries and a prespecified
alpha-spending function. The final analysis uses the remaining alpha.
Do not stop for efficacy at a nominal p-value without the boundary.

If the observed $q$ lies between 0.50 and 0.52, the result is
**inconclusive**, not evidence for H2. Report it as inconclusive.

## 6. Procedure

1. Preregister this document (OSF, GitHub release, or another timestamped
   registry) and record its SHA-256 hash.
2. Generate the machine-target list with a public randomness beacon. Commit
   to the list before data collection.
3. Prepare the source; run the health checks; record the source metadata.
4. For each matched pair:
   1. Randomize the order of the two arms.
   2. Human arm: the participant writes down $(c,d)$ and the timestamp;
      the target is sealed until after the trial.
   3. Machine arm: reveal the next committed target.
   4. Run the trial: draw pairs until the target appears, applying the
      fixed selection rule; log every draw or its commitment.
   5. Record $T$, the target, the arm, the timestamp, and any deviation.
5. After the last trial: freeze the dataset, compute its hash, publish the
   hash, and only then unblind the analyst.
6. Analyze according to section 7. Publish the analysis script and the
   frozen dataset.

## 7. Analysis plan

**Primary.** One-sided exact sign test for $q>0.5$. Report $q$, a 95%
confidence interval (Wilson), the exact p-value, and the number of
discordant pairs.

**Secondary.**

- Difference in mean $\log T$ (paired), with a bootstrap confidence
  interval.
- Mixed-effects logistic regression with participant as a random intercept
  (if multiple participants).
- Kolmogorov–Smirnov test of the two hitting-time distributions.
- Bayes factor for H2 versus H0 with a half-normal prior on the effect
  size, reported as a sensitivity analysis.

**Multiplicity.** Holm-Bonferroni across secondary endpoints. The primary
endpoint is the only confirmatory test.

**Effect size.** Report $q-0.5$, the risk ratio, and the absolute
difference in median $T$.

**Exclusions.** Predefine them: source failure, corrupted log, withdrawal
of consent. Report all exclusions and all deviations. Do not exclude trials
because the result looks inconvenient.

## 8. Data and code

- Raw data: CSV or Parquet, one row per trial, no personal data.
- Logs: source health, timestamps, hashes.
- Code: the release tag of this repository; the analysis script is frozen
  before unblinding.
- Open data unless ethics or privacy require an embargo.

## 9. Exploratory arm (optional)

A per-draw human-selection condition can be run on a smaller alphabet
(e.g., $m=11$, $\mathbb{E}T=121$) to test whether the act of selecting,
rather than the choice of target, correlates with the source. This arm is
exploratory: it is slower per trial, harder to blind, and not powered for
the confirmatory endpoint. Report it separately and do not pool it with the
primary analysis.

## 10. Ethics

- Human participants: informed consent, no deception, right to withdraw.
- If the study is human-subjects research, obtain IRB/ethics approval
  before data collection.
- Do not make medical or clinical claims.
- Do not recruit participants who expect a therapeutic benefit.

## 11. Limitations

- A single laboratory and a single source cannot establish a general
  effect.
- The result may depend on the participant, the source, or the setting.
- A null result rules out effects above the smallest effect of interest,
  not all effects.
- The protocol tests one operationalization of "intention". Other
  operationalizations need their own preregistration.

## 12. Amendments

Any change after preregistration is an amendment with a date, a reason, and
a hash of the new version. The original document remains public. Report
amendments in the final paper.
