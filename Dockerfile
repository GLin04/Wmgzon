# syntax=docker/dockerfile:1

FROM python:3-alpine3.15

WORKDIR /WMGzon
COPY . .
RUN pip install -r requirements.txt

# Install flask
RUN pip install Flask

EXPOSE 3000
CMD ["python", "./website/main.py"]