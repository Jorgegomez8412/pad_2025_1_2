FROM python:3.9-slim

WORKDIR /pad_2025_1_2

COPY setup.py .

RUN pip install -e .

CMD [ "python", "setup.py" ]