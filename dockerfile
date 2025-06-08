FROM python:3.9-slim

WORKDIR /pad_2025_1_2

COPY . .

RUN mkdir -p src/edu_pad/src

RUN pip install --upgrade pip \
    && pip install -e . \
    && rm -rf /root/.cache/pip

ENV PYTHONPATH=/pad_2025_1_2/src

ENTRYPOINT ["python", "-m"]
CMD ["edu_pad.main_extraccion"]

