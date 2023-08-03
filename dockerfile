FROM python:3.8
WORKDIR /code
COPY reqirments.txt /code/reqirments.txt

RUN pip install --upgrade -r /code/reqirments.txt


COPY main.py /code/main.py

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]