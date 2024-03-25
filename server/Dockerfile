FROM python:3.8.18
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app/
RUN chmod 777 /usr/src/app/entrypoint.sh
RUN pip install --upgrade pip
RUN pip install markupsafe
RUN pip install --no-cache-dir -r requirements.txt
COPY ./uwsgi.ini /etc/uwsgi.ini
EXPOSE 5000
CMD ["./entrypoint.sh"]