# flujo_equipo.py
import pandas as pd
import plotly.graph_objs as go

def flujo_caja_por_equipo(ingresos, egresos, id_equipo):
    # Filtrar por ID del equipo
    ingresos_equipo = ingresos[ingresos['Id_equipo'] == id_equipo]
    egresos_equipo = egresos[egresos['COD_EQUIPO'] == id_equipo]
    
    # Convertir fechas a períodos mensuales
    ingresos_equipo['mes'] = pd.to_datetime(ingresos_equipo['Fecha']).dt.to_period('M')
    egresos_equipo['mes'] = pd.to_datetime(egresos_equipo['FECHADOC']).dt.to_period('M')
    
    # Agrupar y sumar por mes
    ingresos_mensuales = ingresos_equipo.groupby('mes')['Subtotal'].sum().reset_index()
    egresos_mensuales = egresos_equipo.groupby('mes')['TOTAL'].sum().reset_index()
    
    # Calcular acumulados
    ingresos_mensuales['acumulado'] = ingresos_mensuales['Subtotal'].cumsum()
    egresos_mensuales['acumulado'] = egresos_mensuales['TOTAL'].cumsum()
    flujo_caja_acumulado = ingresos_mensuales['acumulado'] - egresos_mensuales['acumulado']
    
    # Crear gráfica de valores mensuales
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=ingresos_mensuales['mes'].astype(str), 
        y=ingresos_mensuales['Subtotal'], 
        name='Ingresos Mensuales',
        hovertemplate='Mes: %{x}<br>Ingresos: %{y}<extra></extra>'
    ))
    fig.add_trace(go.Bar(
        x=egresos_mensuales['mes'].astype(str), 
        y=egresos_mensuales['TOTAL'], 
        name='Gastos Mensuales',
        hovertemplate='Mes: %{x}<br>Gastos: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Valores Mensuales por Equipo',
        xaxis_title='Mes',
        yaxis_title='Monto',
        barmode='group'
    )
    
    # Crear gráfica de valores acumulados
    fig_lineas = go.Figure()
    
    fig_lineas.add_trace(go.Scatter(
        x=ingresos_mensuales['mes'].astype(str), 
        y=ingresos_mensuales['acumulado'], 
        mode='lines+markers', 
        name='Ingresos Acumulados',
        hovertemplate='Mes: %{x}<br>Ingresos Acumulados: %{y}<extra></extra>'
    ))
    fig_lineas.add_trace(go.Scatter(
        x=egresos_mensuales['mes'].astype(str), 
        y=egresos_mensuales['acumulado'], 
        mode='lines+markers', 
        name='Gastos Acumulados',
        hovertemplate='Mes: %{x}<br>Gastos Acumulados: %{y}<extra></extra>'
    ))
    fig_lineas.add_trace(go.Scatter(
        x=ingresos_mensuales['mes'].astype(str), 
        y=flujo_caja_acumulado, 
        mode='lines+markers', 
        name='Flujo de Caja Acumulado',
        hovertemplate='Mes: %{x}<br>Flujo de Caja Acumulado: %{y}<extra></extra>'
    ))
    
    fig_lineas.update_layout(
        title='Valores Acumulados por Equipo',
        xaxis_title='Mes',
        yaxis_title='Monto'
    )
    
    return fig, fig_lineas
