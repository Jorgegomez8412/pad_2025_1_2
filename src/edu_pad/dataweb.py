import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime



class Dataweb:
    def __init__(self):
        self.url = "https://es.finance.yahoo.com/quote/CL%3DF/history/"

    def obtener_datos(self):
        try:
            #url cabeceras
            headers = {
                'User-Agent': 'Mozilla/5.0'
            }
            respuesta = requests.get(self.url,headers=headers)
            if respuesta.status_code != 200:
                print("La url no se alcanzó")
            soup = BeautifulSoup(respuesta.text, 'html.parser')
            tabla = soup.select_one('div[data-testid="history-table"] table')
            print(tabla)
        except Exception as err:
            print("Error Al Obtener Datos(Funciòn obtener_datos) ")    







dw = Dataweb()
dw.obtener_datos()
#print(dw.url)