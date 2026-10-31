"""LAB08 · Consultas del recomendador por contenido.

Genera el Top-10 por similitud de géneros para tres películas de géneros
distintos y guarda cada lista en reports/content_<consulta>.csv.

    uv run python scripts/content_queries.py
"""

from inf8239_u03.config import MOVIELENS_DIR, ROOT
from inf8239_u03.data import load_movielens
from inf8239_u03.recommenders import ContentRecommender

CONSULTAS = {
    "amelie": "Amelie (Fabuleux destin d'Amélie Poulain, Le) (2001)",
    "alien": "Alien (1979)",
    "finding_nemo": "Finding Nemo (2003)",
}


def main():
    _, movies = load_movielens(MOVIELENS_DIR)
    modelo = ContentRecommender().fit(movies)
    salida = ROOT / "reports"
    salida.mkdir(exist_ok=True)

    for clave, titulo in CONSULTAS.items():
        generos = movies.loc[movies["title"].eq(titulo), "genres"].iloc[0]
        lista = modelo.recommend(titulo, 10)
        lista.to_csv(salida / f"content_{clave}.csv", index=False)

        empates = int((lista["content_score"].round(6) == lista["content_score"].round(6).max()).sum())
        print(f"\n{titulo} · géneros: {generos}")
        print(f"  ¿aparece en su propia lista? {'sí' if titulo in set(lista['title']) else 'no'}")
        print(f"  recomendaciones con la puntuación máxima: {empates} de {len(lista)}")
        print(lista[["title", "genres", "content_score"]].round(4).to_string(index=False))


if __name__ == "__main__":
    main()
