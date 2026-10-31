# Dataset Card · MovieLens Latest Small

## Identificación

| Campo | Valor |
|---|---|
| Nombre | MovieLens Latest Small (`ml-latest-small`) |
| Responsable | GroupLens Research, University of Minnesota |
| Obtención | `scripts/download_data.py` (descarga directa desde GroupLens) |
| Fecha de descarga | 31 de octubre de 2026 |
| SHA-256 del ZIP | `696d65a3dfceac7c45750ad32df2c259311949efec81f0f144fdfb91ebc9e436` |
| Ubicación local | `data/raw/ml-latest-small/` (excluida de Git) |
| Periodo cubierto | 29-03-1996 a 24-09-2018 (timestamps 828124615 a 1537799250) |

## Licencia y forma de citarlo

El README oficial de GroupLens permite el uso con fines de investigación con tres condiciones: no insinuar respaldo de la Universidad de Minnesota ni de GroupLens, citar el dataset en los trabajos que lo utilicen y no redistribuirlo sin permiso. Por esa última condición, este repositorio guarda solo el script de descarga y el hash, no los archivos CSV.

Cita: Harper, F. M., & Konstan, J. A. (2015). The MovieLens Datasets: History and Context. *ACM Transactions on Interactive Intelligent Systems, 5*(4), 19. https://doi.org/10.1145/2827872

## Archivos utilizados

| Archivo | Filas | Columnas | Uso en el proyecto |
|---|---:|---|---|
| `ratings.csv` | 100,836 | `userId`, `movieId`, `rating`, `timestamp` | Popularidad, factorización, partición temporal y evaluación |
| `movies.csv` | 9,742 | `movieId`, `title`, `genres` | Catálogo, títulos y TF-IDF de géneros |
| `tags.csv` | 3,683 | `userId`, `movieId`, `tag`, `timestamp` | No se usa |
| `links.csv` | 9,742 | `movieId`, `imdbId`, `tmdbId` | No se usa |

`rating` va de 0.5 a 5.0 en pasos de 0.5. `genres` es una lista separada por `|`; 34 películas tienen el valor `(no genres listed)`.

## Auditoría (`scripts/audit_data.py`)

| Indicador | Valor |
|---|---:|
| Usuarios | 610 |
| Películas en el catálogo | 9,742 |
| Películas con al menos una valoración | 9,724 |
| Valoraciones | 100,836 |
| Densidad | 0.016968 (≈ 1.70 %) |
| Media / mediana / desviación | 3.5016 / 3.5 / 1.0425 |
| Valoraciones por usuario (mín. / mediana / máx.) | 20 / 70.5 / 2,698 |
| Películas con una sola valoración | 3,446 |

Lectura: solo 1.70 % de los pares usuario–película tiene una valoración. El resto es desconocido; no significa que la persona rechazara la película. La distribución está muy concentrada: el 10 % de películas más valoradas reúne cerca del 60 % de todas las valoraciones, y 3,446 títulos tienen una sola. Esto favorece a los títulos populares en cualquier modelo que aprenda de las interacciones.

## Población y exclusiones

- Cada usuario del conjunto tiene al menos 20 valoraciones (criterio de GroupLens). Personas con poca actividad no están representadas.
- No hay datos demográficos, así que no es posible medir resultados por grupos de población.
- Para la evaluación del LAB09 se retiene la última valoración de cada usuario (610). 23 de ellas corresponden a películas que no aparecen en el entrenamiento y se excluyen; quedan 587 interacciones evaluables y 9,701 películas candidatas.

## Calidad, sesgos y límites

- **Sesgo de selección:** solo hay valoraciones de películas que la persona eligió ver.
- **Sesgo de popularidad:** pocas películas concentran la mayoría de las valoraciones.
- **Géneros como única descripción de contenido:** muchas películas comparten exactamente la misma combinación, lo que produce empates en la similitud.
- **Antigüedad:** los datos terminan en 2018 y no representan gustos actuales.
- **Usuarios anónimos:** los identificadores no permiten reidentificar a nadie, pero el historial de valoraciones sigue siendo información de comportamiento y se trata con cuidado.

## Evidencia relacionada (LAB08)

- Auditoría en terminal: captura del informe.
- Top-10 de popularidad: `reports/popular_top10.csv` y `reports/graficos/lab08_popularidad_top10.png`.
- Consultas por contenido: `reports/content_amelie.csv`, `reports/content_alien.csv`, `reports/content_finding_nemo.csv`.
