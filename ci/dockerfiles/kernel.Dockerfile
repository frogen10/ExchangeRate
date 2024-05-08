FROM python:3.11-bookworm AS kernel
WORKDIR /app
COPY ./ci/requirements/requirements.txt .
RUN apt-get update && apt-get install -y tree
RUN pip install psycopg2-binary --force-reinstall --no-cache-dir
RUN pip install -r requirements.txt && rm -f requirements.txt
COPY ./backend .
RUN python ./manage.py makemigrations
RUN python ./manage.py makemigrations client exchange transaction
EXPOSE 8000
CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000" ]