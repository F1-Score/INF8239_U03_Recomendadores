"""LAB09 · Consolidación de las corridas híbridas.

Lee todos los reports/hybrid_a<alpha>_s<seed>.json que deja lab09_hybrid.py y
produce el detalle por corrida y el resumen (media y desviación) por alpha.

    uv run python scripts/summarize_lab09.py
"""

import json

import pandas as pd

from inf8239_u03.config import ROOT

REPORTES = ROOT / "reports"
METRICAS = ["rmse", "hit_rate_at_10", "catalog_coverage", "train_seconds"]


def main():
    archivos = sorted(REPORTES.glob("hybrid_a*_s*.json"))
    if not archivos:
        raise SystemExit("No hay corridas guardadas: ejecute primero scripts/lab09_hybrid.py")

    corridas = pd.DataFrame(json.loads(a.read_text(encoding="utf-8")) for a in archivos)
    corridas = corridas.sort_values(["alpha", "seed"]).reset_index(drop=True)
    corridas.to_csv(REPORTES / "lab09_results.csv", index=False)

    resumen = corridas.groupby("alpha")[METRICAS].agg(["mean", "std"])
    resumen.columns = [f"{m}_{e}" for m, e in resumen.columns]
    resumen.insert(0, "corridas", corridas.groupby("alpha").size())
    resumen = resumen.reset_index()
    resumen.to_csv(REPORTES / "lab09_summary.csv", index=False)

    print(f"Corridas encontradas: {len(corridas)}")
    print(corridas[["alpha", "seed"] + METRICAS].round(4).to_string(index=False))
    print("\nResumen por alpha (media y desviación estándar):")
    print(resumen.round(4).to_string(index=False))


if __name__ == "__main__":
    main()
