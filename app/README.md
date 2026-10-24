# App

Layer 3, the presentation: a map where you start a fire and watch the evacuation plan play out.
**Built last, and cut first if time runs short** (plan D7). It only displays what the Python code in
`src/evac/` computes, so the report's analysis describes everything the demo shows.

Planned stack, decided in detail when layer 3 starts: FastAPI serving results from `src/evac/`,
MapLibre for the map, deck.gl's TripsLayer for the moving cars. Nothing here yet.
