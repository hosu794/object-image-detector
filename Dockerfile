FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1s

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY . .

EXPOSE 8080

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
