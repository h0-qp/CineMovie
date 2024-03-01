FROM python:latest


RUN git clone https://github.com/h0-qp/MoviesSite.git /MoviesSite
WORKDIR /MoviesSite
RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r MoviesSite/requirements.txt
CMD python3 app.py
