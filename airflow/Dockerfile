FROM apache/airflow:latest-python3.10

COPY ./dags/ ${AIRFLOW_HOME}/dags/
COPY ./src/ ${AIRFLOW_HOME}/src/
COPY ./requirements.txt ${AIRFLOW_HOME}/requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:${AIRFLOW_HOME}"
RUN pip install -r ${AIRFLOW_HOME}/requirements.txt
