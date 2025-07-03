# Traffic-Control

Este repositorio contiene herramientas y notebooks desarrollados para la simulación, análisis y control del tráfico vehicular utilizando Python y Jupyter Notebook. El proyecto está orientado a la aplicación de técnicas de visión computacional, aprendizaje automático y análisis de video para la gestión eficiente del tráfico.

## Características principales

- Procesamiento y análisis de video para detección y seguimiento de vehículos.
- Extracción de métricas como conteo de autos, velocidad promedio y congestión.
- Algoritmos de control de tráfico basados en los datos recolectados.
- Visualización interactiva de resultados mediante Jupyter Notebooks.

## Estructura del repositorio

- `notebooks/`: Contiene los Jupyter Notebooks principales con ejemplos, experimentos y análisis.
- `src/`: Scripts de Python para procesamiento de video y utilidades.
- `data/`: Carpeta para almacenar videos de entrada y otros datos relevantes.
- `output/`: Resultados generados, incluyendo videos procesados (como `output_video`), gráficos y reportes.

## Ejemplo de resultado (video procesado)

A continuación se muestra un fotograma de ejemplo extraído del video `output_video`, que representa la salida generada por el sistema de análisis de tráfico:

![Frame de salida](output/output_video_frame.png)

> **Nota:** Si deseas ver el video completo, consulta el archivo `output/output_video.mp4` en la carpeta correspondiente del repositorio.

## Requisitos

- Python 3.8+
- Jupyter Notebook
- OpenCV
- NumPy
- Otros paquetes listados en `requirements.txt`

## Uso básico

1. Clona este repositorio:
   ```bash
   git clone https://github.com/Gilberter/Traffic-Control.git
   cd Traffic-Control
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Ejecuta los notebooks o scripts según la documentación interna para analizar videos y obtener resultados.

## Contribuciones

Las contribuciones son bienvenidas. Abre un issue o un pull request para sugerir mejoras o reportar problemas.

---

**Autor:** Gilberter  
**Licencia:** MIT
