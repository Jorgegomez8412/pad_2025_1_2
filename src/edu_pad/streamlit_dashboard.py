import streamlit as st
from ydata_profiling import ProfileReport
from streamlit.components.v1 import html
import pandas as pd

def main():
    st.title("Análisis de Data: Indicadores del Petróleo")

    try:
        # Cargar el archivo CSV
        df = pd.read_csv("src/edu_pad/static/csv/data_webdb.csv")

        # Mostrar nombres de columnas originales
        st.write("Columnas originales:", df.columns.tolist())

        # Normalizar nombres de columnas
        df.columns = df.columns.str.strip().str.lower()

        columnas_deseadas = ["Abrir", "Max", "Min", "Cerrar", "Cierre_ajustado", "Volumen"]

        # Verificar si todas las columnas están presentes
        if all(col in df.columns for col in columnas_deseadas):
            df_2 = df[columnas_deseadas]

            st.write("Vista previa de los datos:")
            st.dataframe(df_2.head())

            profile = ProfileReport(df_2, title="Dashboard de Indicadores del Petróleo", explorative=True)
            html(profile.to_html(), height=1000, scrolling=True)
        else:
            st.error("Una o más columnas deseadas no se encuentran en el archivo. Revisa los nombres.")

    except FileNotFoundError:
        st.error("No se encontró el archivo CSV. Verifica la ruta.")
    except Exception as e:
        st.error(f"Ha ocurrido un error: {e}")

if __name__ == "__main__":
    main()

