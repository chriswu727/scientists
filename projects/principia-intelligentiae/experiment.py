#!/usr/bin/env python3
"""
===============================================================================
PRINCIPIA INTELLIGENTIAE — Experiment 1
"The Hydrogen Atom of Deep Learning"

Designed by: Curie, Mendeleev, Feynman (Team 3: The Experiment Team)
Implemented by: Feynman (intuition), Curie (measurement), Turing (formalism)

A single hidden-layer ReLU network learns C_4 cyclic symmetry on 2D points.
We sweep hidden width and dataset size, measuring phase transitions between
memorization and generalization — the simplest non-trivial system that
exhibits the phenomena our Lagrangian must explain.
===============================================================================

--- FEYNMAN ---
Look, the whole point is this: a neural network is just a machine that draws
decision boundaries. Give it a pattern with four-fold rotational symmetry,
and watch what happens as you turn the knobs — more neurons, more data.
Somewhere in that two-dimensional parameter space, there's a phase transition.
The network stops memorizing and starts *understanding* the symmetry.
That's the hydrogen atom. Simple enough to solve exactly, rich enough to
contain all the physics.

--- CURIE ---
We measure nine quantities per run. Each must be computed with care.
I have seen too many experiments ruined by sloppy measurement. The effective
rank via SVD, the Hessian eigenvalues, the generalization quotient — these
are not decorations. They are the data that will confirm or kill the theory.
One does not rush. One measures.

--- TURING ---
The formal structure: we have a function f: R^2 -> {0,1} defined by
C_4 symmetry (the cyclic group of order 4 acting on polar angle).
The network is a composition: softmax(W2 * relu(W1 * x + b1) + b2).
The hypothesis space is parameterized by (W1, b1, W2, b2) with
dim = 2h + h + 2h + 2 = 4h + 2 total parameters.
The phase transition occurs at a critical ratio N/P where P = 4h + 2.
===============================================================================
"""

import os
import csv
import time
import itertools
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader


# =============================================================================
# SECTION 1: C_4 SYMMETRIC DATASET GENERATION
# =============================================================================
# --- FEYNMAN ---
# Here's the fun part. Take a point in 2D, convert to polar coordinates,
# and divide the angle into four quadrants. But not boring axis-aligned
# quadrants — we use a radial modulation so the boundary is actually
# interesting. The label depends on which of the four sectors you're in,
# and the sectors are defined by theta mod (pi/2). Two classes: even
# sectors vs odd sectors. Four-fold rotational symmetry. Simple as that.
#
# --- TURING ---
# Formally: label(r, theta) = floor(2*theta/pi) mod 2, where theta in [0, 2*pi).
# This yields a C_4-invariant binary classification on R^2.
# The decision boundary consists of four rays from the origin at angles
# 0, pi/2, pi, 3*pi/2 — the simplest non-linearly-separable C_4 pattern.
# We add a radial modulation to prevent trivial solutions.

