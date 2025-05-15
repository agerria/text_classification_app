FROM python:3.12

ADD . /var/www/html/
WORKDIR /var/www/html/
RUN pip install -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/var/www/html/app"
RUN rq worker-pool -n 16 tasks
RUN chmod +x entry_point.sh
ENTRYPOINT ["./entry_point.sh"]