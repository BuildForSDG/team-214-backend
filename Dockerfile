FROM gcr.io/google_appengine/python

# RUN apt-get update && apt-get install -y && apt-get install curl

RUN virtualenv -p python3.7 /env

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

ENV HOME /app

WORKDIR $HOME

COPY . .

RUN pip install setuptools==46.4 wheel==0.34
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

ENV PATH $HOME/.poetry/bin:$PATH

RUN /bin/bash -c "source .poetry/env"
RUN poetry export -f requirements.txt -o requirements.txt

RUN pip install -r requirements.txt
RUN pip install gunicorn==20.0

CMD gunicorn -b 0.0.0.0:$PORT --workers 1 --threads 8 manage:app