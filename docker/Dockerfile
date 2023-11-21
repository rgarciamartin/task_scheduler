FROM python:3.11-alpine
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Postgresql 
RUN apk add --no-cache postgresql-libs postgresql-dev
RUN apk add --no-cache gcc musl-dev

# Configure working directory
RUN mkdir /app  
WORKDIR /app

# Install project requirements
COPY ./app/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY ./app/ /app/

RUN mkdir /scripts
COPY entrypoint.sh /scripts/
