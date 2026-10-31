# Declaración de uso de IA · Recomendadores (LAB08 y LAB09)

**Estudiante:** Emma Carolina Cabrera Valverde
**Asignatura:** INF-8239 · Ciencia de Datos II
**Herramienta:** Claude (Anthropic), asistente conversacional con acceso a los archivos del proyecto

## Procedencia del código

- El proyecto base (paquete `src/inf8239_u03`, `download_data.py`, `audit_data.py`, `lab08_content.py`, `lab09_hybrid.py`, aplicación y pruebas originales) es material del profesor Edwin Ramón José Nolasco.
- Se consultaron como referencia resultados de una ejecución compartida dentro del curso, únicamente para comprobar que las cifras propias fueran coherentes. Las tablas, gráficos y textos de este repositorio salen de mi ejecución.

## En qué ayudó la IA

1. Explicar los pasos del manual y la guía de ejecución, y el orden de los comandos en Windows con `uv`.
2. Modificar `lab09_hybrid.py` para que cada corrida se guarde con su propio nombre y no se sobrescriba.
3. Escribir los scripts `content_queries.py`, `summarize_lab09.py`, `compare_recommenders.py`, `evaluate_profiles.py`, `measure_model_cost.py` y `generate_charts.py`, y la prueba `tests/test_lab09_profiles.py`.
4. Proponer la paleta y el diseño de los gráficos.
5. Redactar borradores del README, Dataset Card, System Card, notebook e informe a partir de mis resultados.

## Qué hice y verifiqué yo

- Ejecuté todos los comandos en mi computadora: descarga y auditoría de MovieLens, LAB08, las seis corridas del híbrido, comparación de modelos, perfiles, costo y gráficos.
- Elegí las películas de consulta (*Amelie*, *Alien* y *Finding Nemo*) y revisé que cada una quedara fuera de su propia lista.
- Comprobé que `uv run pytest -q` diera 9 pruebas aprobadas y que la aplicación Streamlit funcionara con las tres consultas.
- Contrasté las cifras de los documentos con los CSV y JSON de `reports/`. Se corrigió la cobertura del híbrido con α = 0.25: la media correcta es 10.05 % (desviación 0.52 pp).
- Revisé la redacción final y la decisión del System Card.

## Límites

La IA probó algunos scripts en un entorno aparte antes de que yo los ejecutara, pero todos los resultados reportados provienen de las ejecuciones en mi computadora. Los tiempos dependen de ese equipo. Asumo la responsabilidad del código entregado, de la verificación de los resultados y de las conclusiones.
