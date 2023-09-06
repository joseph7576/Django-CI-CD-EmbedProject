FROM docker.joeho.ir/utils/python:3.10.7-slim-buster
ENV HOME=/app
ENV APP_HOME=/app/backend
# keeps python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# turns off buffering for easier container logging
ENV PYTHONNUNBUFFERED=1


RUN mkdir -p /app && \
    groupadd -r app && useradd --no-log-init -r -g app app && \
    python -m pip install --upgrade pip && \
    mkdir ${APP_HOME} ${APP_HOME}/logs

WORKDIR ${APP_HOME}
EXPOSE 8000

# install requirements
COPY requirements.txt .
COPY . ${APP_HOME}

RUN python -m pip install -r requirements.txt && \
    pip install ipython==8.2.0 && \
    pip install gunicorn
