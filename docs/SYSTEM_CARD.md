# System Card · Recomendador de películas (LAB08 y LAB09)

Autora de la ejecución y la documentación: Emma Carolina Cabrera Valverde. Proyecto base del curso INF-8239 (Edwin Ramón José Nolasco). Todas las cifras provienen de los archivos de `reports/` generados el 31 de octubre de 2026 en Windows 11, Python 3.12 y semilla 42 salvo que se indique otra.

## 1. Propósito y personas usuarias

Prototipo académico que sugiere diez películas a una persona a partir de MovieLens Latest Small. Sirve para comparar métodos de recomendación con un mismo protocolo offline. No está pensado para un servicio real: no mide satisfacción, no tiene datos actuales y no fue probado con usuarios.

## 2. Catálogo y candidatos

- Catálogo de evaluación: 9,701 películas presentes en el entrenamiento.
- Para cada persona se excluyen las películas que ya valoró en el entrenamiento.
- La aplicación Streamlit solo expone el recomendador por contenido; los demás modelos se ejecutan con los scripts.

## 3. Señales usadas

| Señal | Origen | Modelos que la usan |
|---|---|---|
| Número de valoraciones y media por película | `ratings.csv` | Popularidad suavizada, fallback |
| Géneros (TF-IDF) | `movies.csv` | Contenido, híbrido |
| Matriz usuario–película de ratings | `ratings.csv` | Colaborativo, híbrido |

No se usan etiquetas, texto libre, datos demográficos ni información de contexto.

## 4. Modelos

**Popularidad suavizada (LAB08).** Mezcla la media de cada película con la media global según su número de valoraciones; el peso mínimo es el percentil 80 de valoraciones por película. Encabeza el ranking *The Shawshank Redemption (1994)*: media 4.429 con 317 valoraciones, puntuación suavizada 4.395. Es la misma lista para todos.

**Contenido (LAB08).** Vectoriza los géneros con TF-IDF y ordena por similitud coseno. Se consultaron tres películas de géneros distintos:

| Consulta | Géneros | Top-10 |
|---|---|---|
| *Amelie* (2001) | Comedy, Romance | 10 comedias románticas con similitud 1.0 |
| *Alien* (1979) | Horror, Sci-Fi | 10 películas de terror y ciencia ficción con similitud 1.0 |
| *Finding Nemo* (2003) | Adventure, Animation, Children, Comedy | 10 animadas familiares con similitud 1.0 |

En las tres consultas la película de partida no aparece en su lista y los diez resultados empatan en el valor máximo. La similitud mide coincidencia de géneros, no calidad ni probabilidad de que guste.

**Colaborativo (LAB09).** Factorización matricial entrenada con descenso de gradiente estocástico: 20 factores, 12 épocas.

**Híbrido (LAB09).** Combina la puntuación colaborativa (peso α) y la de contenido (peso 1 − α), ambas escaladas a [0, 1]. El perfil de contenido de cada persona se construye con las películas que valoró.

**Usuario nuevo (cold start).** Si la persona no está en el entrenamiento, recibe las diez películas con más valoraciones (desempate por media). Se declara como lista no personalizada.

## 5. Protocolo de evaluación

- Partición temporal: la última valoración de cada usuario se reserva para prueba (610); 100,226 valoraciones quedan para entrenamiento.
- 23 interacciones de prueba son de películas ausentes del entrenamiento y se excluyen: 587 evaluables.
- La película retenida cuenta como relevante sin importar su rating.
- Métricas: RMSE (error de predicción del rating), HitRate@10 (proporción de usuarios cuya película retenida aparece en su Top-10) y cobertura del catálogo (proporción de las 9,701 películas que aparece en al menos una lista).

## 6. Resultados

### Cuatro modelos con el mismo protocolo (semilla 42; híbrido con α = 0.75)

| Modelo | HitRate@10 | Cobertura |
|---|---:|---:|
| Popularidad | 3.24 % | 0.63 % |
| Contenido | 0.17 % | 7.78 % |
| Colaborativo | **3.75 %** | 7.46 % |
| Híbrido | 3.07 % | **9.70 %** |

El colaborativo recupera más películas retenidas; el híbrido reparte mejor la exposición del catálogo. La popularidad tiene un HitRate cercano al colaborativo pero muestra casi siempre las mismas 61 películas. El contenido por sí solo casi no acierta.

### Estabilidad del híbrido (3 semillas: 42, 123, 2026)

