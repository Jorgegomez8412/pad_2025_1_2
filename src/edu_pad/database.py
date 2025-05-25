import pandas as pd
import sqlite3
import os

# 1 sobre escribir , 2 actualizar 3 insertar al final

class Database:
     def __init__(self):
        self.rutadb = "src\edu_pad\static\db\petroleo_analisis.db"
        

     def guardar_df(self,df=pd.DataFrame()):
        df = df.copy()
        try:
            conn = sqlite3.connect(self.rutadb)
            df["fecha_create"] = "2025-05-25"
            df["fecha_update"] = "2025-05-25"
            df.to_sql("petroleo_analisis", conn,if_exists='replace', index=False)
            print("**************************************************************************")
            print("Datos Guardados")
            print("**************************************************************************")
            print("Se guardo el df en la base de datos  con la cantidad de registros {str(df.shape)}")
        except Exception as errores:
            print("Error al guardar el df en la base de datos{}".format(df.shape))
     
     
     def obtener_datos(self,nombre_tabla = "petroleo_analisis"):
            try:
                 conn = sqlite3.connect(self.rutadb)
                 consulta = "select * from {}".format(nombre_tabla)
                 df = pd.read_sql_query(consulta,conn)
                 print("**************************************************************************")
                 print("Se obtuvieron los datos desde la DB")
                 print("**************************************************************************")
                 print("Base de datos cantidad de registros {}".format(df.shape))
                 return df            
            except Exception as errores:
                 #return df
                 print("Error al obtener los datos de la tabla {str(nombre_tabla)}  en la base de datos {str(errores)}")


