FROM python:3.10-bullseye
RUN mkdir /p
RUN mkdir /p/app
ADD ./app /p/app
#ADD ./manage.py /p
ADD ./requirements.txt /p
WORKDIR /p
#RUN pip install -r requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 5000
CMD ["uvicorn", "app.main.main:app", "--host", "0.0.0.0", "--port", "5000"]
