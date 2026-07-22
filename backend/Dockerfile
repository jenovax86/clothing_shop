FROM python:3.10
LABEL authors="jenova"

WORKDIR /backend

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-root

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]