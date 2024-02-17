FROM python:3.8.10
RUN pip install -r requirements.txt
COPY . /app
WORKDIR /app
CMD ["flask", "run", "--port=8000"]