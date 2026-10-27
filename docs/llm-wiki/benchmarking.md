# Benchmarking method

How we time and compare algorithms, so that results are fair, repeatable and say what the report
claims. Python-specific details (timers, warm-up, plotting) are added with the first experiment,
once they've been tried on our code. Every experiment follows this; reviewers check it ([REVIEWING.md](../../REVIEWING.md),
step 6).

## Inputs

- **Seeded generators.** Every random input comes from a generator called with an explicit seed,
  recorded in the result. Same seed, same input, on every machine.
- **Generate outside the timed region.** Build the input first, then start the clock.
- **Sizes span orders of magnitude.** Use a geometric series (n = 1k, 2k, 4k, ... or 10³ to 10⁶),
  not 100, 200, 300. Growth rates only show across a wide range.
- **Several input shapes where the analysis says they matter:** sparse vs dense graphs, sorted vs
  random, small vs large alphabets. Best, worst and typical cases if they differ.
- **Same input for every algorithm being compared** at a given size and seed.

## Timing

- **Repeat and take the median.** At least 5 repetitions per size and seed (more for fast runs);
  report the median, and the spread (min/max or IQR) where it's wide.
- **A run should last long enough to measure.** Below about a millisecond, timer resolution and
  noise dominate: time a batch of runs and divide.
- **Warm up first** where the language has a JIT or caches (Java, and to a lesser degree Python).
- **One machine per comparison**, plugged in, with nothing heavy running. Never compare timings
  taken on different machines.
- **Count operations too.** Comparisons, relaxations, heap operations, augmenting paths. Counts
  don't depend on the machine and match the analysis directly; time shows the constant factors.

## Checking a growth rate

- **Plot on log-log axes.** A running time of c·n^k is a straight line of slope k. Fit the slope
  over the larger sizes and compare it with the analysis.
- **Divide by the predicted bound.** Plot time / (n log n), or whatever the analysis predicts. If
  the analysis is right, the curve flattens to a constant.
- **Look for the crossover** where two algorithms' analyses predict different winners, and check
  that it moves the way the analysis says when the input shape changes.

## Recording

Every run writes a CSV to `results/` with one row per (algorithm, size, seed, repetition), and the
plot is made from that CSV by the same command. The entry in [findings.md](findings.md) records the
command, commit, machine and inputs.

## Pitfalls we've hit

*None yet. Add them here as they happen, with the date.*
