FROM python:3.10
WORKDIR /src/
RUN pip install -U pip
COPY . .
RUN pip install -e .

CMD python test.py
