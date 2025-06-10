import streamlit as st
from ydata_profiling import ProfileReport
from streamlit.components.v1 import html
import pandas as pd
import os

def main():
    st.title("Análisis de Data: Indicadores del Petróleo")

    # Cargar datos
    try:
        df = pd.read_csv("src/edu_pad/static/csv/data_webdb.csv")
        columnas = ["abrir", "max", "min", "cerrar", "cierre_ajustado", "volumen", "indicador"]
        df_2 = df[columnas]

        st.write("Vista previa de los datos:")
        st.dataframe(df_2.head())

        # Crear el perfil del reporte
        profile = ProfileReport(df_2, title="Dashboard de Indicadores del Petróleo", explorative=True)

        # Mostrar el reporte en Streamlit
        st.write("Reporte de Perfil de Datos:")
        html(profile.to_html(), height=1000, scrolling=True)

    except FileNotFoundError:
        st.error("No se encontró el archivo CSV. Verifica la ruta.")
    except Exception as e:
        st.error(f"Ha ocurrido un error: {e}")

if __name__ == "__main__":
    main()