| α | RMSE | HitRate@10 | Cobertura | Entrenamiento |
|---|---:|---:|---:|---:|
| 0.25 | 1.0256 ± 0.0012 | 2.90 % ± 0.59 pp | 10.05 % ± 0.52 pp | 14.7 s |
| 0.75 | 1.0256 ± 0.0012 | 3.18 % ± 0.49 pp | 7.37 % ± 0.38 pp | 15.0 s |

El RMSE es idéntico porque α no cambia la factorización, solo el ranking. Más peso colaborativo (0.75) sube el HitRate; más peso de contenido (0.25) amplía la cobertura. Las diferencias de HitRate son del orden de su variación entre semillas.

### Costo frente a calidad (12 épocas, semilla 42)

| Factores | RMSE | Parámetros | Memoria | Tiempo |
|---:|---:|---:|---:|---:|
| 10 | 1.0337 | 103,110 | 0.79 MiB | 14.8 s |
| 20 | 1.0264 | 206,220 | 1.57 MiB | 15.1 s |
| 40 | 1.0211 | 412,440 | 3.15 MiB | 14.9 s |

### Tabla de Pareto

Una configuración está dominada si otra iguala o mejora su utilidad con igual o menor costo.

| Configuración | Utilidad | Costo | ¿Dominada? |
|---|---|---|---|
| 10 factores | RMSE 1.0337 | 0.79 MiB | No (la más barata) |
| 20 factores | RMSE 1.0264 | 1.57 MiB | No |
| 40 factores | RMSE 1.0211 | 3.15 MiB | No (la más precisa) |
| Híbrido α = 0.25 | HR 2.90 %, cobertura 10.05 % | 14.7 s | No (mayor cobertura) |
| Híbrido α = 0.75 | HR 3.18 %, cobertura 7.37 % | 15.0 s | No (mayor HitRate) |

Ninguna opción domina a las demás. Duplicar factores duplica memoria y parámetros, pero el RMSE baja menos de 0.01 en cada paso; el tiempo prácticamente no cambia en este tamaño de datos.

## 7. Perfiles de usuario

| Perfil | Usuario | Valoraciones | Método | Observación |
|---|---:|---:|---|---|
| Historial amplio | 414 | 2,698 | Colaborativo | Lista variada: clásicos, documental, animación japonesa |
| Historial reducido | 595 | 20 | Colaborativo | 5 de sus 10 recomendaciones están en el Top-10 de popularidad |
| Usuario nuevo | 999999 | 0 | Fallback de popularidad | Lista no personalizada |

Con poco historial el modelo colaborativo se acerca a la popularidad: tiene poca información propia de la persona.

## 8. Riesgos y monitoreo

| Riesgo | Señal observada | Mitigación propuesta |
|---|---|---|
| Popularidad dominante | La lista de popularidad cubre 0.63 % del catálogo | Mezclar con contenido; medir cobertura en cada versión |
| Burbuja de filtro | Contenido devuelve solo el mismo grupo de géneros | Reservar posiciones para géneros distintos |
| Cold start | Usuario nuevo recibe una lista genérica | Pedir 3–5 preferencias iniciales |
| Sesgo de selección | Solo hay ratings de películas vistas | No interpretar ausencia como rechazo |
| Retroalimentación | Lo recomendado influye en lo que se valora después | Monitorear concentración del catálogo en el tiempo |
| Sin demografía | No se puede auditar equidad por grupos | Declararlo; no hacer afirmaciones por grupo |

Monitoreo sugerido: HitRate@10, cobertura y proporción de recomendaciones que vienen del fallback, calculados en cada nueva versión.

## 9. Reproducibilidad

- Entorno: `uv`, `pyproject.toml`, `uv.lock`, Python 3.12.
- Comandos y salidas: `README.md`.
- Pruebas: `uv run pytest -q` → 9 aprobadas.
- Las seis corridas del híbrido se guardan como `reports/hybrid_a<alpha>_s<semilla>.json`.
- Notebook con resultados: `notebooks/Ejercicio05_Recomendadores.ipynb`.
- Los tiempos dependen del equipo.

## 10. Decisión

Para este prototipo se selecciona el **híbrido con 20 factores y α = 0.75**. Mantiene un HitRate cercano al colaborativo (3.07 % frente a 3.75 % en la semilla 42; 3.18 % de media en tres semillas) y cubre más catálogo que el colaborativo y que la popularidad. Se usan 20 factores porque 40 duplica la memoria para una mejora de RMSE de 0.005. Los usuarios nuevos reciben el fallback de popularidad, identificado como no personalizado. Si la prioridad fuera la diversidad, α = 0.25 sería la alternativa razonable. La decisión vale solo para la evaluación offline; antes de un uso real haría falta una prueba con personas.
