# Use the official Airflow image as the base
FROM apache/airflow:2.9.1

# Set environment variables
ENV AIRFLOW__CORE__EXECUTOR=CeleryExecutor \
    AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow \
    AIRFLOW__CELERY__RESULT_BACKEND=db+postgresql://airflow:airflow@postgres/airflow \
    AIRFLOW__CELERY__BROKER_URL=redis://:@redis:6379/0 \
    AIRFLOW__CORE__FERNET_KEY='' \
    AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION='true' \
    AIRFLOW__CORE__LOAD_EXAMPLES='true' \
    AIRFLOW__API__AUTH_BACKENDS='airflow.api.auth.backend.basic_auth,airflow.api.auth.backend.session' \
    AIRFLOW__SCHEDULER__ENABLE_HEALTH_CHECK='true' \
    _PIP_ADDITIONAL_REQUIREMENTS=pandas

# Install any additional dependencies if required
# RUN pip install pandas
# USER root

# Set airflow user password
# RUN echo "airflow:airflow" | chpasswd

# Copy custom setup scripts or files (like setup_vim.sh)
# COPY ./mysettings/setup_vim.sh /opt/airflow/mysettings/setup_vim.sh

# Make sure the script is executable
# RUN chmod +x /opt/airflow/mysettings/setup_vim.sh

# Set the command for the scheduler service (overrides the default entrypoint)
# CMD ["bash", "-c", "/opt/airflow/mysettings/setup_vim.sh && airflow scheduler"]

# airflow 유저로 복귀
USER airflow

# Copy requirements.txt to the container
COPY docker-settings/requirements.txt /opt/airflow/docker-settings/requirements.txt

# Install Python dependencies from requirements.txt
RUN pip install -r docker-settings/requirements.txt

# Expose the port for health check if needed
EXPOSE 8974

# Optionally add your healthcheck command (this will be part of the docker-compose config)
HEALTHCHECK CMD curl --fail http://localhost:8974/health || exit 1

# Default entrypoint for Airflow
ENTRYPOINT ["/usr/bin/dumb-init", "--"]

# Command for starting Airflow Webserver (can be overridden by docker-compose)
CMD ["webserver"]
