from src.edu_pad.database import Database
import pandas as pd



def main():
    database = Database()
    df = pd.read_csv("src\edu_pad\static\csv\data_webdb.csv")
    df_db = database.guardar_df(df)
    df_db2 = database.obtener_datos() # capa 3 guardar 
    df_db2.to_csv("src\edu_pad\static\csv\petroleo_analisis.csv", index=False)



if __name__ == "__main__":
    main()