# app.py
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from data_loader import get_egresos, get_deudas, get_ingresos, get_proyectos, get_lista_equipos
from flujo_equipo import flujo_caja_por_equipo
from flujo_proyecto import flujo_caja_por_proyecto

st.title('Flujo de Caja Mensual y Reporte Operativo')

# Obtener listas de proyectos y equipos
proyectos = get_proyectos()
lista_equipos = get_lista_equipos()

# Crear pestañas para cada tipo de reporte
tab1, tab2, tab3, tab4 = st.tabs(["Flujo de Caja General", "Reporte Operativo", "Flujo de Caja por Equipo", "Flujo de Caja por Proyecto"])

with tab1:
    st.header('Flujo de Caja Mensual')
    
    # Selección del rango de fechas
    start_date = st.date_input('Fecha de inicio', value=pd.to_datetime('2023-07-01'))
    end_date = st.date_input('Fecha de fin')

    # Validar que las fechas sean correctas
    if start_date > end_date:
        st.error('La fecha de inicio no puede ser posterior a la fecha de fin.')

    # Confirmar la carga de datos
    cargar_datos = st.button('Cargar Datos')

    if cargar_datos and start_date <= end_date:
        egresos = get_egresos(start_date, end_date)
        deudas = get_deudas(start_date, end_date)
        ingresos = get_ingresos(start_date, end_date)
        
        if not egresos.empty and not deudas.empty and not ingresos.empty:
            st.success('Datos cargados satisfactoriamente.')
        else:
            st.error('Error al cargar uno o más conjuntos de datos.')

        # Mostrar tablas completas
        st.subheader('Ingresos Mensuales')
        st.write(ingresos)
        
        st.subheader('Gastos Mensuales')
        st.write(egresos)
        
        st.subheader('Deudas Mensuales')
        st.write(deudas)
        
        # Convertir fechas a períodos mensuales y filtrar por fecha mínima
        ingresos['mes'] = pd.to_datetime(ingresos['Fecha'])
        egresos['mes'] = pd.to_datetime(egresos['FECHADOC'])
        deudas['mes'] = pd.to_datetime(deudas['Fecha de vencimiento'])
        
        fecha_min_acumulados = pd.to_datetime('2023-07-01')
        
        ingresos_filtrados = ingresos[ingresos['mes'] >= fecha_min_acumulados]
        egresos_filtrados = egresos[egresos['mes'] >= fecha_min_acumulados]
        deudas_filtrados = deudas[deudas['mes'] >= fecha_min_acumulados]
        
        ingresos['mes'] = ingresos['mes'].dt.to_period('M')
        egresos['mes'] = egresos['mes'].dt.to_period('M')
        deudas['mes'] = deudas['mes'].dt.to_period('M')
        
        ingresos_filtrados['mes'] = ingresos_filtrados['mes'].dt.to_period('M')
        egresos_filtrados['mes'] = egresos_filtrados['mes'].dt.to_period('M')
        deudas_filtrados['mes'] = deudas_filtrados['mes'].dt.to_period('M')
        
        # Agrupar y sumar por mes
        ingresos_mensuales = ingresos.groupby('mes')['Subtotal'].sum().reset_index()
        egresos_mensuales = egresos.groupby('mes')['TOTAL'].sum().reset_index()
        deudas_mensuales = deudas.groupby('mes')['Subtotal'].sum().reset_index()
        
        # Agrupar y sumar por mes para acumulados desde la fecha mínima
        ingresos_acumulados = ingresos_filtrados.groupby('mes')['Subtotal'].sum().reset_index()
        egresos_acumulados = egresos_filtrados.groupby('mes')['TOTAL'].sum().reset_index()
        deudas_acumulados = deudas_filtrados.groupby('mes')['Subtotal'].sum().reset_index()
        
        # Calcular gastos totales y flujo de caja
        gastos_mensuales = pd.merge(egresos_mensuales, deudas_mensuales, on='mes', how='outer').fillna(0)
        gastos_mensuales['total_gastos'] = gastos_mensuales['TOTAL'] + gastos_mensuales['Subtotal']
        
        gastos_acumulados = pd.merge(egresos_acumulados, deudas_acumulados, on='mes', how='outer').fillna(0)
        gastos_acumulados['total_gastos'] = gastos_acumulados['TOTAL'] + gastos_acumulados['Subtotal']
        
        flujo_caja_mensual = pd.merge(ingresos_mensuales, gastos_mensuales[['mes', 'total_gastos']], on='mes', how='outer').fillna(0)
        flujo_caja_mensual['flujo_caja_neto'] = flujo_caja_mensual['Subtotal'] - flujo_caja_mensual['total_gastos']
        
        flujo_caja_acumulado = pd.merge(ingresos_acumulados, gastos_acumulados[['mes', 'total_gastos']], on='mes', how='outer').fillna(0)
        flujo_caja_acumulado['flujo_caja_neto'] = flujo_caja_acumulado['Subtotal'] - flujo_caja_acumulado['total_gastos']
        
        # Calcular acumulados desde cero
        flujo_caja_acumulado['ingresos_acumulados'] = flujo_caja_acumulado['Subtotal'].cumsum()
        flujo_caja_acumulado['gastos_acumulados'] = flujo_caja_acumulado['total_gastos'].cumsum()
        flujo_caja_acumulado['flujo_caja_acumulado'] = flujo_caja_acumulado['flujo_caja_neto'].cumsum()
        
        # Crear gráfica de valores mensuales
        fig_barras = go.Figure()
        
        fig_barras.add_trace(go.Bar(
            x=flujo_caja_mensual['mes'].astype(str), 
            y=flujo_caja_mensual['Subtotal'], 
            name='Ingresos Mensuales',
            hovertemplate='Mes: %{x}<br>Ingresos: %{y}<extra></extra>'
        ))
        fig_barras.add_trace(go.Bar(
            x=flujo_caja_mensual['mes'].astype(str), 
            y=flujo_caja_mensual['total_gastos'], 
            name='Gastos Mensuales',
            hovertemplate='Mes: %{x}<br>Gastos: %{y}<extra></extra>'
        ))
        
        fig_barras.update_layout(
            title='Valores Mensuales',
            xaxis_title='Mes',
            yaxis_title='Monto',
            barmode='group'
        )
        
        st.plotly_chart(fig_barras)
        
        # Crear gráfica de valores acumulados
        fig_lineas = go.Figure()
        
        fig_lineas.add_trace(go.Scatter(
            x=flujo_caja_acumulado['mes'].astype(str), 
            y=flujo_caja_acumulado['ingresos_acumulados'], 
            mode='lines+markers', 
            name='Ingresos Acumulados',
            hovertemplate='Mes: %{x}<br>Ingresos Acumulados: %{y}<extra></extra>'
        ))
        fig_lineas.add_trace(go.Scatter(
            x=flujo_caja_acumulado['mes'].astype(str), 
            y=flujo_caja_acumulado['gastos_acumulados'], 
            mode='lines+markers', 
            name='Gastos Acumulados',
            hovertemplate='Mes: %{x}<br>Gastos Acumulados: %{y}<extra></extra>'
        ))
        fig_lineas.add_trace(go.Scatter(
            x=flujo_caja_acumulado['mes'].astype(str), 
            y=flujo_caja_acumulado['flujo_caja_acumulado'], 
            mode='lines+markers', 
            name='Flujo de Caja Acumulado',
            hovertemplate='Mes: %{x}<br>Flujo de Caja Acumulado: %{y}<extra></extra>'
        ))
        
        fig_lineas.update_layout(
            title='Valores Acumulados',
            xaxis_title='Mes',
            yaxis_title='Monto'
        )
        
        st.plotly_chart(fig_lineas)
        
        # Mostrar detalles al hacer clic en una barra
        st.subheader('Detalles de Ingresos y Gastos por Mes')
        mes_seleccionado = st.selectbox('Selecciona el mes', flujo_caja_mensual['mes'].astype(str).unique())
        
        if mes_seleccionado:
            mes_dt = pd.Period(mes_seleccionado, freq='M')
            detalles_ingresos = ingresos[ingresos['mes'] == mes_dt]
            detalles_egresos = egresos[egresos['mes'] == mes_dt]
            detalles_deudas = deudas[deudas['mes'] == mes_dt]
            
            st.subheader(f'Detalles de Ingresos para {mes_seleccionado}')
            st.write(detalles_ingresos)
            
            st.subheader(f'Detalles de Egresos para {mes_seleccionado}')
            st.write(detalles_egresos)
            
            st.subheader(f'Detalles de Deudas para {mes_seleccionado}')
            st.write(detalles_deudas)

