# Dockerfile

FROM quay.io/astronomer/astro-runtime:12.1.1

# Instala as dependências
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Copia todo o código para o contêiner
COPY . /usr/local/airflow/