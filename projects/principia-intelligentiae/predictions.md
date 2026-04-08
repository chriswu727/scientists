# Principia Intelligentiae — Theoretical Predictions
## Derived by Newton + Feynman + Dirac

### The Calculation

Starting from the candidate Lagrangian:

$$\mathcal{L} = \frac{1}{16\pi\kappa}(R[g(\theta)] - 2\Lambda)\sqrt{\det g} - \mathcal{L}_{\text{task}}(\theta,\phi)\sqrt{\det g}$$

For the hydrogen atom case (single hidden layer, h neurons, ReLU, C_4 symmetric 2D classification):

**Fisher metric** (leading order): g_ij ≈ (σ²_x / 2h) · δ_ij

**Ricci scalar**: R ≈ -h² / (16 · N · σ⁴_x) — negative curvature (hyperbolic), as expected for redundant parameterizations.

**Critical ratio** from field equation G_ij + Λg_ij = κ T_ij: Solving for the memorization→generalization transition:

**(N/P)* = 3h(3h - 2) / (8π · η · P)**

where η is the learning rate and P ≈ 3h is the parameter count.

**Effective rank** from C_4 representation theory: C_4 has 4 irreps (A, B, E+, E-). Parameters decompose into h/4 orbits of 4 neurons. The generalizing solution lives in the invariant subspace: **effective rank = 3h/4**.

**Phase transition order**: Landau-Ginzburg analysis shows a cubic invariant exists for C_4 → **first-order (sharp) transition**.

### Predictions Table

For **h = 64, P = 193, C_4 symmetry**:

| Quantity | Prediction | Formula |
|---|---|---|
| Fisher metric (leading order) | g_ij ≈ (σ²_x / 128) · δ_ij | σ²_x / (2h) |
| Ricci scalar | R ≈ -256 / (N · σ⁴_x) | -h² / (16Nσ⁴_x) |
| Critical ratio (N/P)* at η=0.01 | **~752** | 3h(3h-2) / (8πηP) |
| Critical ratio (N/P)* at η=1.0 | **~7.5** | same formula |
| Effective rank at convergence | **48** | 3h/4 |
| Phase transition order | **First-order (sharp)** | Cubic C_4 Landau invariant |
| Neuron orbit structure | 16 orbits of 4 neurons | h/4 |

### Key Testable Claim

The learning rate η enters as a cosmological constant Λ = 1/η. This means:
- Higher learning rate → lower critical data requirement (earlier generalization)
- This is a **specific, non-obvious prediction** that can be falsified