with tab2:
    st.header('Reporte Operativo')
    
    # Selección del rango de fechas
    start_date = st.date_input('Fecha de inicio', key='start_date_operativo', value=pd.to_datetime('2023-07-01'))
    end_date = st.date_input('Fecha de fin', key='end_date_operativo')

    # Validar que las fechas sean correctas
    if start_date > end_date:
        st.error('La fecha de inicio no puede ser posterior a la fecha de fin.')

    # Confirmar la carga de datos
    cargar_datos = st.button('Cargar Datos', key='cargar_datos_operativo')

    if cargar_datos and start_date <= end_date:
        egresos = get_egresos(start_date, end_date)
        deudas = get_deudas(start_date, end_date)
        ingresos = get_ingresos(start_date, end_date)
        
        if not egresos.empty and not deudas.empty and not ingresos.empty:
            st.success('Datos cargados satisfactoriamente.')
        else:
            st.error('Error al cargar uno o más conjuntos de datos.')

        # Mostrar tablas completas
        st.subheader('Ingresos Mensuales')
        st.write(ingresos)
        
        st.subheader('Gastos Mensuales')
        st.write(egresos)
        
        st.subheader('Deudas Mensuales')
        st.write(deudas)

with tab3:
    st.header('Flujo de Caja por Equipo')
    
    # Selección del rango de fechas y el ID del equipo
    lista_equipos['id_nombre'] = lista_equipos['Id_equipo'] + ' - ' + lista_equipos['Name']
    equipo_seleccionado = st.selectbox('ID del Equipo', lista_equipos['id_nombre'])
    
    id_equipo = equipo_seleccionado.split(' - ')[0]
    
    start_date = st.date_input('Fecha de inicio', key='start_date_equipo', value=pd.to_datetime('2023-07-01'))
    end_date = st.date_input('Fecha de fin', key='end_date_equipo')

    # Validar que las fechas sean correctas
    if start_date > end_date:
        st.error('La fecha de inicio no puede ser posterior a la fecha de fin.')

    # Confirmar la carga de datos
    cargar_datos = st.button('Cargar Datos', key='cargar_datos_equipo')

    if cargar_datos and start_date <= end_date:
        egresos = get_egresos(start_date, end_date)
        deudas = get_deudas(start_date, end_date)
        ingresos = get_ingresos(start_date, end_date)
        
        if not egresos.empty and not deudas.empty and not ingresos.empty:
            st.success('Datos cargados satisfactoriamente.')

            fig_equipo_barras, fig_equipo_lineas = flujo_caja_por_equipo(ingresos, egresos, id_equipo)
            st.plotly_chart(fig_equipo_barras)
            st.plotly_chart(fig_equipo_lineas)

            # Mostrar tablas completas
            st.subheader('Ingresos del Equipo')
            st.write(ingresos[ingresos['Id_equipo'] == id_equipo])
        
            st.subheader('Gastos del Equipo')
            st.write(egresos[egresos['COD_EQUIPO'] == id_equipo])
            
            st.subheader('Deudas del Equipo')
            st.write(deudas[deudas['EQUIPO'] == id_equipo])
        else:
            st.error('Error al cargar uno o más conjuntos de datos.')

