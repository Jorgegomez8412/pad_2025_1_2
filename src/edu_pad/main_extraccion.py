from src.edu_pad.dataweb import Dataweb
import pandas as pd


def main():
    dataweb = Dataweb()
    df = dataweb.obtener_datos()
    df = dataweb.convetir_numericos(df)
    print("Holis")
    output_path = "src/edu_pad/static/csv/data_webdb.csv"
    df.to_csv(output_path, index=False)
    print(f"Archivo guardado en: {output_path}")


if __name__ == "__main__":
    main()