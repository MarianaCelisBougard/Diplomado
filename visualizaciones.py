import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def show_visualization_tab():
    st.header("📈 Visualizaciones por Departamento")

    if 'df_fact' not in st.session_state:
        st.warning("Primero debes construir la tabla de hechos en la pestaña 'Transformación y Métricas'.")
        return

    df_fact = st.session_state['df_fact']
    dim_geo = st.session_state['dim_geo']
    dim_tiempo = st.session_state['dim_tiempo']

    # Merge y limpieza
    df = df_fact.merge(dim_geo, on='id_geo').merge(dim_tiempo, on='id_tiempo')
    df['departamento'] = df['departamento'].str.replace(",", "").str.strip().str.title()

    # ================================
    # PRIMER GRÁFICO
    # ================================
    st.subheader("📊 Serie de tiempo: Tasa de Matriculación vs Cobertura Neta")

    deptos = sorted(df['departamento'].unique())
    selected_depto_1 = st.selectbox("Selecciona un departamento (Gráfico 1)", deptos)

    df_1 = df[df['departamento'] == selected_depto_1]
    df_1 = df_1.groupby('a_o')[['tasa_matriculaci_n_5_16', 'cobertura_neta']].mean().reset_index()

    fig1 = go.Figure()

    fig1.add_trace(go.Scatter(
        x=df_1['a_o'],
        y=df_1['tasa_matriculaci_n_5_16'],
        name='Tasa de matriculación (5-16)',
        mode='lines+markers',
        yaxis='y1',
        line=dict(color='blue')
    ))

    fig1.add_trace(go.Scatter(
        x=df_1['a_o'],
        y=df_1['cobertura_neta'],
        name='Cobertura neta',
        mode='lines+markers',
        yaxis='y2',
        line=dict(color='orange')
    ))

    fig1.update_layout(
        title=f"Serie de tiempo - {selected_depto_1}",
        xaxis=dict(title='Año'),
        yaxis=dict(
            title=dict(text='Tasa de Matriculación (%)', font=dict(color='blue')),
            tickfont=dict(color='blue')
        ),
        yaxis2=dict(
            title=dict(text='Cobertura Neta (%)', font=dict(color='orange')),
            tickfont=dict(color='orange'),
            overlaying='y',
            side='right'
        ),
        legend=dict(x=0.01, y=0.99),
        height=500,
        margin=dict(l=40, r=40, t=60, b=40)
    )

    st.plotly_chart(fig1, use_container_width=True)

    # ================================
    # SEGUNDO GRÁFICO
    # ================================
    st.subheader("📊 Serie de tiempo: Cobertura Bruta vs Otra Métrica")

    selected_depto_2 = st.selectbox("Selecciona un departamento (Gráfico 2)", deptos, index=deptos.index(selected_depto_1))

    df_2 = df[df['departamento'] == selected_depto_2]
    df_2 = df_2.groupby('a_o')[['cobertura_bruta']].mean().reset_index()

    # Simulamos métrica adicional
    if 'repitencia_secundaria' in df.columns:
        df_2['otra_metrica'] = df[df['departamento'] == selected_depto_2].groupby('a_o')['repitencia_secundaria'].mean().values
        nombre_metrica = 'Repitencia secundaria'
    else:
        df_2['otra_metrica'] = df[df['departamento'] == selected_depto_2].groupby('a_o')['tasa_matriculaci_n_5_16'].mean().values
        nombre_metrica = 'Tasa de Matriculación (5-16)'

    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(
        x=df_2['a_o'],
        y=df_2['cobertura_bruta'],
        name='Cobertura Bruta',
        mode='lines+markers',
        yaxis='y1',
        line=dict(color='green')
    ))

    fig2.add_trace(go.Scatter(
        x=df_2['a_o'],
        y=df_2['otra_metrica'],
        name=nombre_metrica,
        mode='lines+markers',
        yaxis='y2',
        line=dict(color='purple')
    ))

    fig2.update_layout(
        title=f"Cobertura Bruta vs {nombre_metrica} - {selected_depto_2}",
        xaxis=dict(title='Año'),
        yaxis=dict(
            title=dict(text='Cobertura Bruta (%)', font=dict(color='green')),
            tickfont=dict(color='green')
        ),
        yaxis2=dict(
            title=dict(text=nombre_metrica, font=dict(color='purple')),
            tickfont=dict(color='purple'),
            overlaying='y',
            side='right'
        ),
        legend=dict(x=0.01, y=0.99),
        height=500,
        margin=dict(l=40, r=40, t=60, b=40)
    )

    st.plotly_chart(fig2, use_container_width=True)





