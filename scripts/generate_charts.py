"""Gráficos de LAB08 y LAB09 a partir de los archivos de reports/.

    uv run python scripts/generate_charts.py
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from inf8239_u03.config import ROOT

REP = ROOT / "reports"
OUT = REP / "graficos"
OUT.mkdir(parents=True, exist_ok=True)

LAVANDA, LAVANDA_BORDE = "#A593D3", "#6B58A6"
MENTA, MENTA_BORDE = "#A8D8C2", "#4F9478"
TINTA, TINTA_2, TENUE, REJILLA, FONDO = "#0B0B0B", "#52514E", "#898781", "#E1E0D9", "#FFFFFF"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Segoe UI", "DejaVu Sans", "Arial"],
    "font.size": 11,
    "axes.edgecolor": "#C3C2B7",
    "axes.labelcolor": TINTA_2,
    "xtick.color": TENUE,
    "ytick.color": TINTA,
})


def estilo(ax, eje="x"):
    for lado in ("top", "right", "left" if eje == "x" else "bottom"):
        ax.spines[lado].set_visible(False)
    ax.grid(axis=eje, color=REJILLA, linewidth=0.8, zorder=0)
    ax.tick_params(axis="y" if eje == "x" else "x", length=0)


def titulo(fig, texto, sub):
    fig.suptitle(texto, x=0.02, ha="left", fontsize=14, fontweight="bold", color=TINTA)
    fig.text(0.02, 0.915, sub, ha="left", color=TINTA_2, fontsize=10)


def etiqueta(ax, x, y, texto, ha="left"):
    ax.text(x, y, texto, va="center", ha=ha, color=TINTA, fontsize=10,
            bbox=dict(facecolor=FONDO, edgecolor="none", pad=1.2), zorder=5)


# 1 · LAB08: Top-10 de popularidad suavizada
pop = pd.read_csv(REP / "popular_top10.csv")
fig, ax = plt.subplots(figsize=(10, 5.6), facecolor=FONDO)
y = np.arange(len(pop))
ax.barh(y, pop["weighted_score"], color=LAVANDA, edgecolor=LAVANDA_BORDE, linewidth=1, height=0.62, zorder=3)
for i, f in pop.iterrows():
    etiqueta(ax, f["weighted_score"] + 0.005, i, f"{f['weighted_score']:.3f}  ·  n = {int(f['count'])}")
ax.set_yticks(y, [t if len(t) < 42 else t[:40] + "…" for t in pop["title"]])
ax.invert_yaxis()
ax.set_xlim(4.0, 4.5)
ax.set_xlabel("Puntuación suavizada (escala de 0.5 a 5)")
estilo(ax)
titulo(fig, "LAB08 · Top-10 por popularidad suavizada", "La media de cada película se acerca a la media global cuando tiene pocas valoraciones")
fig.tight_layout(rect=(0, 0, 1, 0.9))
fig.savefig(OUT / "lab08_popularidad_top10.png", dpi=300, facecolor=FONDO)
plt.close(fig)

# 2 · LAB09: cuatro recomendadores con el mismo protocolo
comp = pd.read_csv(REP / "lab09_models_comparison.csv")
nombres = {"popularidad": "Popularidad", "contenido": "Contenido", "colaborativo": "Colaborativo", "hibrido": "Híbrido (α = 0.75)"}
comp["nombre"] = comp["modelo"].map(nombres)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.8), facecolor=FONDO, sharey=True)
y = np.arange(len(comp))
for ax, col, color, borde, tit in [
    (a1, "hit_rate_at_10", LAVANDA, LAVANDA_BORDE, "HitRate@10 (%)"),
    (a2, "catalog_coverage", MENTA, MENTA_BORDE, "Cobertura del catálogo (%)"),
]:
    vals = comp[col] * 100
    ax.barh(y, vals, color=color, edgecolor=borde, linewidth=1, height=0.6, zorder=3)
    for i, v in enumerate(vals):
        etiqueta(ax, v + vals.max() * 0.02, i, f"{v:.2f} %")
    ax.set_xlim(0, vals.max() * 1.3)
    ax.set_title(tit, loc="left", fontsize=11, color=TINTA)
    estilo(ax)
a1.set_yticks(y, comp["nombre"])
a1.invert_yaxis()
titulo(fig, "LAB09 · Cuatro recomendadores con el mismo protocolo", "587 usuarios evaluables · última valoración retenida · 9,701 películas candidatas · semilla 42")
fig.tight_layout(rect=(0, 0, 1, 0.88))
fig.savefig(OUT / "lab09_comparacion_modelos.png", dpi=300, facecolor=FONDO)
plt.close(fig)

# 3 · LAB09: α = 0.25 frente a α = 0.75 en tres semillas
res = pd.read_csv(REP / "lab09_results.csv")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.8), facecolor=FONDO)
for ax, col, tit in [(a1, "hit_rate_at_10", "HitRate@10 (%)"), (a2, "catalog_coverage", "Cobertura del catálogo (%)")]:
    tope = res[col].max() * 100
    ticks, nombres = [], []
    for j, (alpha, color, borde) in enumerate([(0.25, MENTA, MENTA_BORDE), (0.75, LAVANDA, LAVANDA_BORDE)]):
        sub = res[res["alpha"].eq(alpha)].sort_values("seed")
        vals = sub[col].to_numpy() * 100
        x = j * 4 + np.arange(len(vals))
        ax.bar(x, vals, color=color, edgecolor=borde, linewidth=1, width=0.8, zorder=3)
        for xi, v in zip(x, vals):
            ax.text(xi, v + tope * 0.03, f"{v:.1f}", ha="center", color=TINTA, fontsize=9.5)
        ticks += list(x)
        nombres += [f"s{sd}" for sd in sub["seed"]]
        ax.text(x[1], -tope * 0.2, f"α = {alpha} · media {vals.mean():.2f} %", ha="center", color=TINTA, fontsize=10)
    ax.set_xticks(ticks, nombres)
    ax.tick_params(axis="x", length=0, colors=TENUE)
    ax.set_ylim(0, tope * 1.15)
    ax.set_title(tit, loc="left", fontsize=11, color=TINTA)
    estilo(ax, "y")
titulo(fig, "LAB09 · Estabilidad del híbrido según α y semilla", "Cada barra es una corrida con 20 factores y 12 épocas · semillas 42, 123 y 2026")
fig.tight_layout(rect=(0, 0.05, 1, 0.88))
fig.savefig(OUT / "lab09_alpha_semillas.png", dpi=300, facecolor=FONDO)
plt.close(fig)

# 4 · LAB09: costo frente a calidad según número de factores
cost = pd.read_csv(REP / "lab09_cost_summary.csv").sort_values("factors")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.6), facecolor=FONDO)
etiquetas = [f"{f} factores" for f in cost["factors"]]
x = np.arange(len(cost))
a1.plot(x, cost["rmse"], color=LAVANDA_BORDE, linewidth=2, zorder=3)
a1.scatter(x, cost["rmse"], s=120, color=LAVANDA, edgecolor=LAVANDA_BORDE, linewidth=1.2, zorder=4)
for xi, v in zip(x, cost["rmse"]):
    a1.text(xi, v + 0.0012, f"{v:.4f}", ha="center", color=TINTA, fontsize=10)
a1.set_ylim(1.015, 1.040)
a1.set_xlim(-0.5, len(x) - 0.5)
a1.set_title("RMSE (menor es mejor; eje ampliado)", loc="left", fontsize=11, color=TINTA)
a2.bar(x, cost["matrix_size_mib"], color=MENTA, edgecolor=MENTA_BORDE, linewidth=1, width=0.6, zorder=3)
for xi, v, t in zip(x, cost["matrix_size_mib"], cost["training_seconds"]):
    a2.text(xi, v + 0.08, f"{v:.2f} MiB · {t:.1f} s", ha="center", color=TINTA, fontsize=10)
a2.set_ylim(0, cost["matrix_size_mib"].max() * 1.25)
a2.set_title("Memoria de las matrices latentes y tiempo", loc="left", fontsize=11, color=TINTA)
for ax in (a1, a2):
    ax.set_xticks(x, etiquetas)
    estilo(ax, "y")
titulo(fig, "LAB09 · Costo frente a calidad (Green AI)", "12 épocas · semilla 42 · duplicar factores duplica la memoria; el RMSE mejora menos de 0.01")
fig.tight_layout(rect=(0, 0, 1, 0.88))
fig.savefig(OUT / "lab09_costo_factores.png", dpi=300, facecolor=FONDO)
plt.close(fig)

print("Gráficos generados en", OUT)
