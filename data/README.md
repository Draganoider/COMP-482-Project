# Data

The inputs: the road network, the shelters and the households. Owner: the Experiments Lead.

| Data | Source | How we get it | Where |
|---|---|---|---|
| Pacific Palisades road network, with lanes and road types | OpenStreetMap, through OSMnx | A download script, added with the data issue | `data/raw/` (gitignored), with a small processed copy committed if it's under 2 MB |
| Road capacity per lane | Highway Capacity Manual figures, to confirm | Written down with its source | `docs/references.md` |
| Shelters | To decide: real shelter sites or the network's exits | | |
| Households per area | US Census blocks | | |
| Synthetic networks for scaling | Our own seeded generator | In `src/evac/` | Generated, never stored |

Every source gets a line in [docs/references.md](../docs/references.md), with its licence, in the
same pull request that brings it in. OpenStreetMap data is © OpenStreetMap contributors, under the
ODbL, which requires that credit.
