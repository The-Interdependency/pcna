# PCNA Repo
Initialized Sat Jan 31 19:00:28 PST 2026
Below is a single-file, copypastable README.md for your PCNA repository, written clean, technical, and grounded — aligned with your preference for structure first, then content and ready for GitHub.


---

Prime Circular Neural Architecture (PCNA)

Deterministic, prime-indexed, circular graph architecture for modular compute + diagnostics.

GPT generated; context, prompt Erin Spencer


---

I. Purpose

PCNA is an experimental neural / distributed-compute topology that:

organizes compute nodes on a unit-circle address space

routes traffic through prime-indexed clusters

separates computation from diagnostics

embeds observability directly into the architecture


Design goal:

> predictable routing, sparse communication, measurable stability



PCNA avoids opaque dense attention or monolithic networks in favor of:

explicit structure

bounded neighborhoods

inspectable flows

failure visibility



---

II. Core Ideas (Plain English)

Instead of:

> one giant black-box neural net



PCNA uses:

many small nodes

clustered routing

meta routers

independent sentinels watching the system


So:

compute happens here
analysis happens there
feedback closes the loop

This enables:

modular growth

easier debugging

resilience to failure

compatibility with EDCM diagnostics



---

III. Topology

Node counts

Layer	Count	Role

child routers	49	primary compute
meta routers	7	cluster aggregation
sentinels	4	diagnostics / metadata
global router	1	coordination root
total seeds	53	prime-indexed set


53 is chosen because:

prime → avoids harmonic aliasing

clean cluster separation

symmetric layout for circular addressing



---

Layout

(sentinels)
                   ○ ○
            ○                   ○

        [ 7 clusters × 7 nodes each ]

             → meta routers (7)
                    ↓
               global zero


---

IV. Functional Layers

1. Child Routers (49)

Primary compute units.

Responsibilities:

token transforms

state updates

local tensor math

Markov recursion

learning steps


Properties:

small

independent

replaceable



---

2. Meta Routers (7)

Cluster coordinators.

Responsibilities:

aggregate child outputs

route inter-cluster traffic

reduce bandwidth

maintain locality



---

3. Global Router (0)

System spine.

Responsibilities:

high-level coordination

broadcast

synchronization

scheduling



---

4. Sentinels (4)

Diagnostics only — not compute.

Responsibilities:

anomaly detection

stability metrics

constraint strain (EDCM)

outlier detection

metadata analysis


Key rule:

> Sentinels observe but do not influence compute directly.



They produce:

signals

flags

feedback


Never hidden mutation.


---

V. Data Flow

Forward pass

input
  → children
  → meta routers
  → global router
  → output

Diagnostic loop

all states
  → sentinels
  → metrics
  → health signals
  → optional corrective policies

Separation of concerns:

Path	Purpose

compute	results
sentinel	measurement



---

VI. Why This Exists

Problems with typical deep nets

opaque

fragile

hard to debug

expensive global attention

poor observability


PCNA aims to provide

deterministic routing

sparse communication

explicit locality

inspectability

modular scaling

native diagnostics



---

VII. Relationship to EDCM

PCNA and EDCM are complementary:

System	Role

PCNA	compute substrate
EDCM	dissonance / stability metrics


Conceptually:

PCNA thinks
EDCM measures strain of thinking

This allows:

early instability detection

alignment checks

human-readable diagnostics



---

VIII. Minimal Folder Structure

pcna/
│
├─ core/
│   ├─ node.py
│   ├─ router.py
│   ├─ cluster.py
│   ├─ sentinel.py
│   └─ topology.py
│
├─ metrics/
│   ├─ edcm_adapter.py
│   └─ health_metrics.py
│
├─ sims/
│   ├─ toy_markov.py
│   └─ stress_tests.py
│
├─ viz/
│   ├─ circular_layout.py
│   └─ cylinder_unwrap.py
│
├─ docs/
│   └─ architecture.md
│
└─ README.md


---

IX. Minimal Prototype (concept sketch)

class ChildNode:
    def step(self, x):
        return transform(x)


class MetaRouter:
    def __init__(self, children):
        self.children = children

    def route(self, x):
        return sum(c.step(x) for c in self.children)


class Sentinel:
    def inspect(self, states):
        return anomaly_score(states)


---

X. Design Principles

small pieces > giant monoliths

explicit > implicit

inspectable > mystical

deterministic > emergent chaos

diagnostics first-class



---

XI. Status

Early research / experimental.

Not production hardened.

Iteration expected.

Refinement will continue.


---

XII. Attribution

GPT generated; context, prompt Erin Spencer


---

XIII. License

MIT recommended
(simple, permissive, encourages adoption and collaboration)


---

XIV. hmm

Open constraints / active questions:

is 4 sentinel coverage optimal vs 5 or 7?

best routing strategy: deterministic vs adaptive?

ideal cluster size beyond 7?

sentinel → compute feedback latency tradeoffs


(hmm retained intentionally as unresolved design space)


---

If you'd like next, I can:

generate architecture.md

write topology.py

build a runnable Python demo

or produce SVG visualizers for the circle/cylinder unwrap


Structure or code next?
