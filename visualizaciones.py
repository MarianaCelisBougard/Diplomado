import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def show_visualization_tab():
    st.header("📈 Visualizaciones por Departamento")

    if 'df_fact' not in st.session_state:
        st.warning("Primero debes construir la tabla de hechos en la pestaña 'Transformación y Métricas'.")
        return

    df_fact = st.session_state['df_fact']
    dim_geo = st.session_state['dim_geo']
    dim_tiempo = st.session_state['dim_tiempo']

    df = df_fact.merge(dim_geo, on='id_geo').merge(dim_tiempo, on='id_tiempo')

    # 🔍 Filtro único por año
    st.sidebar.header("🎯 Filtros Avanzados")
    years = sorted(df['a_o'].unique())
    selected_years = st.sidebar.multiselect("Filtrar por Año", years, default=years)
    df = df[df['a_o'].isin(selected_years)]

    if df.empty:
        st.warning("⚠️ No hay datos disponibles con los filtros seleccionados.")
        return

    # ================================
    # INDICADORES Y MÉTRICAS CLAVE
    # ================================
    st.subheader("📌 Indicadores Generales")

    cobertura_prom = df['cobertura_neta'].mean()
    escolaridad_std = df['tasa_matriculaci_n_5_16'].std()

    años_ordenados = sorted(df['a_o'].unique())
    primer_año = años_ordenados[0]
    último_año = años_ordenados[-1]

    cobertura_ini = df[df['a_o'] == primer_año]['cobertura_neta'].mean()
    cobertura_fin = df[df['a_o'] == último_año]['cobertura_neta'].mean()
    variación = cobertura_fin - cobertura_ini
    porcentaje_mejora = (variación / cobertura_ini) * 100 if cobertura_ini > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("📊 Prom. Cobertura Neta (%)", f"{cobertura_prom:.2f}")
    col2.metric("📐 Desv. Est. Escolaridad", f"{escolaridad_std:.2f}")
    col3.metric(f"📈 Mejora {primer_año}-{último_año}", f"{porcentaje_mejora:.2f} %")

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

    # ================================
    # TERCER GRÁFICO: RANKING
    # ================================
    st.subheader("🏆 Top Departamentos por Indicador")

    indicador_opcion = st.selectbox(
        "Selecciona el indicador para el ranking",
        ["Tasa de Matriculación (5-16)", "Cobertura Neta (%)", "Cobertura Bruta (%)"]
    )

    col_map = {
        "Tasa de Matriculación (5-16)": "tasa_matriculaci_n_5_16",
        "Cobertura Neta (%)": "cobertura_neta",
        "Cobertura Bruta (%)": "cobertura_bruta"
    }

    columna = col_map[indicador_opcion]

    ranking_df = df.groupby('departamento')[columna].mean().reset_index()
    ranking_df = ranking_df.sort_values(by=columna, ascending=False).head(10)

    fig3 = go.Figure(go.Bar(
        x=ranking_df[columna],
        y=ranking_df['departamento'],
        orientation='h',
        marker_color='indigo'
    ))

    fig3.update_layout(
        title=f"Top 10 Departamentos por {indicador_opcion}",
        xaxis_title=indicador_opcion,
        yaxis_title="Departamento",
        yaxis=dict(autorange="reversed"),
        height=500
    )

    st.plotly_chart(fig3, use_container_width=True)

    # ================================
    # CUARTO GRÁFICO: BOXPLOT DE COBERTURA NETA
    # ================================
    st.subheader("📦 Boxplot de Cobertura Neta por Año")

    fig4 = px.box(
        df,
        x="a_o",
        y="cobertura_neta",
        points="all",
        color_discrete_sequence=["darkorange"],
        labels={"a_o": "Año", "cobertura_neta": "Cobertura Neta (%)"},
        title="Dispersión de la Cobertura Neta por Año"
    )

    st.plotly_chart(fig4, use_container_width=True)

    # ================================
    # ANÁLISIS NARRATIVO / INSIGHTS
    # ================================
    st.subheader("📘 Panel de Insights por Departamento")

    departamento_narrativa = st.selectbox("Selecciona un departamento para análisis narrativo", sorted(df['departamento'].unique()))

    df_depto = df[df['departamento'] == departamento_narrativa].sort_values('a_o')

    if len(df_depto['a_o'].unique()) >= 2:
        año_ini = df_depto['a_o'].min()
        año_fin = df_depto['a_o'].max()

        cobertura_ini = df_depto[df_depto['a_o'] == año_ini]['cobertura_neta'].mean()
        cobertura_fin = df_depto[df_depto['a_o'] == año_fin]['cobertura_neta'].mean()

        variacion = cobertura_fin - cobertura_ini
        variacion_pct = (variacion / cobertura_ini) * 100 if cobertura_ini > 0 else 0

        texto_insight = f"""
        **🧾 Análisis automático para {departamento_narrativa}:**

        Entre **{año_ini} y {año_fin}**, el departamento de **{departamento_narrativa}** mostró una **variación de cobertura neta del {variacion_pct:.2f}%**.

        - Cobertura en {año_ini}: **{cobertura_ini:.2f}%**
        - Cobertura en {año_fin}: **{cobertura_fin:.2f}%**

        {"📈 Mejora significativa en cobertura educativa." if variacion_pct > 5 else "⚠️ Variación leve o negativa. Requiere atención."}
        """
    else:
        texto_insight = f"⚠️ No hay suficientes datos históricos para generar análisis narrativo de **{departamento_narrativa}**."

    st.markdown(texto_insight)






