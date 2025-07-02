import streamlit as st

from cargar_datos import show_data_tab
from transformacion import show_transform_tab
from visualizaciones import show_visualization_tab

# Crear pestañas en el cuerpo de la aplicación
tabs = st.tabs(["📥 Carga de Datos", "🔧 Transformación y Métricas", "📊 Visualizaciones", "🗺️ Mapa"])

# Mostrar contenido en cada pestaña
with tabs[0]:
    show_data_tab()

with tabs[1]:
    show_transform_tab()

with tabs[2]:
    show_visualization_tab()

import folium
from streamlit_folium import folium_static

with tabs[3]:
    st.subheader("🗺️ Mapa Geográfico de Departamentos")

    if 'dim_geo' in st.session_state:
        geo_df = st.session_state['dim_geo'].copy()

        # Simulamos coordenadas (esto deberías completarlo con todos los deptos)
        geo_df['lat'] = geo_df['departamento'].map({
            'Bogotá, D.C.': 4.7110,
            'Antioquia': 6.2518,
            'Valle del Cauca': 3.4516,
            'Atlántico': 10.9685
        })
        geo_df['lon'] = geo_df['departamento'].map({
            'Bogotá, D.C.': -74.0721,
            'Antioquia': -75.5636,
            'Valle del Cauca': -76.5320,
            'Atlántico': -74.7813
        })

        geo_df = geo_df.dropna(subset=['lat', 'lon'])

        m = folium.Map(location=[4.5709, -74.2973], zoom_start=5)

        for _, row in geo_df.iterrows():
            folium.CircleMarker(
                location=[row['lat'], row['lon']],
                radius=8,
                color='blue',
                fill=True,
                fill_color='blue',
                popup=f"{row['departamento']} - {row['municipio']}"
            ).add_to(m)

        folium_static(m)
    else:
        st.warning("❌ No hay datos disponibles para el mapa.")


