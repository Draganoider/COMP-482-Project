# Proposal

2–3 pages, one PDF per team, submitted on Canvas by the Project Lead. **Submitted; due
2026-10-31.**

- **Submitted PDF:** [proposal.pdf](proposal.pdf), written in Google Docs
- **Skeleton:** [skeleton.md](skeleton.md), kept for the record

## Checklist

What the outline asks for, checked against what was submitted. The open items are for the final
report to settle.

- [x] **Title**
- [x] **Problem statement, precise:** section 2, made exact in plan decision D10. Still open: where
      the homes are and how many cars each sends (plan Q10).
- [x] **Algorithms, at least two:** Ford-Fulkerson in O(E·f\*) and Edmonds-Karp in O(VE²), and the
      min cut from the residual graph in O(V+E).
- [x] **The baseline to compare against:** brute force over every cut on small graphs, and
      NetworkX in the tests.
- [ ] **Data:** OpenStreetMap through OSMnx, capacities from the Highway Capacity Manual, and a
      seeded synthetic generator. Still open: the network's size (recorded once it's downloaded)
      and its licence (ODbL), which the proposal doesn't name.
- [ ] **Evaluation plan:** E1–E3, the measures (median time, augmenting paths, max-flow value) and
      a log-log plot. Still open: the input sizes.
- [x] **Roles:** section 8.
- [x] **Stretch goal**, marked as stretch: the fire (E4), the shortest-route comparison (E5) and
      the map app.
- [ ] **The language:** Python 3.11 or newer is named; why it suits the problem isn't said.