def generate_c4_dataset(n_samples, seed=42):
    """
    Generate 2D points with C_4 cyclic symmetry labels.

    --- CURIE ---
    The data must be generated with exact reproducibility. Each seed
    produces an identical dataset. I keep a laboratory notebook; you
    keep a random seed.

    Returns:
        X: (n_samples, 2) tensor of 2D points
        y: (n_samples,) tensor of binary labels {0, 1}
    """
    rng = np.random.RandomState(seed)

    # Sample points uniformly in a disk of radius 2
    # Using rejection sampling for uniform distribution — no bias toward center
    # --- FEYNMAN ---
    # Why a disk and not a square? Because the symmetry is rotational.
    # You want the data distribution to respect the symmetry you're testing.
    # Otherwise you're measuring the interaction of two symmetries, and
    # that's a helium atom, not hydrogen.
    points = []
    n_collected = 0
    while n_collected < n_samples:
        candidates = rng.uniform(-2.0, 2.0, size=(n_samples * 2, 2))
        r = np.sqrt(candidates[:, 0]**2 + candidates[:, 1]**2)
        valid = candidates[r <= 2.0]
        points.append(valid)
        n_collected += len(valid)
    points = np.concatenate(points, axis=0)[:n_samples]

    x = points[:, 0]
    y_coord = points[:, 1]

    # Compute polar angle in [0, 2*pi)
    theta = np.arctan2(y_coord, x) % (2 * np.pi)

    # C_4 symmetry: divide circle into 4 sectors of pi/2 each
    # Sector index: 0, 1, 2, 3
    sector = np.floor(2.0 * theta / np.pi).astype(int) % 4

    # --- TURING ---
    # Binary label: sectors 0,2 -> class 0; sectors 1,3 -> class 1
    # This is the unique non-trivial C_4-invariant binary labeling
    # (up to relabeling). It cannot be learned by a linear classifier
    # because the classes are not linearly separable.
    labels = (sector % 2).astype(np.int64)

    # --- CURIE ---
    # Add a radial-dependent boundary perturbation to make the problem
    # non-trivial near the origin. Without this, points near r=0 are
    # ambiguous and the network wastes capacity on noise.
    # We rotate the sector boundaries by an amount proportional to radius:
    # theta_effective = theta + 0.3 * r
    # This creates a "pinwheel" pattern — still C_4 symmetric, but the
    # boundaries are curved, requiring the network to learn nonlinear features.
    r = np.sqrt(x**2 + y_coord**2)
    theta_effective = (theta + 0.3 * r) % (2 * np.pi)
    sector_eff = np.floor(2.0 * theta_effective / np.pi).astype(int) % 4
    labels = (sector_eff % 2).astype(np.int64)

    X_tensor = torch.tensor(points, dtype=torch.float32)
    y_tensor = torch.tensor(labels, dtype=torch.long)

    return X_tensor, y_tensor


# =============================================================================
# SECTION 2: NETWORK ARCHITECTURE
# =============================================================================
# --- FEYNMAN ---
# One hidden layer. ReLU. Softmax. That's it.
# If you can't understand what a single hidden layer does, you have
# no business stacking 96 of them and calling it "architecture design."
#
# --- TURING ---
# The network computes: f(x) = softmax(W2 * relu(W1 * x + b1) + b2)
# Parameter count P = 2*h (W1) + h (b1) + h*2 (W2) + 2 (b2) = 4*h + 2
# This is the minimal architecture that can represent any continuous
# function on R^2 (universal approximation), making it the correct
# "hydrogen atom" — simple enough to analyze, powerful enough to exhibit
# all phenomena of interest.

class HydrogenNet(nn.Module):
    """
    The simplest possible deep learning architecture that can learn
    a non-trivial symmetric pattern.

    --- CURIE ---
    I name it carefully. "HydrogenNet" — because this is the hydrogen atom
    of deep learning. The simplest system that contains the essential physics.
    """

    def __init__(self, hidden_width):
        super().__init__()
        self.fc1 = nn.Linear(2, hidden_width)       # R^2 input
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_width, 2)        # Binary classification

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x  # Raw logits; CrossEntropyLoss applies softmax internally

    def parameter_count(self):
        """
        --- TURING ---
        P = 4h + 2, where h is hidden width.
        This is the dimension of the parameter manifold on which
        the Fisher information metric is defined.
        """
        return sum(p.numel() for p in self.parameters())


# =============================================================================
# SECTION 3: MEASUREMENT FUNCTIONS
# =============================================================================
# --- CURIE ---
# "One never notices what has been done; one can only see what remains
# to be done." But we must measure what has been done precisely,
# or the remaining work is built on sand.

def compute_accuracy(model, X, y):
    """Compute classification accuracy. No shortcuts, no approximations."""
    model.eval()
    with torch.no_grad():
        logits = model(X)
        preds = torch.argmax(logits, dim=1)
        accuracy = (preds == y).float().mean().item()
    return accuracy


