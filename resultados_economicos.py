import pandas as pd
import plotly.express as px
import streamlit as st

def calcular_utilidad_proyectos(ingresos, egresos):
    ingresos_proyectos = ingresos.groupby('Proyecto')['Subtotal'].sum().reset_index()
    egresos_proyectos = egresos.groupby('NOMBREPROYECTO')['TOTAL'].sum().reset_index()
    egresos_proyectos.rename(columns={'NOMBREPROYECTO': 'Proyecto'}, inplace=True)
    utilidad_proyectos = pd.merge(ingresos_proyectos, egresos_proyectos, on='Proyecto', how='outer').fillna(0)
    utilidad_proyectos['Utilidad'] = utilidad_proyectos['Subtotal'] - utilidad_proyectos['TOTAL']
    return utilidad_proyectos

def generar_graficos_economicos(ingresos, egresos):
    # Calcula la utilidad
    utilidad_proyectos = calcular_utilidad_proyectos(ingresos, egresos)
    
    # Utilidad total
    utilidad_total = utilidad_proyectos['Utilidad'].sum()
    
    # ROI: Retorno sobre la inversión
    inversion_inicial = utilidad_proyectos['TOTAL'].sum()
    roi = (utilidad_total / inversion_inicial) * 100 if inversion_inicial != 0 else 0
    
    # Margen de beneficio: (Ingresos - Egresos) / Ingresos
    total_ingresos = utilidad_proyectos['Subtotal'].sum()
    total_egresos = utilidad_proyectos['TOTAL'].sum()
    margen_beneficio = ((total_ingresos - total_egresos) / total_ingresos) * 100 if total_ingresos != 0 else 0
    
    # Gráfico de Treemap
    fig = px.treemap(
        utilidad_proyectos, 
        path=['Proyecto'], 
        values='Utilidad',
        color='Utilidad',
        color_continuous_scale='RdYlGn',
        title='Utilidad por Proyecto'
    )
    
    return utilidad_proyectos, utilidad_total, roi, margen_beneficio, fig

def mostrar_resultados_economicos(ingresos, egresos, inversion_inicial):
    st.header('Resultados Económicos')
    
    # Generar gráficos económicos
    utilidad_proyectos, rentabilidad, roi, margen_beneficio, fig_rentabilidad = generar_graficos_economicos(ingresos, egresos)
    
    # Mostrar resultados clave
    st.subheader('Indicadores Clave')
    st.metric('Rentabilidad Total', f"${rentabilidad:,.2f}")
    st.metric('ROI (Retorno sobre la Inversión)', f"{roi:.2f}%")
    st.metric('Márgen de Beneficio', f"{margen_beneficio:.2f}%")
    
    # Mostrar gráfico de rentabilidad
    st.plotly_chart(fig_rentabilidad)

    # Desglose de costos - Asegúrate de que la columna 'Categoria' exista en egresos
    if 'Categoria' in egresos.columns:
        st.subheader('Desglose de Costos')
        costos_categoria = egresos.groupby('Categoria')['TOTAL'].sum().reset_index()
        fig_costos = px.bar(costos_categoria, x='Categoria', y='TOTAL', title='Desglose de Costos por Categoría')
        st.plotly_chart(fig_costos)
    else:
        st.warning("La columna 'Categoria' no está presente en los datos de egresos.")

    # Equipos y Proyectos Rentables/No Rentables
    st.subheader('Equipos y Proyectos Rentables/No Rentables')
    rentables = utilidad_proyectos[utilidad_proyectos['Utilidad'] > 0]
    no_rentables = utilidad_proyectos[utilidad_proyectos['Utilidad'] <= 0]
    st.write('Proyectos Rentables', rentables)
    st.write('Proyectos No Rentables', no_rentables)
