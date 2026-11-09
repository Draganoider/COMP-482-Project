# The problem, layer 1

Notation follows Kleinberg and Tardos, chapter 7.

## 1. Input

1. A directed graph *G* = (*V*, *E*). Nodes are intersections. Each edge *e* = (*u*, *v*) is one
   direction of one road, so a two-way road is two edges. Parallel edges are allowed; self-loops
   are not.
2. A whole-number capacity *c*<sub>*e*</sub> ≥ 0 for each edge, in cars per hour.
3. A set *H* ⊆ *V* of homes and a set *S* ⊆ *V* of shelters (where roads leave the area), with
   *H* ∩ *S* = ∅.

Let *C* = Σ<sub>*e* ∈ *E*</sub> *c*<sub>*e*</sub>, the total road capacity.

## 2. The flow network

Add a super-source *s* and a super-sink *t*, an edge (*s*, *h*) for each home *h*, and an edge
(*x*, *t*) for each shelter *x*. These terminal edges have capacity *C* + 1. If a road's capacity
changes, they are reset to the new *C* + 1.

Below, *V* and *E* mean the sizes of this network: |*V*| + 2 nodes and |*E*| + |*H*| + |*S*| edges.

## 3. Flows and cuts

A **flow** is a function *f* : *E* → ℤ with:

1. **Capacity:** 0 ≤ *f*(*e*) ≤ *c*<sub>*e*</sub> for every edge.
2. **Conservation:** *f*<sup>in</sup>(*v*) = *f*<sup>out</sup>(*v*) for every node except *s* and *t*.

Its **value** is *ν*(*f*) = *f*<sup>out</sup>(*s*).

A **cut** is a partition (*A*, *B*) of the nodes with *s* ∈ *A* and *t* ∈ *B*. Its **capacity**
*c*(*A*, *B*) is the sum of *c*<sub>*e*</sub> over edges from *A* to *B*. Its **cut roads** are the
roads among those edges.

## 4. Output

1. A maximum flow *f*\* and its value *ν*(*f*\*).
2. A minimum cut (*A*\*, *B*\*).
3. The bottleneck roads: the cut roads of (*A*\*, *B*\*).

The answer is **correct** when *f*\* is a flow, (*A*\*, *B*\*) is a cut, and
*ν*(*f*\*) = *c*(*A*\*, *B*\*). Since every flow is at most every cut, equality means both are
optimal. Several maximum flows and minimum cuts may exist; any one is correct.

## 5. Terminal edges are never in a minimum cut

The cut *A* = {*s*} ∪ *H* has only roads leaving it (because *H* ∩ *S* = ∅), so its capacity is
at most *C*. A cut with a terminal edge leaving *A* has capacity at least *C* + 1, so it is not
minimum. ∎

## 6. Brute-force checker

**Input:** the network, *s*, *t*
**Output:** the capacity of a minimum cut

```
1  best ← ∞
2  for each subset X of V − {s, t}:
3      A ← {s} ∪ X
4      cap ← sum of c_e over edges e = (u, v) with u ∈ A and v ∉ A
5      best ← min(best, cap)
6  return best
```

Line 2 runs 2<sup>*V* − 2</sup> times and line 4 takes O(*E*), so this is O(2<sup>*V*</sup> · *E*).

## 7. What-ifs

A road is one edge *e* ∈ *E* (one direction), never a terminal edge. Let *ν*\*(*G*) be the
maximum flow value.

- **Closure:** set *c*<sub>*e*</sub> to 0. loss(*e*) = *ν*\*(*G*) − *ν*\*(*G* − *e*).
- **Widening:** add *δ* > 0, one lane's capacity, to *c*<sub>*e*</sub>.
  gain(*e*) = *ν*\*(*G* + *δe*) − *ν*\*(*G*).

Report loss for every road, largest first, and the road with the largest gain. Ties are reported
as ties.

## 8. Example

Roads: *a*→*b* 3, *a*→*c* 2, *b*→*c* 1, *b*→*d* 2, *c*→*d* 3. Homes {*a*}, shelters {*d*}.

- Maximum flow 5: 2 on *a*→*b*→*d*, 2 on *a*→*c*→*d*, 1 on *a*→*b*→*c*→*d*.
- Three minimum cuts of capacity 5: *A* = {*s*, *a*}, {*s*, *a*, *b*}, and {*s*, *a*, *b*, *c*}.

## 9. Limitations

- A rate in cars per hour, not evacuation time.
- Intersections have unlimited capacity (no signals or turns).
- Assumes every driver follows the plan, so it is an upper bound.
- Capacities are estimates from lanes and road type.
- Shelters accept any number of cars; residents without cars are not modelled.