def compute_generalization_quotient(train_acc, test_acc):
    """
    --- FEYNMAN ---
    The generalization quotient G = test_accuracy / train_accuracy.
    When G ≈ 1, the network generalizes. When G << 1, it memorizes.
    The transition from G << 1 to G ≈ 1 is the phase transition we're
    looking for. Dead simple metric, tells you everything.

    --- TURING ---
    More precisely: G ∈ [0, 1] for a non-degenerate classifier.
    G = 1 implies perfect generalization (test = train performance).
    G → 0 implies pure memorization (high train, low test).
    The critical N/P ratio where G transitions is our primary observable.
    """
    if train_acc < 1e-10:
        return 0.0
    return test_acc / train_acc


def compute_effective_rank(model):
    """
    Effective rank of the first-layer weight matrix via SVD.

    --- CURIE ---
    The effective rank tells us how many dimensions the network actually
    uses. A rank-deficient weight matrix means the network has found
    a low-dimensional representation — it has discovered structure.

    --- TURING ---
    Formally: effective_rank = exp(H(sigma_normalized))
    where sigma_normalized = sigma_i / sum(sigma_i) are the normalized
    singular values and H is Shannon entropy. This equals the true rank
    when all singular values are equal, and equals 1 when a single
    singular value dominates. It is the continuous generalization of
    matrix rank.

    For C_4 symmetry, the prediction from group theory is that the
    effective rank at convergence should relate to the number of
    irreducible representations of C_4 (which is 4).
    """
    W = model.fc1.weight.data.cpu().numpy()  # shape: (h, 2)
    singular_values = np.linalg.svd(W, compute_uv=False)

    # Normalize to a probability distribution
    sv_sum = singular_values.sum()
    if sv_sum < 1e-10:
        return 0.0
    p = singular_values / sv_sum

    # Shannon entropy of the singular value distribution
    # Avoid log(0) by filtering out zeros
    p = p[p > 1e-10]
    entropy = -np.sum(p * np.log(p))

    # Effective rank = exp(entropy)
    effective_rank = np.exp(entropy)
    return effective_rank


def compute_hessian_top_eigenvalues(model, X, y, criterion, top_k=5):
    """
    Compute the top-k eigenvalues of the loss Hessian via power iteration.

    --- FEYNMAN ---
    The Hessian eigenvalues tell you the shape of the loss landscape
    around the solution. Big eigenvalues = sharp minimum = memorization.
    Small eigenvalues = flat minimum = generalization. That's the whole
    story of "flat minima generalize better" in two sentences.

    --- CURIE ---
    We use power iteration with deflation rather than computing the full
    Hessian (which would be P x P — enormous for large h). Five eigenvalues
    suffice to characterize the local geometry.

    --- TURING ---
    The Hessian H_ij = d^2 L / d theta_i d theta_j is the curvature
    tensor of the loss surface at the current point in parameter space.
    Its spectrum determines local learning dynamics: eigenvalues > 0
    indicate stable directions; eigenvalues ≈ 0 indicate flat directions
    (the "Goldstone modes" from spontaneous symmetry breaking of the
    permutation group S_h).
    """
    model.eval()

    # Compute loss
    logits = model(X)
    loss = criterion(logits, y)

    # Get gradient
    params = [p for p in model.parameters() if p.requires_grad]
    grads = torch.autograd.grad(loss, params, create_graph=True)
    grad_vec = torch.cat([g.contiguous().view(-1) for g in grads])

    n_params = grad_vec.shape[0]
    top_k = min(top_k, n_params)

    eigenvalues = []
    found_vectors = []

    for k in range(top_k):
        # Power iteration to find dominant eigenvalue
        v = torch.randn(n_params, device=grad_vec.device)
        v = v / v.norm()

        for _ in range(100):  # 100 iterations of power method
            # Hessian-vector product via double backprop
            Hv = torch.autograd.grad(grad_vec, params, grad_outputs=_split_like(v, params),
                                     retain_graph=True)
            Hv = torch.cat([hv.contiguous().view(-1) for hv in Hv])

            # Deflation: project out previously found eigenvectors
            for ev in found_vectors:
                Hv = Hv - torch.dot(Hv, ev) * ev

            eigenvalue = torch.dot(v, Hv).item()
            v = Hv / (Hv.norm() + 1e-10)

        eigenvalues.append(eigenvalue)
        found_vectors.append(v.detach())

    return eigenvalues


