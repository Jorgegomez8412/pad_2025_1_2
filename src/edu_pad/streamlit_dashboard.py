import streamlit as st
#from streamlit_pandas_profiling import st_profile_report
from ydata_profiling import ProfileReport
import pandas as pd
import os



def main():


    

    df = pd.read_csv("\src\edu_pad\static\csv\data_webdb.csv")
    columnas = ["abrir","max","min","cerrar","cierre_ajustado","volumen","indicador"]
    df_2 = df[columnas]
    profile = ProfileReport(df_2, title="Dashboard de indicadores del petroleo")
    st.title("Análisis de Datos")
    #st.write(profile.to_html(),unsafe_allow
