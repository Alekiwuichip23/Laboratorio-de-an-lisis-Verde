# Verde Analytics Lab

Aplicación interactiva desarrollada en Streamlit para la visualización de distribuciones de probabilidad, ejecución de pruebas de hipótesis (Prueba Z) y asistencia en la toma de decisiones utilizando inteligencia artificial.

## Módulos Implementados
1. **Adquisición de Datos:** Carga de archivos CSV numéricos o generación de datos sintéticos.
2. **Visualización y Análisis:** Histogramas, estimación KDE y Boxplots para detección de outliers.
3. **Prueba de Hipótesis (Z-Test):** Cálculo exacto de estadístico Z, P-value y visualización interactiva de la región de rechazo.
4. **Asistente IA:** Integración con Gemini 2.5 Flash para interpretar los resultados y comparar con el análisis humano.

---

## Documentación de Uso de Inteligencia Artificial (Análisis Obligatorio)

**Herramientas utilizadas:**
* Asistente Gemini (Modelo base y API de `gemini-2.5-flash`).

**¿Qué partes utilicé y cuáles no?**
* **Sí utilicé:** La refactorización del código para limpiar el CSS innecesario, la lógica matemática con `scipy.stats` para sombrear las colas de la distribución normal en Plotly, y la estructura del prompt estadístico.
* **No utilicé:** Sugerencias de estructuras complejas con múltiples funciones (`def main()`), prefiriendo una ejecución lineal en Streamlit para mayor legibilidad.

**Análisis Crítico:**
* **¿La IA cometió errores?** Sí. En versiones iniciales, el código generado no mantenía los resultados de la prueba Z en pantalla; al interactuar con el cuadro de texto del asistente, la página se recargaba y las gráficas desaparecían.
* **¿Tuviste que corregir algo? ¿Qué?** Tuve que corregir el flujo de datos implementando `st.session_state` en Streamlit. Esto fue clave para guardar el dataframe cargado y los resultados matemáticos, evitando así que se borraran en cada interacción.
* **¿Qué parte no entendías inicialmente?** No tenía claro cómo mandar la información a la API de Gemini sin enviarle todo el archivo CSV (lo cual habría sobrecargado la memoria). Aprendí a extraer un "resumen estadístico" (media, n, sigma, alpha, valor Z) e inyectarlo en el prompt.
