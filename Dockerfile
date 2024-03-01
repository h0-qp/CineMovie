FROM python:latest


RUN git clone https://github.com/h0-qp/CineMovie.git /CineMovie
WORKDIR /CineMovie
RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r CineMovie/requirements.txt
CMD python3 app.py
