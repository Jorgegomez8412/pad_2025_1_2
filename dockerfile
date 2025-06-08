FROM python:3.9-slim

# Crear directorio de trabajo
WORKDIR /pad_2025_1_2

# Copiar todo el contenido del proyecto
COPY . .

# Crear carpetas necesarias
RUN mkdir -p static/csv static/db

# Instalar dependencias del proyecto
RUN pip install --upgrade pip && \
    pip install -e . && \
    rm -rf /root/.cache/pip

# Establecer variable de entorno para PYTHONPATH
ENV PYTHONPATH=/pad_2025_1_2/src

# Comando por defecto al iniciar el contenedor
ENTRYPOINT ["python", "-m"]
CMD ["edu_pad.main_extraccion"]
