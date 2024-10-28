import pandas as pd 
import plotly.express as px
import streamlit as st
from scipy.interpolate import make_interp_spline
import numpy as np

# Streamlit app title
st.title("Generador Dinámico de Gráficos")

# File uploader for the user to upload an Excel file
uploaded_file = st.file_uploader("Carga un archivo Excel", type="xlsx")

# Check if a file has been uploaded
if uploaded_file is not None:
    # Load the data into a pandas dataframe
    data = pd.read_excel(uploaded_file)

    # Display available columns
    st.write("Columnas disponibles en el archivo cargado:")
    st.write(data.columns)

    # Dropdown menus for selecting x and y axes (or categories/values for pie charts)
    column_options = data.columns.tolist()
    x_column = st.selectbox("Selecciona una columna para el eje X (o categorías para un gráfico de torta)", column_options)
    y_column = st.selectbox("Selecciona una columna para valores del eje Y (o valores para un gráfico de torta)", column_options)

    # Dropdown menu for chart type
    chart_type = st.selectbox("Selecciona el tipo de gráfico", ["Dispersión", "Línea", "Curva Suave", "Barras", "Torta"])

    # Generate the chart based on the user's selection
    if st.button("Generar el Gráfico"):
        if chart_type == "Dispersión":
            fig = px.scatter(data, x=x_column, y=y_column, labels={x_column: x_column, y_column: y_column})
            fig.update_layout(
                title="Gráfico de Dispersión",
                xaxis_title=x_column,
                yaxis_title=y_column
            )

        elif chart_type == "Línea":
            fig = px.line(data, x=x_column, y=y_column, labels={x_column: x_column, y_column: y_column})
            fig.update_layout(
                title="Gráfico de Línea",
                xaxis_title=x_column,
                yaxis_title=y_column
            )

        elif chart_type == "Curva Suave":
            # Smoothing the data using scipy's make_interp_spline
            x_values = data[x_column]
            y_values = data[y_column]
            X_ = np.linspace(x_values.min(), x_values.max(), 500)
            spline = make_interp_spline(x_values, y_values)
            Y_ = spline(X_)
            fig = px.line(x=X_, y=Y_, labels={x_column: x_column, y_column: y_column})
            fig.update_layout(
                title="Curva Suave",
                xaxis_title=x_column,
                yaxis_title=y_column
            )

        elif chart_type == "Barras":
            fig = px.bar(data, x=x_column, y=y_column, labels={x_column: x_column, y_column: y_column})

            # Adjust the y-axis range manually to fit the data range closely
            y_min = data[y_column].min()
            y_max = data[y_column].max()
            fig.update_layout(
                title="Gráfico de Barras",
                xaxis_title=x_column,
                yaxis_title=y_column,
                yaxis=dict(range=[y_min - (y_max - y_min) * 0.05, y_max + (y_max - y_min) * 0.05]),
                yaxis_tickformat="0.1f"
            )

        elif chart_type == "Torta":
            fig = px.pie(data, names=x_column, values=y_column, title="Gráfico de Torta")

        # Display the chart using Streamlit
        st.plotly_chart(fig, use_container_width=True)
else:
    st.write("Por favor carga un archivo Excel para continuar.")
