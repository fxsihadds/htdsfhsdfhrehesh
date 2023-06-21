# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster


WORKDIR /app


ADD . /app


RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

# Run bot.py when the container launches
CMD ["python", "bot.py"]