with tab4:
    st.header('Flujo de Caja por Proyecto')
    
    # Selección del rango de fechas y el nombre del proyecto
    proyecto = st.selectbox('Nombre del Proyecto', proyectos['Proyectos'])
    start_date = st.date_input('Fecha de inicio', key='start_date_proyecto', value=pd.to_datetime('2023-07-01'))
    end_date = st.date_input('Fecha de fin', key='end_date_proyecto')

    # Validar que las fechas sean correctas
    if start_date > end_date:
        st.error('La fecha de inicio no puede ser posterior a la fecha de fin.')

    # Confirmar la carga de datos
    cargar_datos = st.button('Cargar Datos', key='cargar_datos_proyecto')

    if cargar_datos and start_date <= end_date:
        egresos = get_egresos(start_date, end_date)
        deudas = get_deudas(start_date, end_date)
        ingresos = get_ingresos(start_date, end_date)
        
        if not egresos.empty and not deudas.empty and not ingresos.empty:
            st.success('Datos cargados satisfactoriamente.')

            fig_proyecto_barras, fig_proyecto_lineas = flujo_caja_por_proyecto(ingresos, egresos, proyecto)
            st.plotly_chart(fig_proyecto_barras)
            st.plotly_chart(fig_proyecto_lineas)
            
            # Mostrar tablas completas
            st.subheader('Ingresos del Proyecto')
            st.write(ingresos[ingresos['Proyecto'] == proyecto])
    
            st.subheader('Gastos del Proyecto')
            st.write(egresos[egresos['NOMBREPROYECTO'] == proyecto])
            
            st.subheader('Deudas del Proyecto')
            st.write(deudas[deudas['Descripcion'] == proyecto])
        else:
            st.error('Error al cargar uno o más conjuntos de datos.')
