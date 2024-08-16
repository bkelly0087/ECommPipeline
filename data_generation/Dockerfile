FROM python:3.9

WORKDIR /opt/airflow/data_generation

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /opt/airflow/data_generation/generated_data

CMD ["python", "generate_data.py"]