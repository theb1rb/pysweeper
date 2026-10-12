FROM python:3.14-alpine

COPY . /opt/pysweeper/
WORKDIR /opt/pysweeper/
RUN python3 -m venv .venv && \
    .venv/bin/pip install -r requirements.txt

CMD [ ".venv/bin/python", "-m", "backend.app" ]
