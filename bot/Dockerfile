FROM ubuntu

RUN mkdir /app
WORKDIR /app
COPY main.py .
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

ENTRYPOINT [ "python3 main.py" ]