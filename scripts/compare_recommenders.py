"""LAB09 · Comparación de cuatro recomendadores con el mismo protocolo.

Popularidad suavizada, contenido (perfil TF-IDF del usuario), colaborativo
(factorización) e híbrido se evalúan sobre los mismos usuarios, el mismo corte
temporal y los mismos candidatos: películas vistas en entrenamiento que el
usuario aún no ha valorado.

    uv run python scripts/compare_recommenders.py
"""

from time import perf_counter

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import root_mean_squared_error
from sklearn.metrics.pairwise import cosine_similarity

from inf8239_u03.config import MOVIELENS_DIR, ROOT
from inf8239_u03.data import load_movielens
from inf8239_u03.metrics import catalog_coverage, hit_rate_at_k
from inf8239_u03.recommenders import MatrixFactorization, temporal_leave_one_out

SEMILLA, FACTORES, EPOCAS, ALPHA, K = 42, 20, 12, 0.75, 10


def escalar(valores):
    """Lleva las puntuaciones al rango [0, 1] para poder combinarlas."""
    rango = max(valores.max() - valores.min(), 1e-9)
    return (valores - valores.min()) / rango


def mejores(items, puntuaciones, k=K):
    """Top-k con desempate estable por identificador de película."""
    orden = np.lexsort((items, -puntuaciones))
    return items[orden[:k]].astype(int).tolist()


def popularidad_suavizada(train, catalogo):
    estad = train.groupby("movieId")["rating"].agg(["mean", "count"])
    minimo = estad["count"].quantile(0.80)
    media = train["rating"].mean()
    peso = estad["count"] / (estad["count"] + minimo)
    estad["score"] = peso * estad["mean"] + (1 - peso) * media
    return estad.loc[catalogo, "score"].to_numpy()


def main():
    ratings, movies = load_movielens(MOVIELENS_DIR)
    train, test = temporal_leave_one_out(ratings)

    inicio = perf_counter()
    modelo = MatrixFactorization(factors=FACTORES, seed=SEMILLA).fit(train, epochs=EPOCAS)
    seg_entrenamiento = perf_counter() - inicio

    catalogo = np.asarray(modelo.items, dtype=int)
    posicion = {int(m): i for i, m in enumerate(catalogo)}
    evaluables = test[test["userId"].isin(modelo.user_index) & test["movieId"].isin(modelo.item_index)]

    pop = popularidad_suavizada(train, catalogo)
    generos = movies.set_index("movieId").loc[catalogo, "genres"].str.replace("|", " ", regex=False)
    matriz_generos = TfidfVectorizer().fit_transform(generos)

    listas = {"popularidad": {}, "contenido": {}, "colaborativo": {}, "hibrido": {}}
    inicio = perf_counter()
    for usuario in evaluables["userId"].unique():
        historial = train[train["userId"].eq(usuario)]
        no_vistos = ~np.isin(catalogo, historial["movieId"].to_numpy())
        candidatos = catalogo[no_vistos]

        colab = modelo.global_mean + modelo.item_factors[no_vistos] @ modelo.user_factors[modelo.user_index[usuario]]

        pesos = np.clip(historial["rating"].to_numpy() - 2.5, 0.1, None)
        filas = [posicion[int(m)] for m in historial["movieId"]]
        perfil = np.asarray(matriz_generos[filas].multiply(pesos[:, None]).sum(axis=0) / pesos.sum())
        contenido = cosine_similarity(perfil, matriz_generos[no_vistos]).ravel()

        hibrido = ALPHA * escalar(colab) + (1 - ALPHA) * escalar(contenido)

        u = int(usuario)
        listas["popularidad"][u] = mejores(candidatos, pop[no_vistos])
        listas["contenido"][u] = mejores(candidatos, contenido)
        listas["colaborativo"][u] = mejores(candidatos, colab)
        listas["hibrido"][u] = mejores(candidatos, hibrido)
    seg_ranking = perf_counter() - inicio

    predicciones = [modelo.predict(f.userId, f.movieId) for f in evaluables.itertuples()]
    rmse = root_mean_squared_error(evaluables["rating"], predicciones)

    comparacion = pd.DataFrame([
        {
            "modelo": nombre,
            "hit_rate_at_10": hit_rate_at_k(recs, evaluables, K),
            "catalog_coverage": catalog_coverage(recs, len(catalogo)),
            "usuarios_evaluados": len(recs),
            "candidatos_catalogo": len(catalogo),
            "seed": SEMILLA,
            "k": K,
        }
        for nombre, recs in listas.items()
    ])
    protocolo = pd.DataFrame([{
        "train_interactions": len(train),
        "test_interactions": len(test),
        "evaluable_interactions": len(evaluables),
        "excluded_test_interactions": len(test) - len(evaluables),
        "rmse_collaborative": rmse,
        "train_seconds": seg_entrenamiento,
        "ranking_seconds_all_models": seg_ranking,
        "seed": SEMILLA, "factors": FACTORES, "epochs": EPOCAS, "alpha": ALPHA,
        "candidate_policy": "peliculas del entrenamiento no valoradas por el usuario",
        "relevance_policy": "ultima interaccion de cada usuario",
    }])

    reportes = ROOT / "reports"
    reportes.mkdir(exist_ok=True)
    comparacion.to_csv(reportes / "lab09_models_comparison.csv", index=False)
    protocolo.to_csv(reportes / "lab09_comparison_protocol.csv", index=False)

    print(comparacion.round(4).to_string(index=False))
    print(f"\nUsuarios evaluables: {len(evaluables)} de {len(test)} · RMSE colaborativo: {rmse:.4f}")
    print(f"Entrenamiento: {seg_entrenamiento:.2f} s · ranking de los cuatro modelos: {seg_ranking:.2f} s")


if __name__ == "__main__":
    main()
