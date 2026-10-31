"""LAB09 · Costo computacional de la factorización (Green AI).

Entrena una configuración, mide RMSE, parámetros, memoria de las matrices
latentes y tiempo, y guarda reports/lab09_cost_f<factores>_e<epocas>_s<semilla>.json.
Además actualiza reports/lab09_cost_summary.csv con todas las configuraciones medidas.

    uv run python scripts/measure_model_cost.py --factors 20 --epochs 12 --seed 42
"""

import argparse
import json
from time import perf_counter

import pandas as pd
from sklearn.metrics import root_mean_squared_error

from inf8239_u03.config import MOVIELENS_DIR, ROOT
from inf8239_u03.data import load_movielens
from inf8239_u03.recommenders import MatrixFactorization, temporal_leave_one_out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--factors", type=int, default=20)
    p.add_argument("--epochs", type=int, default=12)
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()

    ratings, _ = load_movielens(MOVIELENS_DIR)
    train, test = temporal_leave_one_out(ratings)

    inicio = perf_counter()
    modelo = MatrixFactorization(factors=args.factors, seed=args.seed).fit(train, epochs=args.epochs)
    segundos = perf_counter() - inicio

    evaluables = test[test["userId"].isin(modelo.user_index) & test["movieId"].isin(modelo.item_index)]
    rmse = root_mean_squared_error(
        evaluables["rating"], [modelo.predict(f.userId, f.movieId) for f in evaluables.itertuples()]
    )
    bytes_matrices = modelo.user_factors.nbytes + modelo.item_factors.nbytes

    resultado = {
        "seed": args.seed,
        "factors": args.factors,
        "epochs": args.epochs,
        "users": len(modelo.users),
        "items": len(modelo.items),
        "evaluable_ratings": len(evaluables),
        "rmse": float(rmse),
        "total_parameters": int(modelo.user_factors.size + modelo.item_factors.size),
        "matrix_size_mib": round(bytes_matrices / 1024**2, 4),
        "training_seconds": round(segundos, 4),
    }

    reportes = ROOT / "reports"
    reportes.mkdir(exist_ok=True)
    archivo = reportes / f"lab09_cost_f{args.factors}_e{args.epochs}_s{args.seed}.json"
    archivo.write_text(json.dumps(resultado, indent=2), encoding="utf-8")

    todas = [json.loads(a.read_text(encoding="utf-8")) for a in sorted(reportes.glob("lab09_cost_f*_e*_s*.json"))]
    pd.DataFrame(todas).sort_values("factors").to_csv(reportes / "lab09_cost_summary.csv", index=False)

    print(json.dumps(resultado, indent=2))
    print(f"Guardado en {archivo.name}; resumen con {len(todas)} configuraciones en lab09_cost_summary.csv")


if __name__ == "__main__":
    main()
