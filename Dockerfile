FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1  
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \  
    && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt \  
    && rm -rf /tmp/requirements.txt \  
    && useradd -U skarlet

WORKDIR /app
USER skarlet:skarlet
COPY --chown=skarlet:skarlet . .

CMD [ "python", "-m", "sanic", "docuproof.app:application" ]
