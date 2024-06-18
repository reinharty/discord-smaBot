FROM python:3.12-slim

# Install tzdata for timezone management
RUN apt-get update && apt-get install -y tzdata
# Set the timezone to Berlin
ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY .env .

ADD main.py .
ADD scraper.py .
ADD message.py .

CMD ["python", "./main.py"]