# flujo_proyecto.py
import pandas as pd
import plotly.graph_objs as go

def flujo_caja_por_proyecto(ingresos, egresos, proyecto):
    # Filtrar por proyecto
    ingresos_proyecto = ingresos[ingresos['Proyecto'] == proyecto]
    egresos_proyecto = egresos[egresos['NOMBREPROYECTO'] == proyecto]
    
    # Convertir fechas a períodos mensuales
    ingresos_proyecto['mes'] = pd.to_datetime(ingresos_proyecto['Fecha']).dt.to_period('M')
    egresos_proyecto['mes'] = pd.to_datetime(egresos_proyecto['FECHADOC']).dt.to_period('M')
    
    # Agrupar y sumar por mes
    ingresos_mensuales = ingresos_proyecto.groupby('mes')['Subtotal'].sum().reset_index()
    egresos_mensuales = egresos_proyecto.groupby('mes')['TOTAL'].sum().reset_index()
    
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
        title='Valores Mensuales por Proyecto',
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
        title='Valores Acumulados por Proyecto',
        xaxis_title='Mes',
        yaxis_title='Monto'
    )
    
    return fig, fig_lineas
