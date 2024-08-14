import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from data_loader import get_egresos, get_deudas, get_ingresos, get_proyectos, get_lista_equipos
from flujo_equipo import flujo_caja_por_equipo
from flujo_proyecto import flujo_caja_por_proyecto
from flujo_general import flujo_caja_general

st.title('Flujo de Caja Mensual y Reporte Operativo')

# Obtener listas de proyectos y equipos
proyectos = get_proyectos()
lista_equipos = get_lista_equipos()

# Crear pestañas para cada tipo de reporte
tab1, tab2, tab3, tab4 = st.tabs(["Flujo de Caja General", "Reporte Operativo", "Flujo de Caja por Equipo", "Flujo de Caja por Proyecto"])

with tab1:
    flujo_caja_general()

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