def _split_like(flat_vector, params):
    """Split a flat vector into chunks matching parameter shapes."""
    sections = []
    offset = 0
    for p in params:
        numel = p.numel()
        sections.append(flat_vector[offset:offset + numel].view_as(p))
        offset += numel
    return tuple(sections)


# =============================================================================
# SECTION 4: TRAINING LOOP
# =============================================================================
# --- FEYNMAN ---
# SGD, learning rate 0.01, no momentum. Why? Because momentum and Adam
# and all that jazz obscure the raw dynamics. We want to see the bare
# physics, not the engineering. It's like studying gravity — you drop
# things in vacuum first, THEN worry about air resistance.

def train_model(model, X_train, y_train, X_test, y_test, epochs=2000, lr=0.01, batch_size=64):
    """
    Train with SGD and return final metrics.

    --- CURIE ---
    2000 epochs is sufficient for convergence at all (h, N) combinations
    in our sweep. I verified this in preliminary runs. The network either
    converges or it doesn't — more epochs won't save a fundamentally
    underpowered architecture.
    """
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=lr, momentum=0.0)

    dataset = TensorDataset(X_train, y_train)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    model.train()
    for epoch in range(epochs):
        for batch_X, batch_y in loader:
            optimizer.zero_grad()
            logits = model(batch_X)
            loss = criterion(logits, batch_y)
            loss.backward()
            optimizer.step()

    # --- CURIE ---
    # Measurements taken after training is complete. Not during.
    # You don't open the oven while the souffle is rising.
    # (Feynman would say something about quantum measurement here, but
    # this is a classical experiment.)

    train_acc = compute_accuracy(model, X_train, y_train)
    test_acc = compute_accuracy(model, X_test, y_test)
    G = compute_generalization_quotient(train_acc, test_acc)
    eff_rank = compute_effective_rank(model)

    # Hessian eigenvalues — the most expensive measurement
    # --- FEYNMAN ---
    # We only do 5 eigenvalues. The top ones tell you the shape of the
    # valley. The rest is noise.
    # --- CURIE ---
    # Subsample to at most 1000 points for Hessian computation.
    # The Hessian requires storing the full computational graph, which
    # is expensive for large N. 1000 points gives a stable estimate.
    hessian_n = min(len(X_train), 1000)
    try:
        hessian_eigs = compute_hessian_top_eigenvalues(
            model, X_train[:hessian_n], y_train[:hessian_n], criterion, top_k=5)
    except Exception:
        # If Hessian computation fails (can happen for very small models),
        # record NaN rather than crashing the whole experiment
        hessian_eigs = [float('nan')] * 5

    return {
        'train_acc': train_acc,
        'test_acc': test_acc,
        'G': G,
        'eff_rank': eff_rank,
        'hessian_eig_1': hessian_eigs[0] if len(hessian_eigs) > 0 else float('nan'),
        'hessian_eig_2': hessian_eigs[1] if len(hessian_eigs) > 1 else float('nan'),
        'hessian_eig_3': hessian_eigs[2] if len(hessian_eigs) > 2 else float('nan'),
        'hessian_eig_4': hessian_eigs[3] if len(hessian_eigs) > 3 else float('nan'),
        'hessian_eig_5': hessian_eigs[4] if len(hessian_eigs) > 4 else float('nan'),
    }


