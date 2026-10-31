from inf8239_u03.recommenders import MatrixFactorization


def _modelo(sample_ratings):
    return MatrixFactorization(factors=3, seed=42).fit(sample_ratings, epochs=2)


def test_lista_colaborativa_no_repite_peliculas_vistas(sample_ratings):
    vistas = set(sample_ratings.loc[sample_ratings["userId"].eq(1), "movieId"])
    lista = _modelo(sample_ratings).top_n(1, vistas, 5)
    assert not set(lista["movieId"]) & vistas
    assert len(lista) <= 5


def test_usuario_sin_historial_requiere_fallback(sample_ratings):
    lista = _modelo(sample_ratings).top_n(999999, set(), 10)
    assert lista.empty
