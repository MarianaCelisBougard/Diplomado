# Entregables 1 y 2 del Diplomado en Estrategias de datos de Datos
## Primer entregable

En la carpeta cuadernos encontraaremos un archivo con le nombre "Cuaderno_ETL_Modelo_Estrella_VersionFinal.ipynb" el cual es el resultado para el primer entregable solicitado con las instrucciones del profesor Isaac Zainea, este entregable cuenta con un análisis detallado sobre el rendimiento educativo en Colombia a partir de datos del Ministerio de Educación Nacional, estructurados mediante un modelo estrella y consultados con SQL dentro de Python.

## Estructura general del análisis

- **Limpieza exhaustiva** de cuatro bases de datos relacionadas con educación, proyecciones de población y códigos oficiales (DIVIPOLA).
- **Creación del modelo estrella**: 
  - **Tabla de hechos**: matrícula, aprobación, tasa de cobertura.
  - **Dimensiones**: geografía (a partir de DIVIPOLA), tiempo y niveles educativos.
- **Análisis exploratorio inicial** con visualizaciones y estadísticas descriptivas.

## Preguntas respondidas

1. ¿Qué porcentaje de escolaridad hay respecto a la población?
   Se calculó el total de estudiantes matriculados entre 5 y 16 años frente al total poblacional de esa franja por municipio.  
   Resultado: municipios con tasas superiores al 95% muestran cobertura casi universal.

2. ¿Cómo compararía el rendimiento educativo por municipios?
   Se usó la variable de aprobación para establecer un ranking de los municipios con mayor proporción de estudiantes aprobados.  
  Resultado: se identificaron los municipios con mejor desempeño académico sostenido.

3. ¿Qué departamentos son los que mejor cobertura tienen? ¿Pueden hacer cálculo con SQL?**  
   Se aplicó una consulta SQL para obtener el promedio de la tasa de matrícula obligatoria por departamento.  
   Resultado: algunos departamentos alcanzan más del 97% de cobertura en edad escolar obligatoria.

## 📁 Archivos utilizados
- MEN_ESTADISTICAS_EN_EDUCACION
- Info_2005_2019 y Info_2020_2035 (proyecciones DANE)
- DIVIPOLA (dimensión geográfica oficial)

## Segundo entregable 

#  Aplicación Educativa Interactiva con Streamlit

Este proyecto es una aplicación desarrollada en **Streamlit** que permite explorar, transformar y visualizar indicadores clave de educación en Colombia usando datos del **Ministerio de Educación Nacional (MEN)** y otras fuentes oficiales.

##  Estructura del Proyecto

```
├── app.py                    # Punto de entrada principal con las pestañas
├── cargar_datos.py          # Lógica para cargar datos desde API
├── transformacion.py        # Limpieza, modelo estrella y fuentes adicionales
├── visualizaciones.py       # Panel con múltiples visualizaciones interactivas
├── mapa.py                  # Mapa coroplético por departamento
├── Datos/
│   ├── Info_2005_2019.xlsx      # Proyecciones poblacionales del DANE (histórico)
│   └── Info_2020_2035.xlsx      # Proyecciones poblacionales del DANE (futuro)
├── data/shapes/             # Archivos .shp y relacionados para visualización geográfica
└── DIVIPOLA-_C_digos_municipios_20250623.csv  # Códigos oficiales DANE (DIVIPOLA)
```

## 📥 1. Carga de Datos (`cargar_datos.py`)

- Carga los datos del MEN directamente desde la API oficial de [datos.gov.co](https://www.datos.gov.co/).
- Al presionar el botón, los datos son descargados y almacenados en la sesión de la aplicación (`st.session_state['df_raw']`).

## 🔧 2. Transformación y Modelo Estrella (`transformacion.py`)

- **Limpieza de datos**: se eliminan valores faltantes, se normalizan nombres de departamentos (como San Andrés).
- **Modelo estrella**: se construyen las dimensiones de tiempo y geografía, y una tabla de hechos con indicadores clave:
  - `cobertura_neta`
  - `cobertura_bruta`
  - `tasa_matriculaci_n_5_16`
- **Fuentes secundarias**:
  - Proyecciones poblacionales del DANE (2005–2035).
  - DIVIPOLA (códigos oficiales de municipios).
- Los datos procesados se almacenan en la sesión para usarlos en otras pestañas:
  - `df_fact`, `dim_geo`, `dim_tiempo`

## 📊 3. Visualizaciones Interactivas (`visualizaciones.py`)

Muestra diferentes visualizaciones dinámicas con filtros y análisis de comportamiento educativo:

### 3.1. Serie de tiempo: Tasa de Matriculación vs Cobertura Neta
- Comparación con doble eje entre dos métricas clave para un departamento seleccionado.

### 3.2. Serie de tiempo: Cobertura Bruta vs Otra Métrica
- Muestra la cobertura bruta y otra métrica complementaria, como la repitencia o matrícula.

### 3.3. Boxplot de Cobertura Neta por Año
- Visualiza la dispersión y outliers entre departamentos cada año.

### 3.4. Scatter Plot: Tasa de Matrícula vs Cobertura Neta
- Evalúa la relación entre ambas métricas.

### 3.5. Ranking Top 10 por Indicador y Año
- Ranking interactivo por cobertura o matrícula, configurable por año.

### 3.6. Histograma de Cobertura Bruta
- Muestra cómo se distribuye la cobertura bruta entre los departamentos.

Todas estas gráficas usan Plotly y son completamente interactivas.

## 🗺️ 4. Mapa Interactivo (`mapa.py`)

- Mapa tipo **choropleth** usando `folium` y `geopandas`.
- Permite seleccionar:
  - La métrica (cobertura neta, bruta, matrícula).
  - El año.
- Los colores reflejan los valores promedio por departamento usando el archivo `MGN_ANM_DPTOS.shp` del DANE.

## 📌 Fuentes de Datos Utilizadas

| Fuente | Descripción |
|--------|-------------|
| MEN API | Estadísticas educativas oficiales (Socrata API) |
| DANE    | Proyecciones poblacionales por año y sexo |
| DIVIPOLA | Códigos y nombres oficiales de municipios y departamentos |

## 🚀 Cómo Ejecutar la App

1. Abre la terminal en el directorio raíz del proyecto.

2. Si usas `poetry`:
```bash
poetry install         # Instala dependencias
poetry shell           # Activa el entorno virtual
streamlit run app.py   # Inicia la aplicación
```

## ✅ Requisitos

- Python 3.11
- streamlit
- pandas
- plotly
- geopandas
- openpyxl
- folium
- requests


## ✨ Autor

Desarrollado por Aura Mariana Celis Bougard como parte del Diplomado en Estrategias de Datos de la Universidad Santo Tomas 
Docentes: Wilmer Pineda / Isaac Zainea 
