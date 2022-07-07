FROM python:3.8-alpine
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/requirements.txt
RUN apk add -u gcc musl-dev
RUN pip install --no-cache-dir -r /code/requirements.txt
COPY . /code/

COPY docker-entrypoint.sh /code/docker-entrypoint.sh
RUN chmod +x /code/docker-entrypoint.sh
ENTRYPOINT ["sh", "/code/docker-entrypoint.sh"]
