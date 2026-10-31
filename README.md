# INF-8239 · Unidad 03 · Recomendadores de películas (LAB08 y LAB09)

Proyecto base del curso Ciencia de Datos II (autor del proyecto base: Edwin Ramón José Nolasco), ejecutado y documentado por **Emma Carolina Cabrera Valverde**. Compara cuatro formas de recomendar películas sobre MovieLens Latest Small: popularidad suavizada, contenido (TF-IDF de géneros), factorización colaborativa y un híbrido de las dos últimas.

## Requisitos

Python 3.12 y [uv](https://docs.astral.sh/uv/). La primera vez se necesita Internet para instalar dependencias y descargar MovieLens.

```bash
uv python install 3.12
uv sync
```

## Datos

MovieLens no se redistribuye en este repositorio; se descarga en cada equipo:

```bash
uv run python scripts/download_data.py   # imprime el SHA-256 del ZIP descargado
uv run python scripts/audit_data.py      # usuarios, películas, densidad y rango de ratings
```

Fuente, licencia y hash: ver `docs/DATASET_CARD.md`.

## Ejecución

| Paso | Comando | Salida principal en `reports/` |
|---|---|---|
| LAB08 · popularidad y contenido | `uv run python scripts/lab08_content.py` | `popular_top10.csv`, `content_recommendations.csv` |
| LAB08 · tres consultas por contenido | `uv run python scripts/content_queries.py` | `content_amelie.csv`, `content_alien.csv`, `content_finding_nemo.csv` |
| LAB09 · híbrido (una configuración) | `uv run python scripts/lab09_hybrid.py --factors 20 --epochs 12 --alpha 0.75 --seed 42` | `hybrid_metrics.json` y una copia `hybrid_a075_s42.json` |
| LAB09 · resumen de corridas | `uv run python scripts/summarize_lab09.py` | `lab09_results.csv`, `lab09_summary.csv` |
| LAB09 · cuatro modelos, mismo protocolo | `uv run python scripts/compare_recommenders.py` | `lab09_models_comparison.csv`, `lab09_comparison_protocol.csv` |
| LAB09 · tres perfiles de usuario | `uv run python scripts/evaluate_profiles.py` | `profile_*.csv` |
| LAB09 · costo según factores | `uv run python scripts/measure_model_cost.py --factors 10` (y 20, 40) | `lab09_cost_f*_e12_s42.json`, `lab09_cost_summary.csv` |
| Gráficos | `uv run python scripts/generate_charts.py` | `reports/graficos/*.png` |

`lab09_hybrid.py` guarda cada configuración con su propio nombre (`hybrid_a<alpha>_s<semilla>.json`), así que las seis corridas del experimento (α = 0.25 y 0.75 × semillas 42, 123 y 2026) se conservan sin copiar archivos a mano.

## Aplicación y pruebas

```bash
uv run streamlit run app/streamlit_app.py   # recomendador por contenido
uv run pytest -q                            # 9 pruebas
```

La aplicación muestra solo el recomendador por contenido; los demás modelos se evalúan con los scripts.

## Documentación

- `docs/DATASET_CARD.md`: origen, licencia, hash, auditoría y límites de MovieLens.
- `docs/SYSTEM_CARD.md`: modelos, protocolo de evaluación, resultados, riesgos y decisión.
- `AI_USE_DECLARATION.md`: asistencia de IA recibida y verificaciones.
- `notebooks/Ejercicio05_Recomendadores.ipynb`: resultados consolidados.

## Referencia

Harper, F. M., & Konstan, J. A. (2015). The MovieLens Datasets: History and Context. *ACM Transactions on Interactive Intelligent Systems, 5*(4), 19. https://doi.org/10.1145/2827872
