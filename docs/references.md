# References

Every source we didn't write: the textbook, datasets, articles, and external code. The report's
references section is built from this page, so **add a line in the same pull request that brings
the source in** (AGENTS.md hard rule 6).

For code, say what was taken and where it lives in the repository. For a dataset, give the licence
and how to get it, so the download script and this page agree.

## Textbooks and course material

| Source | Used for |
|---|---|
| Kleinberg, J. and Tardos, É. *Algorithm Design*. Pearson | The course's main textbook: notation, proof forms |
| Cormen, T. H. et al. *Introduction to Algorithms*. MIT Press | The course's second textbook |

## Datasets

| Dataset | Source (URL) | Licence | Where it lives | Used by |
|---|---|---|---|---|
| OpenStreetMap road network of Pacific Palisades, Los Angeles | [openstreetmap.org](https://www.openstreetmap.org/), downloaded with OSMnx | [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/) | `data/raw/`, from a download script still to write | Layer 1 and the experiments; cited in the proposal |

## Articles and other sources

| Source | Used for |
|---|---|
| Borgwardt, S. et al. (2024). *Evacuation Planning on Time-Expanded Networks with Integrated Wildfire Information*. [arXiv:2410.14500](https://arxiv.org/abs/2410.14500) | Related work: wildfire evacuation as max flow on a time-expanded network (layer 2). Cited in the proposal |
| Transportation Research Board. *Highway Capacity Manual* | Road capacities in cars per hour from lanes and road type (plan D10). Cited in the proposal; the edition is still to note |
| Fox LA report on the cars abandoned during the January 2025 Palisades fire evacuation | The proposal's motivation. Cited in the proposal; the article's URL and date are still to add |

## External code and libraries

| Library or snippet | Version | Licence | Used for |
|---|---|---|---|
| [pytest](https://pytest.org/) | ≥ 8 | MIT | Running the test suite (development only) |
| [Ruff](https://docs.astral.sh/ruff/) | ≥ 0.6 | MIT | Style and lint checks (development only) |
| [NetworkX](https://networkx.org/) | ≥ 3.2 | BSD-3-Clause | Reference max flow in tests, to check our own implementations. Never used in `src/` |
