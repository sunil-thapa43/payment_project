FROM python:3.12.6

WORKDIR /code

# Python
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1


COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
EXPOSE 50051


# Set the entrypoint
ENTRYPOINT ["/code/runners.sh"]