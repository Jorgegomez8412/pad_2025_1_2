from dataweb import Dataweb
import pandas as pd


def main():
    dataweb = Dataweb()
    df = dataweb.obtener_datos()
    df = dataweb.convetir_numericos(df)
    df.to_csv("src\edu_pad\static\data_webdb.csv", index=False)


if __name__ == "__main__":
    main()