from dataweb import Dataweb 
import pandas as pd

def main():
    dataweb = Dataweb()
    df = pd.DataFrame()
    df.to_csv("data_web.cvs")

if __name__ == "main":
    main()