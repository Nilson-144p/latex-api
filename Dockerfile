FROM texlive/texlive:latest

RUN apt-get update && apt-get install -y python3 python3-pip
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app
WORKDIR /app

CMD ["gunicorn", "app:app"]
