FROM python:3.12

RUN pip install --no-cache-dir poetry

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-root 

COPY . .

RUN mkdir -p /app/staticfiles

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
