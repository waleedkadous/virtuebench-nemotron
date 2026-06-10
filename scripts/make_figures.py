#!/usr/bin/env python3
"""
Generate the three report figures for the Nemotron 3 Ultra VirtueBench V2
10-run baseline, in the style of the upstream VirtueBench figures
(scripts/regenerate_figs_2_4.py): grouped bars / boxplots with 95%
bootstrap confidence intervals.

Usage:
    python scripts/make_figures.py

Reads  results/nemotron_10run_sweep.json
Writes figures/fig1_nemotron_bars.png
       figures/fig2_courage_gap.png
       figures/fig3_run_boxplots.png
"""

import json
import random
from pathlib import Path
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results" / "nemotron_10run_sweep.json"
OUTPUT = ROOT / "figures"

MODEL_LABEL = "Nemotron 3 Ultra"
VIRTUES = ["prudence", "justice", "courage", "temperance"]
VARIANTS = ["ratio", "caro", "mundus", "diabolus", "ignatian"]

# Variant colors follow the upstream figures (ratio=blue, mundus=orange,
# caro=green, diabolus=red, ignatian=purple).
VARIANT_COLORS = {
    "ratio": "#2196f3",
    "mundus": "#ff9800",
    "caro": "#4caf50",
    "diabolus": "#f44336",
    "ignatian": "#9c27b0",
}


def bootstrap_ci(values, n_bootstrap=10000, confidence=0.95, seed=42):
    """Bootstrap percentile CI (same as upstream regenerate_figs_2_4.py)."""
    if len(values) <= 1:
        v = values[0] if values else 0.0
        return v, v
    rng = random.Random(seed)
    n = len(values)
    means = sorted(
        sum(values[rng.randint(0, n - 1)] for _ in range(n)) / n
        for _ in range(n_bootstrap)
    )
    alpha = 1 - confidence
    lo = int((alpha / 2) * n_bootstrap)
    hi = int((1 - alpha / 2) * n_bootstrap) - 1
    return means[lo], means[hi]


def load_records():
    records = json.loads(RESULTS.read_text())
    if len(records) != 200:
        raise ValueError(f"Expected 200 cell-run records, got {len(records)}")
    scored = [r for r in records if r.get("accuracy") is not None]
    dropped = [r for r in records if r.get("accuracy") is None]
    for r in dropped:
        print(
            f"Dropping unscored cell-run: {r['virtue']}/{r['variant']} "
            f"run {r['run_index']} (status={r['status']})"
        )
    return scored


def cell_accuracies(records):
    """dict[(virtue, variant)] -> list of per-run accuracies."""
    cells = defaultdict(list)
    for r in records:
        cells[(r["virtue"], r["variant"])].append(r["accuracy"])
    return cells


# ─── Figure 1: Accuracy by virtue and variant ──────────────────────

def make_figure_1(records):
    cells = cell_accuracies(records)

    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(VIRTUES))
    bar_w = 0.75 / len(VARIANTS)
    offsets = np.arange(len(VARIANTS)) - (len(VARIANTS) - 1) / 2

    for i, variant in enumerate(VARIANTS):
        means, ci_lo, ci_hi = [], [], []
        for virtue in VIRTUES:
            accs = cells[(virtue, variant)]
            m = sum(accs) / len(accs)
            lo, hi = bootstrap_ci(accs)
            means.append(m * 100)
            ci_lo.append((m - lo) * 100)
            ci_hi.append((hi - m) * 100)
        ax.bar(
            x + offsets[i] * bar_w, means, bar_w,
            color=VARIANT_COLORS[variant], edgecolor="grey", linewidth=0.5,
            label=variant.capitalize(),
            yerr=[ci_lo, ci_hi], capsize=3,
            error_kw={"elinewidth": 1, "capthick": 1},
        )

    ax.axhline(50, color="grey", ls="--", lw=1, alpha=0.5)
    ax.set_xticks(x)
    ax.set_xticklabels([v.capitalize() for v in VIRTUES], fontsize=12)
    ax.set_ylabel("Accuracy (%)", fontsize=12)
    ax.set_xlabel("Virtue", fontsize=12)
    ax.set_title(
        f"{MODEL_LABEL}: Accuracy by Virtue and Temptation Variant (±95% CI)",
        fontsize=14, fontweight="bold",
    )
    ax.set_ylim(0, 105)
    ax.legend(loc="lower right", fontsize=10)
    ax.grid(axis="y", alpha=0.3)

    out = OUTPUT / "fig1_nemotron_bars.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"Saved: {out}")
    plt.close(fig)


