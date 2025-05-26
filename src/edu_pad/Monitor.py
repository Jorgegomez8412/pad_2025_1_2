import pandas as pd
import sqlite3
import os
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


class DatabaseMonitor:
    def __init__(self):
        self.rutadb = "src/edu_pad/static/db/dolar_analisis.db"
        self.tabla = "dolar_analisis"
        self.ruta_log = "src/edu_pad/static/logs/monitor_log.json"
        
    def verificar_base_datos(self):
        """Verifica si la base de datos existe y es accesible"""
        if not os.path.exists(self.rutadb):
            print(f"ERROR: Base de datos no encontrada en {self.rutadb}")
            return False
            
        try:
            conn = sqlite3.connect(self.rutadb)
            conn.close()
            print("Base de datos verificada correctamente")
            return True
        except Exception as e:
            print(f"ERROR: No se pudo conectar a la base de datos: {str(e)}")
            return False
    
    def contar_registros(self):
        """Cuenta el número de registros en la tabla y verifica su integridad"""
        try:
            conn = sqlite3.connect(self.rutadb)
            cursor = conn.cursor()
            
            # Contar registros
            cursor.execute(f"SELECT COUNT(*) FROM {self.tabla}")
            total_registros = cursor.fetchone()[0]
            
            # Contar registros con valores nulos en columnas importantes
            cursor.execute(f"SELECT COUNT(*) FROM {self.tabla} WHERE fecha IS NULL OR cerrar IS NULL")
            registros_nulos = cursor.fetchone()[0]
            
            # Obtener fecha del último registro
            cursor.execute(f"SELECT MAX(fecha_update) FROM {self.tabla}")
            ultima_actualizacion = cursor.fetchone()[0]
            
            conn.close()
            
            print(f"Total de registros: {total_registros}")
            print(f"Registros con valores nulos: {registros_nulos}")
            print(f"Última actualización: {ultima_actualizacion}")
            
            return {
                "total_registros": total_registros,
                "registros_nulos": registros_nulos,
                "ultima_actualizacion": ultima_actualizacion,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            print(f"ERROR: No se pudo contar registros: {str(e)}")
            return None
    
    def analizar_tendencia(self):
        """Analiza la tendencia del dólar basado en los últimos registros"""
        try:
            conn = sqlite3.connect(self.rutadb)
            
            # Obtener los últimos 30 registros ordenados por fecha
            query = f"""
            SELECT fecha, cerrar 
            FROM {self.tabla} 
            ORDER BY fecha DESC 
            LIMIT 30
            """
            
            df = pd.read_sql_query(query, conn)
            conn.close()
            
            if len(df) < 5:
                print("No hay suficientes datos para analizar tendencia")
                return None
            
            # Convertir a numérico para el análisis
            df['cerrar'] = pd.to_numeric(df['cerrar'], errors='coerce')
            
            # Calcular medias móviles
            df['ma_5'] = df['cerrar'].rolling(window=5).mean()
            
            # Determinar tendencia basada en la comparación del último valor con la media móvil
            ultimo_valor = df['cerrar'].iloc[0]
            media_movil = df['ma_5'].iloc[0]
            
            if ultimo_valor > media_movil * 1.02:
                tendencia = "ALCISTA"
            elif ultimo_valor < media_movil * 0.98:
                tendencia = "BAJISTA"
            else:
                tendencia = "ESTABLE"
                
            print(f"Análisis de tendencia: {tendencia}")
            return {
                "ultimo_valor": ultimo_valor,
                "media_movil_5": media_movil,
                "tendencia": tendencia
            }
        except Exception as e:
            print(f"ERROR: No se pudo analizar tendencia: {str(e)}")
            return None
    
    def guardar_log(self, metricas):
        """Guarda las métricas en un archivo log JSON"""
        try:
            # Crear el directorio de logs si no existe
            os.makedirs(os.path.dirname(self.ruta_log), exist_ok=True)
            
            # Leer logs existentes si existe el archivo
            if os.path.exists(self.ruta_log):
                with open(self.ruta_log, 'r') as f:
                    try:
                        logs = json.load(f)
                    except:
                        logs = {"registros": []}
            else:
                logs = {"registros": []}
            
            # Añadir el nuevo registro
            logs["registros"].append(metricas)
            
            # Limitar a los últimos 30 registros
            if len(logs["registros"]) > 30:
                logs["registros"] = logs["registros"][-30:]
            
            # Guardar el archivo actualizado
            with open(self.ruta_log, 'w') as f:
                json.dump(logs, f, indent=2)
                
            print(f"Log guardado correctamente en {self.ruta_log}")
            return True
        except Exception as e:
            print(f"ERROR: No se pudo guardar el log: {str(e)}")
            return False
    
    def enviar_alerta(self, asunto, mensaje):
        """Envía una alerta por correo electrónico (configurado mediante variables de entorno)"""
        try:
            # Obtener configuración de correo de variables de entorno
            email_emisor = os.environ.get('EMAIL_SENDER')
            email_receptor = os.environ.get('EMAIL_RECEIVER')
            email_password = os.environ.get('EMAIL_PASSWORD')
            smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
            smtp_port = int(os.environ.get('SMTP_PORT', 587))
            
            if not all([email_emisor, email_receptor, email_password]):
                print("ADVERTENCIA: No se enviará alerta por correo. Faltan credenciales.")
                return False
            
            # Crear mensaje
            msg = MIMEMultipart()
            msg['From'] = email_emisor
            msg['To'] = email_receptor
            msg['Subject'] = asunto
            
            # Añadir cuerpo del mensaje
            msg.attach(MIMEText(mensaje, 'plain'))
            
            # Enviar correo
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(email_emisor, email_password)
            server.send_message(msg)
            server.quit()
            
            print(f"Alerta enviada correctamente a {email_receptor}")
            return True
        except Exception as e:
            print(f"ERROR: No se pudo enviar la alerta: {str(e)}")
            return False
    
    def ejecutar_monitoreo(self):
        """Método principal que ejecuta todas las verificaciones"""
        print("*******************************************************************")
        print(f"Inicio de monitoreo: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("*******************************************************************")
        
        # Verificar base de datos
        if not self.verificar_base_datos():
            self.enviar_alerta(
                "ALERTA: Base de datos no accesible", 
                f"La base de datos dolar_analisis.db no se encuentra o no es accesible. Fecha: {datetime.now()}"
            )
            return False
        
        # Contar registros
        metricas = self.contar_registros()
        if not metricas:
            self.enviar_alerta(
                "ALERTA: Error en monitoreo de DB", 
                f"No se pudo obtener métricas de la tabla {self.tabla}. Fecha: {datetime.now()}"
            )
            return False
        
        # Analizar tendencia
        tendencia = self.analizar_tendencia()
        if tendencia:
            metricas.update(tendencia)
        
        # Guardar log
        self.guardar_log(metricas)
        
        # Verificar alertas basadas en métricas
        if metricas.get("registros_nulos", 0) > 0:
            self.enviar_alerta(
                "ALERTA: Registros con valores nulos", 
                f"Se detectaron {metricas['registros_nulos']} registros con valores nulos en la tabla {self.tabla}."
            )
        
        # Si hay una tendencia fuerte, enviar alerta informativa
        if tendencia and tendencia.get("tendencia") != "ESTABLE":
            self.enviar_alerta(
                f"INFO: Tendencia del dólar {tendencia['tendencia']}", 
                f"Se ha detectado una tendencia {tendencia['tendencia']} en el valor del dólar.\n" +
                f"Último valor: {tendencia['ultimo_valor']}\n" +
                f"Media móvil (5 días): {tendencia['media_movil_5']}"
            )
        
        print("*******************************************************************")
        print(f"Fin de monitoreo: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("*******************************************************************")
        return True


if __name__ == "__main__":
    monitor = DatabaseMonitor()
    monitor.ejecutar_monitoreo()