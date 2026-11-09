# Min cut and the what-ifs

Notation from `problem.md`. The theorem and the residual-graph cut are Kleinberg and Tardos §7.2.

## 1. Every flow is at most every cut

**Claim.** For any flow *f* and any cut (*A*, *B*), *ν*(*f*) ≤ *c*(*A*, *B*).

**Proof.** Add up conservation over the nodes of *A*. Every node except *s* has net flow 0, so
*ν*(*f*) equals the flow on edges leaving *A* minus the flow on edges entering *A*. The first part is
at most *c*(*A*, *B*), and the second is at least 0. ∎

## 2. Max-flow min-cut theorem

**Claim.** The value of a maximum flow equals the capacity of a minimum cut.

**Proof.** When MaxFlow (`max-flow.md`) stops, let *A* be the nodes reachable from *s* in
*G*<sub>*f*</sub>. Then *t* ∉ *A*, every road from *A* to *B* is full, and every road from *B* to
*A* carries 0, so in the sum of §1, *ν*(*f*) = *c*(*A*, *B*). By §1 no flow is larger and no cut is
smaller. ∎

## 3. Finding the cut

**MinCut**
**Input:** the residual graph *G*<sub>*f*</sub> of a maximum flow, and *s*
**Output:** the set *A* and the bottleneck roads

```
1  mark s; Q.enqueue(s)
2  while Q is not empty:
3      u ← Q.dequeue()
4      for each residual edge e = (u, v) leaving u:
5          if r(e) > 0 and v is not marked:
6              mark v; Q.enqueue(v)
7  A ← the marked nodes
8  return A and every road (u, v) with u ∈ A, v ∉ A
```

**Correct** by §2: *A* is the set in that proof, so (*A*, *B*) is a minimum cut.

**Running time O(*V* + *E*).** Each node is enqueued once and each residual edge scanned once
(lines 1–6), and line 8 checks each road once.

**No terminal edge is returned.** (*A*, *B*) is a minimum cut, and `problem.md` §5 shows no minimum
cut has a terminal edge leaving *A*.

## 4. The what-ifs

Write *ν*\* for the maximum flow value. Since *ν*\* is the smallest cut capacity (§2), every what-if
can be read off how it changes the cuts.

**Fact 1. 0 ≤ loss(*e*) ≤ *c*<sub>*e*</sub> and 0 ≤ gain(*e*) ≤ *δ*.** Closing *e* lowers each
cut's capacity by *c*<sub>*e*</sub> or by 0, so the smallest cut drops by between 0 and
*c*<sub>*e*</sub>. Widening raises each cut by *δ* or by 0, the same way. ∎

**Fact 2 (H2, first half). If *e* is a cut road of some minimum cut and *c*<sub>*e*</sub> > 0,
closing *e* lowers the max flow.** That cut's capacity drops to *ν*\* − *c*<sub>*e*</sub> < *ν*\*,
and the max flow is at most it. ∎

**Fact 3 (H2, second half). A road on no minimum cut can lower the max flow too.** Counterexample:
home *h*, shelter *x*, roads *h*→*u* 5, *u*→*x* 10, *h*→*w* 5, *w*→*x* 10.

- The max flow is 10. The only minimum cut is {*h*→*u*, *h*→*w*}; the others cost 15 or 20.
- Close *u*→*x*, which is on no minimum cut. The cut {*h*→*w*, *u*→*x*} now costs 5 + 0, so the max
  flow drops to 5.

Closing a road can make a cut that wasn't minimum into a new, smaller one. So the min cut alone can't
rank closures, and every road is re-solved (E2).

**Fact 4. If some maximum flow puts 0 on *e*, closing *e* loses nothing.** That flow is still valid
without *e*. If the code uses this to skip roads, the report says so (AGENTS.md hard rule 3).

**Fact 5 (H3). Widening *e* raises the max flow exactly when *e* is a cut road of every minimum
cut.** Widening only changes cuts that contain *e*.

- If some minimum cut doesn't contain *e*, it still costs *ν*\*, so the max flow stays *ν*\*.
- If every minimum cut contains *e*, each rises to *ν*\* + *δ*. Every other cut already cost at
  least *ν*\* + 1, since capacities are whole numbers. So the smallest cut, and the max flow, rise
  by at least 1. ∎

Counterexample for "widen a min-cut road": home *h*, shelter *x*, roads *h*→*u* 5, *u*→*x* 5. Both
roads are minimum cuts on their own. Widening *h*→*u* leaves *u*→*x* at 5, so the gain is 0. The
example in `problem.md` §8 shows the same with three minimum cuts and no road in all of them (E3).

## 5. Running time of the what-ifs

One what-if per road means |*E*| max-flow runs, plus O(*E*) to copy the network each time.

| Solver | One run | All closures (or all widenings) |
|---|---|---|
| Edmonds-Karp | O(*VE*²) | O(*VE*³) |
| Ford-Fulkerson | O(*E* · *f*\*) | O(*E*² · *f*\*) |

Brute force is not an option on the real map. A network with *V* nodes has 2<sup>*V* − 2</sup> cuts,
so the checker in `problem.md` §6 takes O(2<sup>*V*</sup> · *E*), which doubles with every
intersection.