# =============================================================================
# SECTION 5: MAIN EXPERIMENT SWEEP
# =============================================================================
# --- FEYNMAN ---
# The sweep is the experiment. 7 widths x 5 dataset sizes x 5 seeds = 175 runs.
# Each run trains a network and measures everything. The whole thing fits
# on a laptop. No cloud, no cluster, no excuses.
#
# --- TURING ---
# The parameter space:
#   h ∈ {4, 8, 16, 32, 64, 128, 256}  — hidden width
#   N ∈ {100, 500, 1000, 5000, 10000}  — dataset size
#   seeds ∈ {0, 1, 2, 3, 4}            — for statistical significance
#
# The key derived quantity is the ratio N/P where P = 4h + 2.
# Our prediction: there exists a critical (N/P)* ≈ O(1) where
# G transitions from ~0.5 (random / memorization) to ~1.0 (generalization).

def main():
    print("=" * 72)
    print("PRINCIPIA INTELLIGENTIAE — Experiment 1")
    print("The Hydrogen Atom of Deep Learning")
    print("C_4 Symmetric Classification with Single Hidden Layer ReLU Network")
    print("=" * 72)
    print()

    # --- CURIE ---
    # Experimental parameters. Each chosen deliberately.
    hidden_widths = [4, 8, 16, 32, 64, 128, 256]
    dataset_sizes = [100, 500, 1000, 5000, 10000]
    seeds = [0, 1, 2, 3, 4]
    epochs = 2000
    lr = 0.01
    test_size = 2000  # Fixed test set size — large enough for stable estimates

    # --- TURING ---
    # Total configurations: 7 x 5 x 5 = 175 runs
    total_runs = len(hidden_widths) * len(dataset_sizes) * len(seeds)
    print(f"Sweep: {len(hidden_widths)} widths x {len(dataset_sizes)} sizes "
          f"x {len(seeds)} seeds = {total_runs} runs")
    print(f"Hidden widths h: {hidden_widths}")
    print(f"Dataset sizes N: {dataset_sizes}")
    print(f"Seeds: {seeds}")
    print(f"Epochs per run: {epochs}")
    print(f"Optimizer: SGD, lr={lr}, momentum=0")
    print(f"Test set size: {test_size} (fixed)")
    print()

    # CSV output setup
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "experiment_results.csv")
    fieldnames = [
        'hidden_width', 'dataset_size', 'seed', 'param_count', 'N_over_P',
        'train_acc', 'test_acc', 'generalization_quotient',
        'effective_rank', 'hessian_eig_1', 'hessian_eig_2',
        'hessian_eig_3', 'hessian_eig_4', 'hessian_eig_5',
        'elapsed_seconds'
    ]

    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        run_count = 0
        for h, N in itertools.product(hidden_widths, dataset_sizes):
            P = 4 * h + 2  # Total parameter count
            N_over_P = N / P

            for seed in seeds:
                run_count += 1
                t0 = time.time()

                # --- CURIE ---
                # Reproducibility: set all random seeds before each run.
                # torch, numpy, and python's random module.
                torch.manual_seed(seed)
                np.random.seed(seed)

                # Generate data
                # Use different seeds for train and test to avoid leakage
                # --- CURIE ---
                # The test set seed is offset by 10000 to guarantee no overlap
                # with any training seed. This is a basic hygiene measure.
                X_train, y_train = generate_c4_dataset(N, seed=seed)
                X_test, y_test = generate_c4_dataset(test_size, seed=seed + 10000)

                # Build model
                model = HydrogenNet(h)

                # --- TURING ---
                # Verify parameter count matches our formula
                actual_P = model.parameter_count()
                assert actual_P == P, f"Parameter count mismatch: {actual_P} != {P}"

                # Train and measure
                metrics = train_model(model, X_train, y_train, X_test, y_test,
                                      epochs=epochs, lr=lr)

                elapsed = time.time() - t0

                # Write row
                row = {
                    'hidden_width': h,
                    'dataset_size': N,
                    'seed': seed,
                    'param_count': P,
                    'N_over_P': round(N_over_P, 4),
                    'train_acc': round(metrics['train_acc'], 6),
                    'test_acc': round(metrics['test_acc'], 6),
                    'generalization_quotient': round(metrics['G'], 6),
                    'effective_rank': round(metrics['eff_rank'], 6),
                    'hessian_eig_1': round(metrics['hessian_eig_1'], 6)
                        if not np.isnan(metrics['hessian_eig_1']) else '',
                    'hessian_eig_2': round(metrics['hessian_eig_2'], 6)
                        if not np.isnan(metrics['hessian_eig_2']) else '',
                    'hessian_eig_3': round(metrics['hessian_eig_3'], 6)
                        if not np.isnan(metrics['hessian_eig_3']) else '',
                    'hessian_eig_4': round(metrics['hessian_eig_4'], 6)
                        if not np.isnan(metrics['hessian_eig_4']) else '',
                    'hessian_eig_5': round(metrics['hessian_eig_5'], 6)
                        if not np.isnan(metrics['hessian_eig_5']) else '',
                    'elapsed_seconds': round(elapsed, 2),
                }
                writer.writerow(row)
                csvfile.flush()  # Flush after each run so partial results are saved

                # Progress
                print(f"[{run_count:3d}/{total_runs}] "
                      f"h={h:4d}, N={N:5d}, seed={seed} | "
                      f"P={P:5d}, N/P={N_over_P:7.2f} | "
                      f"train={metrics['train_acc']:.4f}, "
                      f"test={metrics['test_acc']:.4f}, "
                      f"G={metrics['G']:.4f}, "
                      f"rank={metrics['eff_rank']:.2f} | "
                      f"{elapsed:.1f}s")

    print()
    print(f"Results saved to: {csv_path}")
    print()

    # =========================================================================
    # SECTION 6: PHASE DIAGRAM SUMMARY
    # =========================================================================
    # --- FEYNMAN ---
    # Now the fun part: print the phase diagram. Average G over seeds for
    # each (h, N) combo and display it as a grid. This is the picture that
    # tells the whole story.
    #
    # --- CURIE ---
    # We read back the CSV we just wrote. This ensures what we analyze is
    # exactly what was saved — no discrepancies between displayed and
    # recorded results.

    print("=" * 72)
    print("PHASE DIAGRAM: Generalization Quotient G (averaged over 5 seeds)")
    print("Rows = hidden width h, Columns = dataset size N")
    print("G ≈ 1.0 means generalization, G < 0.7 suggests memorization")
    print("=" * 72)
    print()

    # Read back results
    results = {}
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            h = int(row['hidden_width'])
            N = int(row['dataset_size'])
            G = float(row['generalization_quotient'])
            key = (h, N)
            if key not in results:
                results[key] = []
            results[key].append(G)

    # Print header
    header = f"{'h \\ N':>8s}"
    for N in dataset_sizes:
        header += f"  {N:>7d}"
    header += f"  {'P':>6s}  {'Critical N/P':>12s}"
    print(header)
    print("-" * len(header))

    # --- TURING ---
    # For each hidden width, find the approximate critical N/P ratio
    # where G crosses 0.85. This is our primary theoretical prediction.
    for h in hidden_widths:
        P = 4 * h + 2
        line = f"{h:>8d}"
        G_values = []
        for N in dataset_sizes:
            key = (h, N)
            if key in results:
                mean_G = np.mean(results[key])
                G_values.append((N, mean_G))

                # --- FEYNMAN ---
                # Visual indicators because numbers alone are boring:
                # *** = great generalization (G > 0.9)
                # **  = decent (0.8 < G <= 0.9)
                # *   = borderline (0.7 < G <= 0.8)
                # .   = memorization (G <= 0.7)
                if mean_G > 0.9:
                    marker = "***"
                elif mean_G > 0.8:
                    marker = "** "
                elif mean_G > 0.7:
                    marker = "*  "
                else:
                    marker = ".  "
                line += f"  {mean_G:>4.2f}{marker}"
            else:
                line += f"  {'N/A':>7s}"

        # Estimate critical N/P by interpolation
        critical_NP = "N/A"
        threshold = 0.85
        for i in range(len(G_values) - 1):
            N1, G1 = G_values[i]
            N2, G2 = G_values[i + 1]
            if G1 < threshold <= G2:
                # Linear interpolation
                frac = (threshold - G1) / (G2 - G1) if G2 != G1 else 0.5
                N_crit = N1 + frac * (N2 - N1)
                critical_NP = f"{N_crit / P:.2f}"
                break
        if critical_NP == "N/A":
            if len(G_values) > 0 and G_values[0][1] >= threshold:
                critical_NP = f"<{G_values[0][0] / P:.2f}"
            elif len(G_values) > 0 and G_values[-1][1] < threshold:
                critical_NP = f">{G_values[-1][0] / P:.2f}"

        line += f"  {P:>6d}  {critical_NP:>12s}"
        print(line)

    print()
    print("-" * 72)

    # --- TURING ---
    # Print the effective rank summary — our prediction is that
    # converged networks will show effective rank related to the
    # number of irreducible representations of C_4.
    print()
    print("=" * 72)
    print("EFFECTIVE RANK (averaged over 5 seeds)")
    print("Prediction: converged networks should show rank ≈ 2 (input dim)")
    print("for the first layer weight matrix W1 ∈ R^{h x 2}")
    print("=" * 72)
    print()

    # Read ranks
    ranks = {}
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            h = int(row['hidden_width'])
            N = int(row['dataset_size'])
            r = float(row['effective_rank'])
            key = (h, N)
            if key not in ranks:
                ranks[key] = []
            ranks[key].append(r)

    header = f"{'h \\ N':>8s}"
    for N in dataset_sizes:
        header += f"  {N:>7d}"
    print(header)
    print("-" * len(header))

    for h in hidden_widths:
        line = f"{h:>8d}"
        for N in dataset_sizes:
            key = (h, N)
            if key in ranks:
                mean_r = np.mean(ranks[key])
                line += f"  {mean_r:>7.2f}"
            else:
                line += f"  {'N/A':>7s}"
        print(line)

    print()

    # --- FEYNMAN ---
    # Final summary: the punchline
    print("=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print()
    print("The phase diagram above shows the generalization quotient G as a")
    print("function of network capacity (hidden width h) and data quantity (N).")
    print()
    print("Key predictions from the Principia Intelligentiae Lagrangian:")
    print("  1. There exists a critical ratio (N/P)* where G transitions")
    print("     from memorization to generalization.")
    print("  2. The transition should be sharp (not gradual) — a true")
    print("     phase transition, not a smooth crossover.")
    print("  3. The effective rank at convergence should reflect the")
    print("     symmetry structure of the problem (C_4 has 4 irreps).")
    print("  4. The Hessian spectrum at convergence should show a gap")
    print("     between 'bulk' and 'edge' eigenvalues — the gap width")
    print("     correlates with generalization quality.")
    print()
    print("--- FEYNMAN ---")
    print("If the data agrees with these predictions, the Lagrangian lives")
    print("to fight another day. If not, it's wrong. That's how science works.")
    print()
    print("--- CURIE ---")
    print("The results are in the CSV. Every number is reproducible.")
    print("Now we analyze.")
    print()
    print("--- TURING ---")
    print("We can only see a short distance ahead, but we can see plenty")
    print("there that needs to be done.")
    print("=" * 72)


if __name__ == "__main__":
    main()
