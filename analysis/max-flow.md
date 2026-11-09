# Max flow: Ford-Fulkerson and Edmonds-Karp

Notation from `problem.md`. Both algorithms are Kleinberg and Tardos §7.1; the Edmonds-Karp bound
is from Cormen et al. §26.2 (4th edition §24.2).

## 1. The residual graph

For a flow *f*, the residual graph *G*<sub>*f*</sub> has, for each road *e* = (*u*, *v*):

- a forward edge (*u*, *v*) with residual capacity *r*(*e*) = *c*<sub>*e*</sub> − *f*(*e*), and
- a backward edge (*v*, *u*) with residual capacity *f*(*e*), for undoing flow.

Only edges with residual capacity > 0 can be used. An **augmenting path** is a simple *s*–*t* path
in *G*<sub>*f*</sub> using only such edges.

## 2. Pseudocode

Both algorithms are the same loop; only the search differs.

**Augment**
**Input:** a flow *f* and an augmenting path *P*
**Output:** the amount *b* pushed

```
1  b ← min of r(e) over edges e in P
2  for each edge e in P:
3      r(e) ← r(e) − b
4      r(reverse of e) ← r(reverse of e) + b
5  return b
```

**FindPath**
**Input:** *G*<sub>*f*</sub>, *s*, *t*, and a container *D*: a stack for DFS, a queue for BFS
**Output:** an augmenting path, or none

```
1   mark s; parent(s) ← none; D.add(s)
2   while D is not empty:
3       u ← D.take()                       (stack: pop; queue: dequeue)
4       for each residual edge e = (u, v) leaving u:
5           scanned ← scanned + 1
6           if r(e) > 0 and v is not marked:
7               mark v; parent(v) ← e
8               if v = t: return the path found by following parent from t back to s
9               D.add(v)
10  return none
```

**MaxFlow**
**Input:** the network, *s*, *t*
**Output:** a maximum flow and its value

```
1  set f(e) ← 0 for every edge (r(e) ← c_e, r(reverse of e) ← 0)
2  paths ← 0
3  loop:
4      P ← FindPath(G_f, s, t)
5      if P is none: return f and ν(f)
6      Augment(f, P)
7      paths ← paths + 1
```

**Ford-Fulkerson** is MaxFlow with a stack in FindPath (DFS). **Edmonds-Karp** is MaxFlow with a
queue (BFS), so each path it finds is a shortest one in edges.

**Counters for E1:** `paths` counts augmentations, and `scanned` counts residual edges examined.
These are the two quantities the bounds below count.

## 3. Correctness

**Claim 1. After Augment, *f* is still a flow.** Line 1 picks *b* ≤ every residual capacity on
*P*, so no forward edge goes above *c*<sub>*e*</sub> and no backward edge takes back more flow than
exists: the capacity condition holds. At each inner node of *P*, one edge of the path enters and one
leaves, and each changes that node's net flow by *b* in opposite directions, so conservation holds.
(Kleinberg and Tardos §7.1.)

**Claim 2. Each augmentation raises *ν*(*f*) by *b* ≥ 1.** No road enters *s*, so the first edge of *P*
is a forward road out of *s*, and a simple path never returns to *s*. So the flow out of *s*
rises by *b*. Capacities are whole
numbers, so all residual capacities stay whole numbers and *b* ≥ 1.

**Claim 3. Both algorithms stop.** The value is at most *f*\* = *ν*(*f*\*) and rises by at least 1
per augmentation (Claim 2), so there are at most *f*\* augmentations.

**Claim 4. When FindPath returns none, *f* is maximum.** Let *A* be the nodes reachable from *s* in
*G*<sub>*f*</sub>. Then *t* ∉ *A*, so (*A*, *B*) is a cut. Every road from *A* to *B* is full (else
its head would be reachable), and every road from *B* to *A* carries 0 (else its backward edge would
make its tail reachable). So *ν*(*f*) = *c*(*A*, *B*), and by `problem.md` §4 the flow is maximum.
(Kleinberg and Tardos §7.2; the full argument is in `min-cut.md`.)

## 4. Running time

**One search.** Each node enters *D* at most once, and each residual edge is scanned at most once
when its tail is taken out, so FindPath and Augment take O(*E*): the search only reaches nodes it
entered by an edge.

**Ford-Fulkerson: O(*E* · *f*\*).** At most *f*\* augmentations (Claim 3), each O(*E*). We use *f*\*
rather than Kleinberg and Tardos's *C* (the capacity out of *s*), because our terminal edges make
that number huge. *f*\* ≤ *C*, the total road capacity (`problem.md` §5).

**Edmonds-Karp: O(*VE*²).** At most O(*VE*) augmentations, each O(*E*). The augmentation bound
follows from two lemmas. Let *d*<sub>*f*</sub>(*v*) be the fewest edges on a path from *s* to *v* in
*G*<sub>*f*</sub>.

**Lemma 1. *d*<sub>*f*</sub>(*v*) never decreases.** Suppose an augmentation turns *f* into *f*′
and some distances drop. Among the nodes whose distance dropped, take *v* with the smallest
*d*<sub>*f*′</sub>(*v*), and let *u* be the node before *v* on a shortest path in
*G*<sub>*f*′</sub>. Then *d*<sub>*f*′</sub>(*v*) = *d*<sub>*f*′</sub>(*u*) + 1, and *u*'s distance
didn't drop, so *d*<sub>*f*</sub>(*u*) ≤ *d*<sub>*f*′</sub>(*u*).

- If (*u*, *v*) was in *G*<sub>*f*</sub>, then *d*<sub>*f*</sub>(*v*) ≤ *d*<sub>*f*</sub>(*u*) + 1
  ≤ *d*<sub>*f*′</sub>(*v*), so *v*'s distance didn't drop. Contradiction.
- If it wasn't, the augmentation created it, so it pushed flow along (*v*, *u*). Edmonds-Karp
  augments along a shortest path, so *d*<sub>*f*</sub>(*v*) = *d*<sub>*f*</sub>(*u*) − 1
  ≤ *d*<sub>*f*′</sub>(*u*) − 1 = *d*<sub>*f*′</sub>(*v*) − 2. Again *v*'s distance didn't drop.
  Contradiction. ∎

**Lemma 2. Each residual edge is critical at most *V*/2 times.** An edge (*u*, *v*) is *critical*
on *P* if its residual capacity equals *b*; it then leaves the residual graph. When that happens,
*d*<sub>*f*</sub>(*v*) = *d*<sub>*f*</sub>(*u*) + 1. It can only return after a later augmentation,
at flow *f*″, pushes along (*v*, *u*), and then *d*<sub>*f*″</sub>(*u*) = *d*<sub>*f*″</sub>(*v*) + 1
≥ *d*<sub>*f*</sub>(*v*) + 1 = *d*<sub>*f*</sub>(*u*) + 2 by Lemma 1. So *u*'s distance grows by at
least 2 between two times the edge is critical. It starts at ≥ 0 and is at most *V* − 2 while *u* is
reachable, so this happens at most *V*/2 times. ∎

Every augmentation has at least one critical edge, and there are 2*E* residual edges, so there are
at most 2*E* · *V*/2 = *VE* augmentations.

**Which wins?** Ford-Fulkerson's bound grows with the flow value, Edmonds-Karp's does not. When
*f*\* is small compared with *VE*, Ford-Fulkerson can be faster. Experiment E1 tests both bounds
with the two counters.