# ─── Figure 2: The courage gap ─────────────────────────────────────

def make_figure_2(records):
    # Per run and variant: courage accuracy vs mean of the other virtues.
    run_accs = defaultdict(dict)  # (variant, run_index) -> {virtue: acc}
    for r in records:
        run_accs[(r["variant"], r["run_index"])][r["virtue"]] = r["accuracy"]

    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(VARIANTS))
    bar_w = 0.35
    light_c, dark_c = "#a8c4e0", "#2166ac"  # upstream courage-gap palette

    for offset, color, label, pick in [
        (-bar_w / 2, light_c, "Other virtues (mean)",
         lambda v: sum(v[u] for u in VIRTUES if u != "courage") / 3),
        (bar_w / 2, dark_c, "Courage",
         lambda v: v["courage"]),
    ]:
        means, ci_lo, ci_hi = [], [], []
        for variant in VARIANTS:
            per_run = [
                pick(virtues)
                for (var, _), virtues in run_accs.items()
                if var == variant and len(virtues) == len(VIRTUES)
            ]
            m = sum(per_run) / len(per_run)
            lo, hi = bootstrap_ci(per_run)
            means.append(m * 100)
            ci_lo.append((m - lo) * 100)
            ci_hi.append((hi - m) * 100)
        bars = ax.bar(
            x + offset, means, bar_w,
            color=color, edgecolor="grey", linewidth=0.5, label=label,
            yerr=[ci_lo, ci_hi], capsize=4,
            error_kw={"elinewidth": 1, "capthick": 1},
        )
        for bar in bars:
            h = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2, h + 2,
                f"{h:.1f}", ha="center", va="bottom", fontsize=9,
            )

    ax.set_xticks(x)
    ax.set_xticklabels([v.capitalize() for v in VARIANTS], fontsize=12)
    ax.set_ylabel("Accuracy (%)", fontsize=12)
    ax.set_xlabel("Temptation Type", fontsize=12)
    ax.set_title(
        f"The Courage Gap: {MODEL_LABEL} (10 runs, ±95% CI)",
        fontsize=14, fontweight="bold",
    )
    ax.set_ylim(0, 110)
    ax.legend(loc="upper left", fontsize=10)
    ax.grid(axis="y", alpha=0.3)

    out = OUTPUT / "fig2_courage_gap.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"Saved: {out}")
    plt.close(fig)


# ─── Figure 3: Run variance boxplots ───────────────────────────────

def make_figure_3(records):
    cells = cell_accuracies(records)

    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(VIRTUES))
    box_w = 0.75 / len(VARIANTS)
    offsets = np.arange(len(VARIANTS)) - (len(VARIANTS) - 1) / 2

    for i, variant in enumerate(VARIANTS):
        data = [
            [a * 100 for a in cells[(virtue, variant)]] for virtue in VIRTUES
        ]
        bp = ax.boxplot(
            data,
            positions=x + offsets[i] * box_w,
            widths=box_w * 0.85,
            patch_artist=True,
            medianprops={"color": "#b2182b", "linewidth": 1.2},
            flierprops={"markersize": 4},
        )
        for patch in bp["boxes"]:
            patch.set_facecolor(VARIANT_COLORS[variant])
            patch.set_alpha(0.8)

    ax.axhline(50, color="grey", ls="--", lw=1, alpha=0.5)
    ax.set_xticks(x)
    ax.set_xticklabels([v.capitalize() for v in VIRTUES], fontsize=12)
    ax.set_ylabel("Accuracy (%)", fontsize=12)
    ax.set_xlabel("Virtue", fontsize=12)
    ax.set_title(
        f"{MODEL_LABEL}: Run Variance by Virtue (10 runs each)",
        fontsize=14, fontweight="bold",
    )
    handles = [
        plt.Rectangle((0, 0), 1, 1, facecolor=VARIANT_COLORS[v], alpha=0.8)
        for v in VARIANTS
    ]
    ax.legend(
        handles, [v.capitalize() for v in VARIANTS],
        loc="lower right", fontsize=10,
    )
    ax.grid(axis="y", alpha=0.3)

    out = OUTPUT / "fig3_run_boxplots.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"Saved: {out}")
    plt.close(fig)


if __name__ == "__main__":
    OUTPUT.mkdir(exist_ok=True)
    records = load_records()
    make_figure_1(records)
    make_figure_2(records)
    make_figure_3(records)
    print("Done.")
