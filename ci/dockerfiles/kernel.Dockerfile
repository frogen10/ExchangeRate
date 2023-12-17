FROM python:3.10.12-bookworm AS kernel
WORKDIR /app
COPY ./ci/requirements/requirements.txt .
RUN apt update && apt install -y tree
RUN pip install -r requirements.txt && rm -f requirements.txt
COPY ./backend .
EXPOSE 8000
CMD [ "./manage.py", "runserver", "0.0.0.0:8000" ]