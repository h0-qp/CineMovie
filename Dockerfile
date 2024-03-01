FROM python:latest


RUN git clone https://github.com/h0-qp/bots.git /bots
WORKDIR /bots
RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r api-bots/requirements.txt
CMD python3 run.py