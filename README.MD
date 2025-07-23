# Entregables 1 y 2 del Diplomado en Estrategias de datos de Datos

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

