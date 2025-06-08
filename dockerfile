FROM python:3.9-slim


WORKDIR /pad_2025_1_2


COPY . .
COPY src/edu_pad/static/csv/data_webdb.csv src/edu_pad/static/csv/data_webdb.csv


RUN mkdir -p static/csv static/db


RUN pip install --upgrade pip && \
    pip install -e . && \
    rm -rf /root/.cache/pip


ENV PYTHONPATH=/pad_2025_1_2/src


ENTRYPOINT ["python", "-m"]
CMD ["edu_pad.main_extraccion", "edu_pad.main_inges" ]
