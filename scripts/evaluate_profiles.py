"""LAB09 · Recomendaciones para tres perfiles de usuario.

- historial_amplio (414): muchas valoraciones; usa la señal colaborativa.
- historial_reducido (595): pocas valoraciones; misma señal, menos evidencia.
- usuario_nuevo (999999): no existe en el entrenamiento; recibe la lista de
  popularidad como alternativa no personalizada (fallback).

    uv run python scripts/evaluate_profiles.py
"""

import pandas as pd

from inf8239_u03.config import MOVIELENS_DIR, ROOT
from inf8239_u03.data import load_movielens
from inf8239_u03.recommenders import MatrixFactorization, temporal_leave_one_out

PERFILES = {"historial_amplio": 414, "historial_reducido": 595, "usuario_nuevo": 999999}


def main():
    ratings, movies = load_movielens(MOVIELENS_DIR)
    train, _ = temporal_leave_one_out(ratings)
    modelo = MatrixFactorization(factors=20, seed=42).fit(train, epochs=12)

    populares = (
        train.groupby("movieId")["rating"].agg(["count", "mean"])
        .sort_values(["count", "mean"], ascending=False)
        .head(10).index.tolist()
    )
    reportes = ROOT / "reports"
    reportes.mkdir(exist_ok=True)

    for perfil, usuario in PERFILES.items():
        vistos = set(train.loc[train["userId"].eq(usuario), "movieId"])
        if usuario in modelo.user_index:
            lista = modelo.top_n(usuario, vistos, 10)
            lista["method"] = "collaborative"
        else:
            lista = pd.DataFrame({"movieId": populares, "method": "popularity_fallback"})

        lista = lista.merge(movies[["movieId", "title", "genres"]], on="movieId", how="left")
        lista["profile"], lista["userId"] = perfil, usuario
        lista.to_csv(reportes / f"profile_{perfil}.csv", index=False)

        repetidas = len(vistos & set(lista["movieId"]))
        print(f"\n{perfil} · usuario {usuario} · {len(vistos)} valoraciones en entrenamiento")
        print(f"  método: {lista['method'].iloc[0]} · películas ya vistas en la lista: {repetidas}")
        print(lista[["title", "genres"]].to_string(index=False))


if __name__ == "__main__":
    main()
